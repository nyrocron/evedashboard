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
        self.stdout.write("Static data import done.")
    
    def _import_race(self):
        """ Import from chrRaces table.
        
        "raceID" integer NOT NULL, -> pk
        "raceName" varchar(100) DEFAULT NULL, -> name
        "description" varchar(1000) DEFAULT NULL, -> description
        "shortDescription" varchar(500) DEFAULT NULL, -> description_short
        
        """
        self._import_data('chrRaces', Race, [
            ('raceID', 'pk', None),
            ('raceName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('shortDescription', 'description_short', _string_null_to_empty),
        ])
    
    def _import_marketgroup(self):
        """ Import from invMarketGroups table.
        
        "marketGroupID" integer NOT NULL, -> pk
        "parentGroupID" integer DEFAULT NULL, -> parent
        "marketGroupName" varchar(100) DEFAULT NULL, -> name
        "description" varchar(3000) DEFAULT NULL, -> description
        "hasTypes" integer DEFAULT NULL, -> has_types
    
        """
        self._import_data('invMarketGroups', MarketGroup, [
            ('marketGroupID', 'pk', None),
            ('parentGroupID', 'parent_id', None),
            ('marketGroupName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('hasTypes', 'has_types', _int_to_bool),
        ])

    def _import_invcategory(self):
        """ Import from invCategories table.
        
        "categoryID" integer NOT NULL, -> pk
        "categoryName" varchar(100) DEFAULT NULL, -> name
        "description" varchar(3000) DEFAULT NULL, -> description
        "published" integer DEFAULT NULL, -> published
        
        """
        self._import_data('invCategories', InvCategory, [
            ('categoryID', 'pk', None),
            ('categoryName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('published', 'published', _int_to_bool),
        ])
    
    #def _import_invgroup(self):
    #    """ Import from invGroups table into InvGroup model"""
    #    static_table = 'invGroups'
    #    static_cols = ['groupID', 'categoryID', 'groupName', 'description', 'useBasePrice', 'allowManufacture']
    #    model_params = ['pk', 'name', 'description', 'published']
    #    data_transforms = {
    #        'description': _string_null_to_empty,
    #        'published': _int_to_bool,
    #    }
    #    self._import_data(InvCategory, model_params, static_table, static_cols, data_transforms)
    
    def _import_data(self, static_table, model, col_map):
        """ Import data from a static db table to a model"""
        # query static db
        cursor_static = self._db_static.cursor()
        cursor_static.execute("SELECT " + ",".join([x[0] for x in col_map]) +
                              " FROM " + static_table)
        
        # delete old values
        cursor_default = self._db_default.cursor()
        cursor_default.execute("DELETE FROM " + model._meta.db_table)
        
        # from sql result create models, apply tranform if there is any,
        # then save the created object
        for row in cursor_static.fetchall():
            model_values = dict()
            for i in range(len(col_map)):
                if col_map[i][2] is not None:
                    model_values[col_map[i][1]] = col_map[i][2](row[i])
                else:
                    model_values[col_map[i][1]] = row[i]
            model(**model_values).save()
        
        self.stdout.write("Imported %s -> %s." % (static_table, model.__name__))
    
def _string_null_to_empty(value):
    if value is None:
        return ""
    else:
        return value

def _int_to_bool(value):
    return value == 1
