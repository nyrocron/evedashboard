from django.db import models

from django.contrib.auth.models import User

from eveapi.models import ApiKey, ApiError

class Character(models.Model):
    apikey = models.ForeignKey(ApiKey)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    
    def __str__(self, ):
        return self.name

    def charactersheet(self):
        sheet = self.apikey.query("char/CharacterSheet", { 'characterID': self.pk })
        return sheet