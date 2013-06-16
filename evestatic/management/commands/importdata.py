from django.core.management.base import NoArgsCommand
from django.db import connections, transaction

from eve import settings

from evestatic.models import InvName, InvCategory, InvGroup, InvType
from evestatic.models import MarketGroup
from evestatic.models import NPCCorporation, Race, Faction
from evestatic.models import Region, Constellation, SolarSystem
from evestatic.models import MapDenormalize, Station

class Command(NoArgsCommand):
    args = ''
    help = 'imports EVE static data'
    
    _db_default = connections['default']
    _db_static = connections['evestatic']
    
    def handle_noargs(self, **options):
        # attach default to static db
        cursor_static = self._db_static.cursor()
        #cursor_static.execute("ATTACH '%s' AS eve" %
        #                      settings.DATABASES['default']['NAME'])
        
        # inv
        self._import_invname()
        self._import_marketgroup()
        self._import_invcategory()
        self._import_invgroup()
        self._import_invtype()
        
        # chr
        self._import_npc_corporation()
        self._import_race()
        self._import_faction()
        
        # map
        self._import_region()
        self._import_constellation()
        self._import_solarsystem()
        self._import_jumps()
        self._import_map_denormalize()
        
        # sta
        self._import_station()
        
        self.stdout.write("Static data import done.")
    
    def _import_invname(self, ):
        """Import data from invNames to InvName model."""
        self._import_table_data_direct('invNames', InvName, [
            ('itemID', 'id', None),
            ('itemName', 'name', None)
        ])
    
    def _import_marketgroup(self):
        """Import from invMarketGroups table to MargetGroup model."""
        self._import_table_data('invMarketGroups', MarketGroup, [
            ('marketGroupID', 'id', None),
            ('parentGroupID', 'parent_id', None),
            ('marketGroupName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('hasTypes', 'has_types', _int_to_bool),
        ])

    def _import_invcategory(self):
        """Import from invCategories table to InvCategory model."""
        self._import_table_data('invCategories', InvCategory, [
            ('categoryID', 'id', None),
            ('categoryName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('published', 'is_published', _int_to_bool),
        ])
    
    def _import_invgroup(self):
        """Import from invGroups table to InvGroup model."""
        self._import_table_data('invGroups', InvGroup, [
            ('groupID', 'id', None),
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
            ('typeID', 'id', None),
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
    
    def _import_npc_corporation(self):
        """Import data from crpNPCCorporations to NPCCorporation model."""
        self._import_table_data('crpNPCCorporations', NPCCorporation, [
            ('corporationID', 'id', None),
            ('factionID', 'faction_id', None),
            ('solarSystemID', 'solarsystem_id', None),
            ('description', 'description', _string_null_to_empty),
            ('size', 'size', _string_null_to_empty),
            ('extent', 'extent', _string_null_to_empty),
            ('sizeFactor', 'size_factor', None),
            ('stationCount', 'station_count', _int_null_to_zero),
            ('stationSystemCount', 'station_system_count', _int_null_to_zero),
        ])
    
    def _import_race(self):
        """Import from chrRaces table to Race model."""
        self._import_table_data('chrRaces', Race, [
            ('raceID', 'id', None),
            ('raceName', 'name', None),
            ('description', 'description', _string_null_to_empty),
            ('shortDescription', 'description_short', _string_null_to_empty),
        ])
    
    def _import_faction(self):
        """Import data from chrFactions table to Faction model."""
        self._import_table_data('chrFactions', Faction, [
            ('factionID', 'id', None),
            ('factionName', 'name', None),
            ('solarSystemID', 'hq_system_id', None),
            ('description', 'description', _string_null_to_empty),
            ('corporationID', 'main_corporation_id', None),
            ('sizeFactor', 'size_factor', None),
            ('stationCount', 'station_count', None),
            ('stationSystemCount', 'station_system_count', None),
        ])
    
    def _import_region(self):
        """Import data from mapRegions table to Region model."""
        self._import_table_data('mapRegions', Region, [
            ('regionID', 'id', None),
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
            ('constellationID', 'id', None),
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
            ('solarSystemID', 'id', None),
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
    
    def _import_map_denormalize(self):
        """Import data from mapDenormalize to MapDenormalize model."""
        self._import_table_data_direct('mapDenormalize', MapDenormalize, [
            ('itemID', 'id', None),
            ('itemName', 'name', None),
            ('typeID', 'inv_type', None),
            ('groupID', 'inv_group', None),
            ('solarSystemID', 'solarsystem', None),
            ('constellationID', 'constellation', None),
            ('regionID', 'region', None),
            ('orbitID', 'orbit', None),
            ('celestialIndex', 'celestial_index', None),
            ('orbitIndex', 'orbit_index', None),
            ('security', 'security', None),
            ('radius', 'radius', None),
            ('x', 'x', None),
            ('y', 'y', None),
            ('z', 'z', None),
        ])
    
    def _import_station(self):
        """Import data from staStations to Station model."""
        self._import_table_data('staStations', Station, [
            ('stationID', 'station_id', None),
            ('stationName', 'name', None),
            ('stationTypeID', 'station_type_id', None),
            ('corporationID', 'corporation_id', None),
            ('solarSystemID', 'solarsystem_id', None),
            ('constellationID', 'constellation_id', None),
            ('regionID', 'region_id', None),
            ('security', 'security', None),
            ('maxShipVolumeDockable', 'max_dock_volume', None),
            ('reprocessingEfficiency', 'reprocessing_efficiency', None),
            ('reprocessingStationsTake', 'reprocessing_take', None),
            ('x', 'x', None),
            ('y', 'y', None),
            ('z', 'z', None),
        ])
    
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
        
        cursor_static = self._db_static.cursor()
        static_cols = ",".join([x[0] for x in col_map])
        cursor_static.execute("SELECT %s FROM %s" %
                              (static_cols, static_table))
        
        # if there are no transformations to be applied, import data via SQL
        #if (all(item[2] is None for item in col_map) and
        #    settings.DATABASES['default']['ENGINE'] ==
        #        'django.db.backends.sqlite3' and
        #    settings.DATABASES['evestatic']['ENGINE'] ==
        #        'django.db.backends.sqlite3'):
        #    self.stdout.write("using direct import...")
        #    model_table = model._meta.db_table
        #    model_cols = ",".join([model._meta.get_field(x[1]).column
        #                           for x in col_map])
        #    
        #    cursor_static.execute("ATTACH '%s' AS eve" %
        #                          settings.DATABASES['default']['NAME'])
        #    transaction.commit_unless_managed()
        #    
        #    cursor_static.execute("INSERT INTO eve.%s (%s) SELECT %s FROM %s" %
        #                          (model._meta.db_table, model_cols,
        #                           static_cols, static_table))
        #    transaction.commit_unless_managed()
        #    return
                
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
    
    def _import_table_data_direct(self, static_table, model, col_map):
        """Directly import table data via SQL"""
        assert(settings.DATABASES['default']['ENGINE'] ==
               'django.db.backends.sqlite3')
        assert(settings.DATABASES['evestatic']['ENGINE'] ==
               'django.db.backends.sqlite3')
                #    model_table = model._meta.db_table
        
        self.stdout.write("Direct import: %s -> %s" %
                          (static_table, model.__name__))
        
        cursor_static = self._db_static.cursor()
        static_cols = ",".join([x[0] for x in col_map])
        model_cols = ",".join([model._meta.get_field(x[1]).column
                               for x in col_map])
        
        #cursor_static.execute("INSERT INTO eve.%s (%s) SELECT %s FROM %s" %
        #                      (model._meta.db_table, model_cols,
        #                       static_cols, static_table))
        #transaction.commit()

def _int_to_bool(value):
    return value == 1
    
def _int_null_to_zero(value):
    if value is None:
        return 0
    else:
        return value

def _string_null_to_empty(value):
    if value is None:
        return ""
    else:
        return value