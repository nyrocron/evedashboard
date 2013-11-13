from django.forms import ModelForm
from charinfo.models import Character

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ['character_id', 'name', 'apikey']
