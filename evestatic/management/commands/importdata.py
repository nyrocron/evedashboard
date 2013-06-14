from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections

from evestatic.models import Race

class Command(NoArgsCommand):
    args = ''
    help = 'imports EVE static data'
    _static_db = connections['evestatic']
    
    def handle_noargs(self, **options):
        self._import_race()
        self.stdout.write("import done.")
    
    def _import_map(self):
        pass
    
    # import chrRaces table:
    # "raceID" integer NOT NULL, -> pk
    # "raceName" varchar(100) DEFAULT NULL, -> name
    # "description" varchar(1000) DEFAULT NULL, -> description
    # "shortDescription" varchar(500) DEFAULT NULL, -> description_short
    def _import_race(self):
        static_table = 'chrRaces'
        static_cols = ['raceID', 'raceName', 'description', 'shortDescription']
        model_params = ['pk', 'name', 'description', 'description_short']
        self._import_data(static_table, static_cols, Race, model_params)
    
    def _import_data(self, static_table, static_cols, model, model_params):
        cursor = self._static_db.cursor()
        cursor.execute("SELECT " + ",".join(static_cols) + " FROM " + static_table)
        
        model.objects.all().delete()
        for row in cursor.fetchall():
            d = dict()
            for i in range(len(row)):
                d[model_params[i]] = row[i]
            model(**d).save()
        
        self.stdout.write("imported %s -> %s" % (static_table, model.__name__))