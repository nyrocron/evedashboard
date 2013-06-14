from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from evestatic.models import SolarSystem

class Command(BaseCommand):
    args = ''
    help = 'imports EVE static data'
    
    def handle(self, *args, **options):
        self._importMap()
    
    def _importMap(self):
        cursor = connections['evestatic']
    