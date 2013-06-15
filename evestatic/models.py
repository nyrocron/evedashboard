from django.db import models


class InvCategory(models.Model):
    
    """ Equivalent of invCategories

    "categoryID" integer NOT NULL, -> pk
    "categoryName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(3000) DEFAULT NULL, -> description
    "published" integer DEFAULT NULL, -> published
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=3000)
    published = models.BooleanField()
    
    def __str__(self):
        return self.name

class InvGroup(models.Model):
    
    """ Equivalent of invGroups
    
    "groupID" integer NOT NULL, -> pk
    "categoryID" integer DEFAULT NULL, -> invcategory
    "groupName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(3000) DEFAULT NULL, -> description
    "useBasePrice" integer DEFAULT NULL, -> use_baseprice
    "allowManufacture" integer DEFAULT NULL, -> allow_manufacture
    "allowRecycler" integer DEFAULT NULL, -> allow_recycler
    "anchored" integer DEFAULT NULL, -> anchored
    "anchorable" integer DEFAULT NULL, -> anchorable
    "fittableNonSingleton" integer DEFAULT NULL, -> fittable_non_singleton
    "published" integer DEFAULT NULL, -> published
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """
    
    name = models.CharField(max_length=100)
    invcategory = models.ForeignKey(InvCategory)
    description = models.CharField(max_length=3000)
    use_baseprice = models.BooleanField()
    allow_manufacture = models.BooleanField()
    allow_recycler = models.BooleanField()
    anchored = models.BooleanField()
    anchorable = models.BooleanField()
    fittable_non_singleton = models.BooleanField()
    published = models.BooleanField()
    
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
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)
    description = models.CharField(max_length=3000)
    has_types = models.BooleanField()
    
    def __str__(self):
        return self.name

class Race(models.Model):
    """ Equivalent of chrRaces
    
    "raceID" integer NOT NULL, -> pk
    "raceName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(1000) DEFAULT NULL, -> description
    "shortDescription" varchar(500) DEFAULT NULL, -> description_short
    
    not implemented:
    "iconID" integer DEFAULT NULL,
    
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    description_short = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

class InvType(models.Model):
    """ Equivalent of invTypes
    
    "typeID" integer NOT NULL, -> pk
    "groupID" integer DEFAULT NULL, -> invgroup
    "typeName" varchar(100) DEFAULT NULL, -> name
    "description" varchar(3000) DEFAULT NULL, -> description
    "mass" double DEFAULT NULL, -> mass
    "volume" double DEFAULT NULL, -> volume
    "capacity" double DEFAULT NULL, -> capacity
    "portionSize" integer DEFAULT NULL, -> portion_size
    "raceID" integer DEFAULT NULL, -> race
    "basePrice" decimal(19,4) DEFAULT NULL, -> baseprice
    "published" integer DEFAULT NULL, -> published
    "marketGroupID" integer DEFAULT NULL, -> marketgroup
    
    not implemented:
    "chanceOfDuplicating" double DEFAULT NULL,
    
    """

    name = models.CharField(max_length=100)
    invgroup = models.ForeignKey(InvGroup)
    marketgroup = models.ForeignKey(MarketGroup, null=True)
    description = models.CharField(max_length=3000)
    mass = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    capacity = models.FloatField(null=True)
    portion_size = models.IntegerField(null=True)
    race = models.ForeignKey(Race, null=True)
    baseprice = models.DecimalField(max_digits=19, decimal_places=4)
    published = models.BooleanField()
    
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)
    # TODO

class Constellation(models.Model):
    name = models.CharField(max_length=100)
    # TODO

class SolarSystem(models.Model):
    """ Equivalent of mapSolarSystems
    
    "regionID" integer DEFAULT NULL, -> region
    "constellationID" integer DEFAULT NULL, -> constellation
    "solarSystemID" integer NOT NULL, -> pk
    "solarSystemName" varchar(100) DEFAULT NULL, -> name
    "x" double DEFAULT NULL, -> x
    "y" double DEFAULT NULL, -> y
    "z" double DEFAULT NULL, -> z
    "xMin" double DEFAULT NULL, -> x_min
    "xMax" double DEFAULT NULL, -> x_max
    "yMin" double DEFAULT NULL, -> y_min
    "yMax" double DEFAULT NULL, -> y_max
    "zMin" double DEFAULT NULL, -> z_min
    "zMax" double DEFAULT NULL, -> z_max
    "luminosity" double DEFAULT NULL, -> luminosity
    "border" integer DEFAULT NULL, -> border
    "fringe" integer DEFAULT NULL, -> fringe
    "corridor" integer DEFAULT NULL, -> corridor
    "hub" integer DEFAULT NULL, -> hub
    "international" integer DEFAULT NULL, -> international
    "regional" integer DEFAULT NULL, -> regional
    "constellation" integer DEFAULT NULL, -> constellation
    "security" double DEFAULT NULL, -> security
    "securityClass" varchar(2) DEFAULT NULL, -> security_class
    "radius" double DEFAULT NULL, -> radius
    
    not implemented:
    "sunTypeID" integer DEFAULT NULL,
    "factionID" integer DEFAULT NULL,
    """

    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)
    constellation = models.ForeignKey(Constellation)
    security = models.FloatField()
    security_class = models.CharField(max_length=2)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    x_min = models.FloatField()
    y_min = models.FloatField()
    z_min = models.FloatField()
    x_max = models.FloatField()
    y_max = models.FloatField()
    z_max = models.FloatField()
    radius = models.FloatField()
    luminosity = models.BooleanField()
    border = models.BooleanField()
    fringe = models.BooleanField()
    corridor = models.BooleanField()
    hub = models.BooleanField()
    international = models.BooleanField()
    regional = models.BooleanField()
    constellation = models.BooleanField()