from time import strptime, mktime
from http.client import HTTPSConnection
from lxml import objectify

from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone

class ApiError(Exception):
    def __init__(self, message):
        self._message = message
    
    def __str__(self):
        strval = "An error occured while querying the EVE Online API"
        if len(self._message) > 0:
            strval += ": " + self._message
        return strval

class APIKey(models.Model):
    user = models.ForeignKey(User)
    vcode = models.CharField(max_length=64)
    comment = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.pk) + " " + self.comment
    
    def query(self, query, args):
        queryString = self._make_query_string(query, args)
        resultObject = cache.get(queryString)
        # if query is cached, return cached value
        if resultObject is not None:
            return resultObject.result
        
        # otheriwse query EVE api, write to cache and return result
        con = HTTPSConnection("api.eveonline.com")
        con.request("GET", queryString)
        response = con.getresponse()
        if response.status != 200:
            raise ApiError()
        resultObject = objectify.fromstring(response.read())
        
        # get number of seconds to cache the result and write to cache
        cachedUntilTimestamp = mktime(strptime(resultObject.cachedUntil + " UTC", "%Y-%m-%d %H:%M:%S %Z"))
        nowTimestamp = mktime(timezone.now().timetuple())
        cacheSeconds = cachedUntilTimestamp - nowTimestamp
        cache.set(queryString, resultObject, cacheSeconds)
        
        return resultObject.result
    
    def _make_query_string(self, query, args):
        if not query.startswith('/'):
            query = '/' + query
        if not query.endswith(".xml.aspx"):
            query += ".xml.aspx"
        args['keyID'] = self.pk
        args['vCode'] = self.vcode
        return "?".join([query, "&".join(["=".join(map(str, i)) for i in args.items()])])