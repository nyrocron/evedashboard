from django.db import models

class InvName(models.Model):
    """ Equivalent of invNames
    
    "itemID" integer NOT NULL, -> pk
    "itemName" varchar(200) NOT NULL, -> name
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class InvCategory(models.Model):
    
    """ Equivalent of invCategories

    "categoryID" integer NOT NULL, -> pk
    "categoryName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(3000) DEFAULT NULL, -> description
    "published" integer DEFAULT NULL, -> is_published
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=3000)
    is_published = models.BooleanField()
    
    def __str__(self):
        return self.name

class InvGroup(models.Model):
    
    """ Equivalent of invGroups
    
    "groupID" integer NOT NULL, -> pk
    "categoryID" integer DEFAULT NULL, -> invcategory
    "groupName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(3000) DEFAULT NULL, -> description
    "useBasePrice" integer DEFAULT NULL, -> is_use_baseprice
    "allowManufacture" integer DEFAULT NULL, -> is_allow_manufacture
    "allowRecycler" integer DEFAULT NULL, -> is_allow_recycler
    "anchored" integer DEFAULT NULL, -> is_anchored
    "anchorable" integer DEFAULT NULL, -> is_anchorable
    "fittableNonSingleton" integer DEFAULT NULL, -> is_fittable_non_singleton
    "published" integer DEFAULT NULL, -> is_published
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    invcategory = models.ForeignKey(InvCategory)
    description = models.CharField(max_length=3000)
    is_use_baseprice = models.BooleanField()
    is_allow_manufacture = models.BooleanField()
    is_allow_recycler = models.BooleanField()
    is_anchored = models.BooleanField()
    is_anchorable = models.BooleanField()
    is_fittable_non_singleton = models.BooleanField()
    is_published = models.BooleanField()
    
    def __str__(self):
        return self.name

class MarketGroup(models.Model):
    """ Equivalent of marketGroups
    
    "marketGroupID" integer NOT NULL, -> pk
    "parentGroupID" integer DEFAULT NULL, -> parent
    "marketGroupName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(3000) DEFAULT NULL, -> description
    "hasTypes" integer DEFAULT NULL, -> has_types
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)
    description = models.CharField(max_length=3000)
    has_types = models.BooleanField()
    
    def __str__(self):
        return self.name

class InvType(models.Model):
    """ Equivalent of invTypes
    
    "typeID" integer NOT NULL, -> pk
    "typeName" varchar(100) DEFAULT NULL, -> name
    "groupID" integer DEFAULT NULL, -> invgroup
    "marketGroupID" integer DEFAULT NULL, -> marketgroup
    "raceID" integer DEFAULT NULL, -> race
    "description" varchar(3000) DEFAULT NULL, -> description
    "mass" double DEFAULT NULL, -> mass
    "volume" double DEFAULT NULL, -> volume
    "capacity" double DEFAULT NULL, -> capacity
    "portionSize" integer DEFAULT NULL, -> portion_size
    "basePrice" decimal(19,4) DEFAULT NULL, -> baseprice
    "published" integer DEFAULT NULL, -> is_published
    
    not implemented:
    "chanceOfDuplicating" double DEFAULT NULL,
    
    """

    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    invgroup = models.ForeignKey(InvGroup)
    marketgroup = models.ForeignKey(MarketGroup, null=True)
    race = models.ForeignKey('Race', null=True)
    description = models.CharField(max_length=3000)
    mass = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    capacity = models.FloatField(null=True)
    portion_size = models.IntegerField(null=True)
    baseprice = models.DecimalField(max_digits=19, decimal_places=4)
    is_published = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_type_name(type_id):
        return InvType.objects.get(pk=type_id).name

class Race(models.Model):
    """ Equivalent of chrRaces
    
    "raceID" integer NOT NULL, -> pk
    "raceName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(1000) DEFAULT NULL, -> description
    "shortDescription" varchar(500) DEFAULT NULL, -> description_short
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """

    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    description_short = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

