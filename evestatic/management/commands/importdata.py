from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections

from evestatic.models import Race, MarketGroup, InvCategory

class Command(NoArgsCommand):
    args = ''
    help = 'imports EVE static data'
    
    _db_default = connections['default']
    _db_static = connections['evestatic']
    
    def handle_noargs(self, **options):
        self._import_race()
        self._import_marketgroup()
        self._import_invcategory()
        self.stdout.write("import done.")
    
    def _import_map(self):
        pass
    
    # import from chrRaces table:
    # "raceID" integer NOT NULL, -> pk
    # "raceName" varchar(100) DEFAULT NULL, -> name
    # "description" varchar(1000) DEFAULT NULL, -> description
    # "shortDescription" varchar(500) DEFAULT NULL, -> description_short
    def _import_race(self):
        static_table = 'chrRaces'
        static_cols = ['raceID', 'raceName', 'description', 'shortDescription']
        model_params = ['pk', 'name', 'description', 'description_short']
        data_transforms = {
            'description': _string_null_to_empty,
            'shortDescription': _string_null_to_empty,
        }
        self._import_data(Race, model_params, static_table, static_cols, data_transforms)
    
    # import from invMarketGroups table:
    # "marketGroupID" integer NOT NULL, -> pk
    # "parentGroupID" integer DEFAULT NULL, -> parent
    # "marketGroupName" varchar(100) DEFAULT NULL, -> name
    # "description" varchar(3000) DEFAULT NULL, -> description
    # "hasTypes" integer DEFAULT NULL, -> has_types
    def _import_marketgroup(self):
        static_table = 'invMarketGroups'
        static_cols = ['marketGroupID', 'parentGroupID', 'marketGroupName', 'description', 'hasTypes']
        model_params = ['pk', 'parent_id', 'name', 'description', 'has_types']
        data_transforms = {
            'hasTypes': _int_to_bool,
            'description': _string_null_to_empty,
        }
        self._import_data(MarketGroup, model_params, static_table, static_cols, data_transforms)

    # import from invCategories table:
    # "categoryID" integer NOT NULL, -> pk
    # "categoryName" varchar(100) DEFAULT NULL, -> name
    # "description" varchar(3000) DEFAULT NULL, -> description
    # "published" integer DEFAULT NULL, -> published
    def _import_invcategory(self):
        static_table = 'invCategories'
        static_cols = ['categoryID', 'categoryName', 'description', 'published']
        model_params = ['pk', 'name', 'description', 'published']
        data_transforms = {
            'description': _string_null_to_empty,
            'published': _int_to_bool,
        }
        self._import_data(InvCategory, model_params, static_table, static_cols, data_transforms)
    
    def _import_data(self, model, model_params, static_table, static_cols, data_transforms):
        cursor_static = self._db_static.cursor()
        cursor_static.execute("SELECT " + ",".join(static_cols) + " FROM " + static_table)
        
        cursor_default = self._db_default.cursor()
        cursor_default.execute("DELETE FROM " + model._meta.db_table)
        
        for row in cursor_static.fetchall():
            d = dict()
            for i in range(len(row)):
                if static_cols[i] in data_transforms:
                    d[model_params[i]] = data_transforms[static_cols[i]](row[i])
                else:
                    d[model_params[i]] = row[i]
            model(**d).save()
        
        self.stdout.write("imported %s -> %s" % (static_table, model.__name__))
    
def _string_null_to_empty(value):
    if value is None:
        return ""
    else:
        return value

def _int_to_bool(value):
    return value == 1
