from django.core.management.base import NoArgsCommand
from django.db import connections

from evestatic.models import Race, Faction
from evestatic.models import MarketGroup, InvCategory, InvGroup, InvType
from evestatic.models import Region, Constellation, SolarSystem

class Command(NoArgsCommand):
    args = ''
    help = 'imports EVE static data'
    
    _db_default = connections['default']
    _db_static = connections['evestatic']
    
    def handle_noargs(self, **options):
        # chr
        self._import_race()
        self._import_faction()
        
        # inv
        self._import_marketgroup()
        self._import_invcategory()
        self._import_invgroup()
        self._import_invtype()
        
        #map
        self._import_region()
        self._import_constellation()
        self._import_solarsystem()
        self._import_jumps()
        
        self.stdout.write("Static data import done.")
    
    def _import_race(self):
        """ Import from chrRaces table to Race model."""
        self._import_table_data('chrRaces', Race, [
            ('raceID', 'pk', None),
            ('raceName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('shortDescription', 'description_short', _string_null_to_empty),
        ])
    
    def _import_faction(self):
        """Import data from chrFactions table to Faction model."""
        self._import_table_data('chrFactions', Faction, [
            ('factionID', 'pk', None),
            ('factionName', 'name', None),
            #('solarSystemID', 'hq_system_id', None),
            ('description', 'description', _string_null_to_empty),
            #('corporationID', 'corporation', None),
            ('sizeFactor', 'size_factor', None),
            ('stationCount', 'station_count', None),
            ('stationSystemCount', 'station_system_count', None),
        ])
    
    def _import_marketgroup(self):
        """Import from invMarketGroups table to MargetGroup model."""
        self._import_table_data('invMarketGroups', MarketGroup, [
            ('marketGroupID', 'pk', None),
            ('parentGroupID', 'parent_id', None),
            ('marketGroupName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('hasTypes', 'has_types', _int_to_bool),
        ])

    def _import_invcategory(self):
        """Import from invCategories table to InvCategory model."""
        self._import_table_data('invCategories', InvCategory, [
            ('categoryID', 'pk', None),
            ('categoryName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('published', 'is_published', _int_to_bool),
        ])
    
    def _import_invgroup(self):
        """Import from invGroups table to InvGroup model."""
        self._import_table_data('invGroups', InvGroup, [
            ('groupID', 'pk', None),
            ('categoryID', 'invcategory_id', None),
            ('groupName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('useBasePrice', 'is_use_baseprice', _int_to_bool),
            ('allowManufacture', 'is_allow_manufacture', _int_to_bool),
            ('allowRecycler', 'is_allow_recycler', _int_to_bool),
            ('anchored', 'is_anchored', _int_to_bool),
            ('anchorable', 'is_anchorable', _int_to_bool),
            ('fittableNonSingleton', 'is_fittable_non_singleton', _int_to_bool),
            ('published', 'is_published', _int_to_bool),
        ])
    
    def _import_invtype(self):
        """Import from invTypes table to InvTypes model."""
        self._import_table_data('invTypes', InvType, [
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
            ('published', 'is_published', _int_to_bool),
        ])
    
    def _import_region(self):
        """Import data from mapRegions table to Region model."""
        self._import_table_data('mapRegions', Region, [
            ('regionID', 'pk', None),
            ('regionName', 'name', None),
            ('factionID', 'faction_id', None),
            ('radius', 'radius', None),
            ('x', 'x', None),
            ('y', 'y', None),
            ('z', 'z', None),
            ('xMin', 'x_min', None),
            ('yMin', 'y_min', None),
            ('zMin', 'z_min', None),
            ('xMax', 'x_max', None),
            ('yMax', 'y_max', None),
            ('zMax', 'z_max', None),
        ])
    
    def _import_constellation(self):
        """Import data from mapConstellations to Constellation model"""
        self._import_table_data('mapConstellations', Constellation, [
            ('constellationID', 'pk', None),
            ('constellationName', 'name', None),
            ('regionID', 'region_id', None),
            ('factionID', 'faction_id', None),
            ('radius', 'radius', None),
            ('x', 'x', None),
            ('y', 'y', None),
            ('z', 'z', None),
            ('xMin', 'x_min', None),
            ('yMin', 'y_min', None),
            ('zMin', 'z_min', None),
            ('xMax', 'x_max', None),
            ('yMax', 'y_max', None),
            ('zMax', 'z_max', None),
        ])
    
    def _import_solarsystem(self):
        """Import data from mapSolarSystems table to SolarSystem model."""
        self._import_table_data('mapSolarSystems', SolarSystem, [
            ('solarSystemID', 'pk', None),
            ('solarSystemName', 'name', None),
            ('regionID', 'region_id', None),
            ('constellationID', 'constellation_id', None),
            ('security', 'security', None),
            ('securityClass', 'security_class', None),
            ('radius', 'radius', None),
            ('luminosity', 'luminosity', None),
            ('border', 'is_border', _int_to_bool),
            ('fringe', 'is_fringe', _int_to_bool),
            ('corridor', 'is_corridor', _int_to_bool),
            ('hub', 'is_hub', _int_to_bool),
            ('international', 'is_international', _int_to_bool),
            ('regional', 'is_regional', _int_to_bool),
            ('constellation', 'is_constellation', _int_to_bool),
            ('x', 'x', None),
            ('y', 'y', None),
            ('z', 'z', None),
            ('xMin', 'x_min', None),
            ('yMin', 'y_min', None),
            ('zMin', 'z_min', None),
            ('xMax', 'x_max', None),
            ('yMax', 'y_max', None),
            ('zMax', 'z_max', None),
        ])
    
    def _import_jumps(self):
        """Import data from mapSolarSystemJumps to SolarSystem.jumps"""
        # only import if there are no values for jumps already
        cursor_default = self._db_default.cursor()
        cursor_default.execute("SELECT COUNT(*)"
                               " FROM evestatic_solarsystem_jumps""")
        jumps_count = cursor_default.fetchone()[0]
        if jumps_count > 0:
            self.stdout.write("evestatic_solarsystem_jumps already has data,"
                              " skipping import")
            return
        
        self.stdout.write("Importing mapSolarSystemJumps...")
        
        cursor_static = self._db_static.cursor()
        cursor_static.execute("SELECT fromSolarSystemID, toSolarSystemID "
                              " FROM mapSolarSystemJumps")
        for row in cursor_static.fetchall():
            system_from = SolarSystem.objects.get(pk=row[0])
            system_to = SolarSystem.objects.get(pk=row[1])
            system_from.jumps.add(system_to)
    
    def _import_table_data(self, static_table, model, col_map):
        """ Import data from a static db table to a model"""
        # only import if there are no values in the table
        if model.objects.count() > 0:
            self.stdout.write("Model %s already has objects, skipping import" %
                              model.__name__)
            return
        
        self.stdout.write("Importing %s -> %s..." %
                          (static_table, model.__name__))
                          #ending='')
        
        # query static db
        cursor_static = self._db_static.cursor()
        cursor_static.execute("SELECT " + ",".join([x[0] for x in col_map]) +
                              " FROM " + static_table)
                
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
    
def _string_null_to_empty(value):
    if value is None:
        return ""
    else:
        return value

def _int_to_bool(value):
    return value == 1