class NPCCorporation(models.Model):
    """ Equivalent of chrNPCCorporations
    
    "corporationID" integer NOT NULL, -> pk
    "factionID" integer DEFAULT NULL, -> faction (ref Faction)
    "solarSystemID" integer DEFAULT NULL, -> solarsystem (ref SolarSystem)
    "description" varchar(4000) DEFAULT NULL, -> description
    "size" char(1) DEFAULT NULL, -> size
    "extent" char(1) DEFAULT NULL, -> extent
    "sizeFactor" double DEFAULT NULL, -> size_factor
    "stationCount" integer DEFAULT NULL, -> station_count
    "stationSystemCount" integer DEFAULT NULL, -> station_system_count
    
    not implemented:
    "investorID1" integer DEFAULT NULL,
    "investorShares1" integer DEFAULT NULL,
    "investorID2" integer DEFAULT NULL,
    "investorShares2" integer DEFAULT NULL,
    "investorID3" integer DEFAULT NULL,
    "investorShares3" integer DEFAULT NULL,
    "investorID4" integer DEFAULT NULL,
    "investorShares4" integer DEFAULT NULL,
    "friendID" integer DEFAULT NULL, 
    "enemyID" integer DEFAULT NULL,
    "publicShares" integer DEFAULT NULL,
    "initialPrice" integer DEFAULT NULL,
    "minSecurity" double DEFAULT NULL,
    "iconID" integer DEFAULT NULL,
    "scattered" integer DEFAULT NULL, -> is_scattered
    "fringe" integer DEFAULT NULL, -> is_fringe
    "corridor" integer DEFAULT NULL, -> is_corridor
    "hub" integer DEFAULT NULL, -> is_hub
    "border" integer DEFAULT NULL, -> is_border
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    faction = models.ForeignKey('Faction')
    solarsystem = models.ForeignKey('SolarSystem')
    description = models.CharField(max_length=4000, null=True)
    size = models.CharField(max_length=1)
    extent = models.CharField(max_length=1)
    size_factor = models.FloatField(null=True)
    station_count = models.FloatField()
    station_system_count = models.FloatField()
    
    def __str__(self):
        return self.name()
    
    def name(self):
        """Get the name of this corporation"""
        try:
            return self._name
        except AttributeError:
            self._name = InvName.objects.get(pk=self.pk).name
            return self._name

class Faction(models.Model):
    """ Equivalent of chrFactions
    
    "factionID" integer NOT NULL, -> pk
    "factionName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(1000) DEFAULT NULL, -> description
    "sizeFactor" double DEFAULT NULL, -> size_factor
    "stationCount" integer DEFAULT NULL, -> station_count
    "stationSystemCount" integer DEFAULT NULL, -> station_system_count
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    "militiaCorporationID" integer DEFAULT NULL,
    "raceIDs" integer DEFAULT NULL,
    "solarSystemID" integer DEFAULT NULL, -> hq_system
    "corporationID" integer DEFAULT NULL, -> corporation
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    hq_system = models.ForeignKey('SolarSystem')
    description = models.CharField(max_length=1000)
    main_corporation = models.ForeignKey(NPCCorporation,
                                         related_name='main_corporation')
    size_factor = models.FloatField()
    station_count = models.IntegerField()
    station_system_count = models.IntegerField()
    
    def __str__(self):
        return self.name

