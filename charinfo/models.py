from time import strptime, mktime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from eve.util import *

from eveapi.models import APIKey, ApiError
from evestatic.models import InvType

class Character(models.Model):
    character_id = models.IntegerField(primary_key=True)
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

    def assetlist(self):
        """Get asset list for this character."""
        try:
            return self._assetlist
        except AttributeError:
            self._assetlist = self._get_api_result("char/AssetList").rowset
            return self._assetlist

    def skillqueue(self):
        """Get sorted list of skills in the queue."""
        rows = self._api_skillqueue().rowset
        skillqueue = []
        for row in rows.iterchildren():
            type_id = int(row.get('typeID'))
            level = int(row.get('level'))

            skill = Skill(type_id, level)
            skill.queue_id = int(row.get('queuePosition'))

            try:
                skill.end_timestamp = _str_to_timestamp(row.get('endTime'))
            except ValueError:
                skill.end_timestamp = -1

            skillqueue.append(skill)

        skillqueue.sort(key=lambda x: x.queue_id)
        return skillqueue

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
            skillqueue = self.skillqueue()

            if len(skillqueue) == 0:
                delta_seconds = 0
            else:
                queue_end_timestamp = skillqueue[-1].end_timestamp
                if queue_end_timestamp == -1:
                    delta_seconds = 0
                else:
                    delta_seconds = (queue_end_timestamp -
                                     mktime(timezone.now().timetuple()))

            self._skillqueue_time = timedelta(seconds=delta_seconds)
            return self._skillqueue_time

    def current_skill(self):
        """Get the name of the first skill in the queue."""
        try:
            return self._current_skill
        except AttributeError:
            skillqueue = self.skillqueue()
            self._current_skill = skillqueue[0]
            return self._current_skill

    def current_skill_level(self):
        """Get the level the current skill is being trained to."""
        return self.current_skill().level

    def is_training(self):
        """Check if this character is training."""
        return self.skillqueue_time() > timedelta(0)

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

    def ship(self):
        """Get the ship the character is currently flying."""
        # TODO fix when pilot is docked
        ship = self.assetlist().row
        type_id = ship.get('typeID')
        type_name = InvType.get_type_name(type_id)
        return type_name

    def item_locations(self, item_ids):
        id_string = ','.join(map(str, item_ids))
        result = self._get_api_result("char/Locations", {'IDs': id_string})
        return result.rowset

    def corptag(self):
        """Get a tag in the style [corp] <ally>."""
        char_sheet = self.charactersheet()

        corp = char_sheet.corporationName
        try:
            alliance = char_sheet.allianceName
        except AttributeError:
            alliance = ""

        if len(alliance) > 0:
            return "[{0}] <{1}>".format(corp, alliance)
        else:
            return "[{0}]".format(corp)

    def _api_skillqueue(self):
        """Get SkillQueue API result object for this character."""
        try:
            return self._skillqueue
        except AttributeError:
            self._skillqueue = self._get_api_result("char/SkillQueue")
            return self._skillqueue

    def _get_api_result(self, query, args={}):
        return self.apikey.query(query,
                                 merge_dict({'characterID': self.pk}, args))

class Skill(object):
    def __init__(self, type_id, level=0):
        self.type_id = type_id
        self.level = level
        self.name = InvType.get_type_name(self.type_id)

    def __str__(self):
        return ' '.join([self.name, str(self.level)])

    def __repr__(self):
        return "Skill({0}) '{1}'".format(self.type_id, str(self))

def _str_to_timestamp(time_str):
    return mktime(strptime(" ".join([str(time_str), 'UTC']),
                           "%Y-%m-%d %H:%M:%S %Z"))
