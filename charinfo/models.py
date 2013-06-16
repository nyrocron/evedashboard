from time import strptime, mktime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from eveapi.models import APIKey, ApiError
from evestatic.models import InvType

class Character(models.Model):
    apikey = models.ForeignKey(APIKey)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    def charactersheet(self):
        """Get CharacterSheet API result object for this character."""
        try:
            return self._charsheet
        except AttributeError:
            self._charsheet = self._get_api_result("char/CharacterSheet")
            return self._charsheet
    
    def skillqueue(self):
        """Get SkillQueue API result object for this character."""
        try:
            return self._skillqueue
        except AttributeError:
            self._skillqueue = self._get_api_result("char/SkillQueue")
            return self._skillqueue
    
    def accountstatus(self):
        """Get AccountStatus API result object for this character."""
        try:
            return self._accountstatus
        except AttributeError:
            self._accountstatus = self._get_api_result("account/AccountStatus")
            return self._accountstatus
    
    def total_skillpoints(self):
        """Get total skillpoints of this character."""
        try:
            return self._total_sp
        except AttributeError:
            self._total_sp = 0
            skills = self.charactersheet().find("rowset[@name='skills']")
            for skill in skills.iterchildren():
                self._total_sp += int(skill.get("skillpoints"))
            return self._total_sp
    
    def skillqueue_time(self):
        """Get time until the end of this character's skillqueue."""
        try:
            return self._skillqueue_time
        except AttributeError:
            skillqueue = self.skillqueue().rowset
            
            current_skill_id = None
            current_skill_level = None
            queue_end_timestamp = 0
            for skill in skillqueue.iterchildren():
                if int(skill.get('queuePosition')) == 0:
                    current_skill_id = int(skill.get('typeID'))
                    current_skill_level = int(skill.get('level'))
                skill_end_timestamp = _str_to_timestamp(skill.get('endTime'))
                queue_end_timestamp = max(queue_end_timestamp,
                                          skill_end_timestamp)
            
            if current_skill_id is None:
                delta_seconds = 0    
            else:
                now_timestamp = mktime(timezone.now().timetuple())
                delta_seconds = queue_end_timestamp - now_timestamp
                self._current_skill = InvType.get_type_name(current_skill_id)
                self._current_skill_level = current_skill_level
            self._skillqueue_time = timedelta(seconds=delta_seconds)
            return self._skillqueue_time
    
    def current_skill(self):
        """Get time until the end of this character's skillqueue."""
        try:
            return self._current_skill
        except AttributeError:
            skillqueue = self.skillqueue().rowset
            
            current_skill_id = None
            current_skill_level = None
            for skill in skillqueue.iterchildren():
                if int(skill.get('queuePosition')) == 0:
                    current_skill_id = int(skill.get('typeID'))
                    current_skill_level = int(skill.get('level'))
                    break
            
            if current_skill_id is None:
                self._current_skill = ""
                self._current_skill_level = 0
            else:
                self._current_skill = InvType.get_type_name(current_skill_id)
                self._current_skill_level = current_skill_level
            return self._current_skill
    
    def current_skill_level(self):
        """Get the level the current skill is being trained to."""
        try:
            return self._current_skill_level
        except AttributeError:
            self.current_skill()
            return self._current_skill_level
    
    def is_training(self):
        """Check if this character is training."""
        return self.current_skill() != ""
    
    def subscribed_time(self):
        """
        Get time until the subscription for this character's account expires.
        """
        try:
            return self._subscribed_time
        except AttributeError:
            paid_until = self.accountstatus().paidUntil
            paid_until_timestamp = _str_to_timestamp(paid_until)
            now_timestamp = mktime(timezone.now().timetuple())
            delta_seconds = paid_until_timestamp - now_timestamp
            
            self._subscribed_time = timedelta(seconds=delta_seconds)
            return self._subscribed_time
    
    def _get_api_result(self, query):
        return self.apikey.query(query, {'characterID': self.pk})
    
def _str_to_timestamp(time_str):
    return mktime(strptime(" ".join([str(time_str), 'UTC']),
                           "%Y-%m-%d %H:%M:%S %Z"))