class Region(models.Model):
    """ Equivalent of mapRegions
    
    "regionID" integer NOT NULL, -> pk
    "regionName" varchar(100) DEFAULT NULL, -> name
    "factionID" integer DEFAULT NULL, -> faction
    "radius" double DEFAULT NULL, -> radius
    "x" double DEFAULT NULL, -> x
    "y" double DEFAULT NULL, -> y
    "z" double DEFAULT NULL, -> z
    "xMin" double DEFAULT NULL, -> x_min
    "xMax" double DEFAULT NULL, -> x_max
    "yMin" double DEFAULT NULL, -> y_min
    "yMax" double DEFAULT NULL, -> y_max
    "zMin" double DEFAULT NULL, -> z_min
    "zMax" double DEFAULT NULL, -> z_max
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, null=True)
    radius = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    x_min = models.FloatField()
    y_min = models.FloatField()
    z_min = models.FloatField()
    x_max = models.FloatField()
    y_max = models.FloatField()
    z_max = models.FloatField()
    
    def __str__(self, ):
        return self.name

class Constellation(models.Model):
    """ Equivalent of mapConstellations
    
    "constellationID" integer NOT NULL, -> pk
    "constellationName" varchar(100) DEFAULT NULL, -> name
    "regionID" integer DEFAULT NULL, -> region
    "factionID" integer DEFAULT NULL, -> faction
    "radius" double DEFAULT NULL, -> radius
    "x" double DEFAULT NULL, -> x
    "y" double DEFAULT NULL, -> y
    "z" double DEFAULT NULL, -> z
    "xMin" double DEFAULT NULL, -> x_min
    "yMin" double DEFAULT NULL, -> y_min
    "zMin" double DEFAULT NULL, -> z_min
    "xMax" double DEFAULT NULL, -> x_max
    "yMax" double DEFAULT NULL, -> y_max
    "zMax" double DEFAULT NULL, -> z_max
    
    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)
    faction = models.ForeignKey(Faction, null=True)
    radius = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    x_min = models.FloatField()
    y_min = models.FloatField()
    z_min = models.FloatField()
    x_max = models.FloatField()
    y_max = models.FloatField()
    z_max = models.FloatField()
    
    def __str__(self):
        return self.name

class SolarSystem(models.Model):
    """ Equivalent of mapSolarSystems
    
    "solarSystemID" integer NOT NULL, -> pk
    "solarSystemName" varchar(100) DEFAULT NULL, -> name
    "regionID" integer DEFAULT NULL, -> region
    "constellationID" integer DEFAULT NULL, -> constellation
    "security" double DEFAULT NULL, -> security
    "securityClass" varchar(2) DEFAULT NULL, -> security_class
    "radius" double DEFAULT NULL, -> radius
    "luminosity" double DEFAULT NULL, -> luminosity
    "border" integer DEFAULT NULL, -> is_border
    "fringe" integer DEFAULT NULL, -> is_fringe
    "corridor" integer DEFAULT NULL, -> is_corridor
    "hub" integer DEFAULT NULL, -> is_hub
    "international" integer DEFAULT NULL, -> is_international
    "regional" integer DEFAULT NULL, -> is_regional
    "constellation" integer DEFAULT NULL, -> is_constellation
    "x" double DEFAULT NULL, -> x
    "y" double DEFAULT NULL, -> y
    "z" double DEFAULT NULL, -> z
    "xMin" double DEFAULT NULL, -> x_min
    "yMin" double DEFAULT NULL, -> y_min
    "zMin" double DEFAULT NULL, -> z_min
    "xMax" double DEFAULT NULL, -> x_max
    "yMax" double DEFAULT NULL, -> y_max
    "zMax" double DEFAULT NULL, -> z_max
    
    not implemented:
    "sunTypeID" integer DEFAULT NULL,
    "factionID" integer DEFAULT NULL,
    """

    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)
    constellation = models.ForeignKey(Constellation)
    jumps = models.ManyToManyField('self')
    security = models.FloatField()
    security_class = models.CharField(max_length=2, null=True)
    radius = models.FloatField()
    luminosity = models.FloatField()
    is_border = models.BooleanField()
    is_fringe = models.BooleanField()
    is_corridor = models.BooleanField()
    is_hub = models.BooleanField()
    is_international = models.BooleanField()
    is_regional = models.BooleanField()
    is_constellation = models.BooleanField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    x_min = models.FloatField()
    y_min = models.FloatField()
    z_min = models.FloatField()
    x_max = models.FloatField()
    y_max = models.FloatField()
    z_max = models.FloatField()
    
    def __str__(self):
        return self.name

