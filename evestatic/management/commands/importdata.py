from django.core.management.base import NoArgsCommand, CommandError
from django.db import connections

from evestatic.models import Race
from evestatic.models import MarketGroup, InvCategory, InvGroup, InvType

class Command(NoArgsCommand):
    args = ''
    help = 'imports EVE static data'
    
    _db_default = connections['default']
    _db_static = connections['evestatic']
    
    def handle_noargs(self, **options):
        self._import_race()
        self._import_marketgroup()
        self._import_invcategory()
        self._import_invgroup()
        self._import_invtype()
        self.stdout.write("Static data import done.")
    
    def _import_race(self):
        """ Import from chrRaces table to Race model."""
        self._import_data('chrRaces', Race, [
            ('raceID', 'pk', None),
            ('raceName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('shortDescription', 'description_short', _string_null_to_empty),
        ])
    
    def _import_marketgroup(self):
        """Import from invMarketGroups table to MargetGroup model."""
        self._import_data('invMarketGroups', MarketGroup, [
            ('marketGroupID', 'pk', None),
            ('parentGroupID', 'parent_id', None),
            ('marketGroupName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('hasTypes', 'has_types', _int_to_bool),
        ])

    def _import_invcategory(self):
        """Import from invCategories table to InvCategory model."""
        self._import_data('invCategories', InvCategory, [
            ('categoryID', 'pk', None),
            ('categoryName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('published', 'published', _int_to_bool),
        ])
    
    def _import_invgroup(self):
        """Import from invGroups table to InvGroup model"""
        self._import_data('invGroups', InvGroup, [
            ('groupID', 'pk', None),
            ('categoryID', 'invcategory_id', None),
            ('groupName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('useBasePrice', 'use_baseprice', _int_to_bool),
            ('allowManufacture', 'allow_manufacture', _int_to_bool),
            ('allowRecycler', 'allow_recycler', _int_to_bool),
            ('anchored', 'anchored', _int_to_bool),
            ('anchorable', 'anchorable', _int_to_bool),
            ('fittableNonSingleton', 'fittable_non_singleton', _int_to_bool),
            ('published', 'published', _int_to_bool),
        ])
    
    def _import_invtype(self):
        """Import from invTypes table to InvTypes model."""
        self._import_data('invTypes', InvType, [
            ('typeID', 'pk', None),
            ('typeName', 'name', None),
            ('groupID', 'invgroup_id', None),
            ('marketGroupID', 'marketgroup_id', None),
            ('description', 'description', _string_null_to_empty),
            ('mass', 'mass', None),
            ('volume', 'volume', None),
            ('portionSize', 'portion_size', None),
            ('raceID', 'race_id', None),
            ('basePrice', 'baseprice', None),
            ('published', 'published', _int_to_bool),
        ])
    
    def _import_data(self, static_table, model, col_map):
        """ Import data from a static db table to a model"""
        self.stdout.write("Importing %s -> %s..." %
                          (static_table, model.__name__))
                          #ending='')
        
        # query static db
        cursor_static = self._db_static.cursor()
        cursor_static.execute("SELECT " + ",".join([x[0] for x in col_map]) +
                              " FROM " + static_table)
        
        # delete old values
        cursor_default = self._db_default.cursor()
        cursor_default.execute("DELETE FROM " + model._meta.db_table)
        
        # from sql result create models, apply transform if there is any,
        # then save the created object
        for row in cursor_static.fetchall():
            model_values = dict()
            for i in range(len(col_map)):
                if col_map[i][2] is not None: # transform defined
                    model_values[col_map[i][1]] = col_map[i][2](row[i])
                else:
                    model_values[col_map[i][1]] = row[i]
            model(**model_values).save()
        
        #self.stdout.write("done.")
    
def _string_null_to_empty(value):
    if value is None:
        return ""
    else:
        return value

def _int_to_bool(value):
    return value == 1