class MapDenormalize(models.Model):
    """ Equivalent of mapDenormalize
    
    "itemID" integer NOT NULL, -> pk
    "itemName" varchar(100) DEFAULT NULL, -> name
    "typeID" integer DEFAULT NULL, -> inv_type (ref InvType)
    "groupID" integer DEFAULT NULL, -> inv_group (ref InvGroup)
    "solarSystemID" integer DEFAULT NULL, -> solarsystem (ref SolarSystem)
    "constellationID" integer DEFAULT NULL, -> constellation (ref Constellation)
    "regionID" integer DEFAULT NULL, -> region (ref Region)
    "orbitID" integer DEFAULT NULL, -> orbit (ref self)
    "celestialIndex" integer DEFAULT NULL, -> celestial_index
    "orbitIndex" integer DEFAULT NULL, -> orbit_index
    "security" double DEFAULT NULL, -> security
    "radius" double DEFAULT NULL, -> radius
    "x" double DEFAULT NULL, -> x
    "y" double DEFAULT NULL, -> y
    "z" double DEFAULT NULL, -> z

    """
    
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=100)
    inv_type = models.ForeignKey(InvType)
    inv_group = models.ForeignKey(InvGroup)
    solarsystem = models.ForeignKey(SolarSystem)
    constellation = models.ForeignKey(Constellation)
    region = models.ForeignKey(Region)
    orbit = models.ForeignKey('self')
    celestial_index = models.IntegerField()
    orbit_index = models.IntegerField()
    security = models.FloatField(null=True)
    radius = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    
    def __str__(self):
        return self.name

#class StationType(models.Model):
#    """ Equivalent of staStationTypes
#    
#    "stationTypeID" integer NOT NULL,
#    "dockEntryX" double DEFAULT NULL,
#    "dockEntryY" double DEFAULT NULL,
#    "dockEntryZ" double DEFAULT NULL,
#    "dockOrientationX" double DEFAULT NULL,
#    "dockOrientationY" double DEFAULT NULL,
#    "dockOrientationZ" double DEFAULT NULL,
#    "operationID" integer DEFAULT NULL,
#    "officeSlots" integer DEFAULT NULL,
#    "reprocessingEfficiency" double DEFAULT NULL,
#    "conquerable" integer DEFAULT NULL,
#    
#    """
#    
#    name = models.CharField(max_length=100)
#    
#    def __str__(self):
#        return self.name

class Station(models.Model):
    """ Equivalent of staStations
    
    "stationID" integer NOT NULL, -> station_id (ref MapDenormalize)
    "stationName" varchar(100) DEFAULT NULL, -> name
    #"stationTypeID" integer DEFAULT NULL, -> station_type (ref StationType)
    "stationTypeID" integer DEFAULT NULL, -> station_type (ref InvType)
    "corporationID" integer DEFAULT NULL, -> corporation (ref Corporation)
    "solarSystemID" integer DEFAULT NULL, -> solarsystem (ref SolarSystem)
    "constellationID" integer DEFAULT NULL, -> constellation (ref Constellation)
    "regionID" integer DEFAULT NULL, -> region (ref Region)
    "security" integer DEFAULT NULL, -> security
    "maxShipVolumeDockable" double DEFAULT NULL, -> max_dock_volume
    "reprocessingEfficiency" double DEFAULT NULL, -> reprocessing_efficiency
    "reprocessingStationsTake" double DEFAULT NULL, -> reprocessing_take
    "x" double DEFAULT NULL, -> x
    "y" double DEFAULT NULL, -> y
    "z" double DEFAULT NULL, -> z
    
    not implemented:
    "dockingCostPerVolume" double DEFAULT NULL,
    "officeRentalCost" integer DEFAULT NULL,
    "operationID" integer DEFAULT NULL,
    "reprocessingHangarFlag" integer DEFAULT NULL,
    
    """
    
    station_id = models.ForeignKey(MapDenormalize, primary_key=True,
                                   db_column='station_id')
    name = models.CharField(max_length=100)
    #station_type = models.ForeignKey(StationType)
    station_type = models.ForeignKey(InvType)
    corporation = models.ForeignKey(NPCCorporation)
    solarsystem = models.ForeignKey(SolarSystem)
    constellation = models.ForeignKey(Constellation)
    region = models.ForeignKey(Region)
    security = models.FloatField()
    max_dock_volume = models.FloatField()
    reprocessing_efficiency = models.FloatField()
    reprocessing_take = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    
    def __str__(self):
        return self.name
    
    def type_name(self):
        try:
            return self._type_name
        except AttributeError:
            self._type_name = InvTypes.objects.get(pk=self.pk).name
            return self._type_name