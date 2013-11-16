from django.db import models

from django.contrib.auth.models import User

from eve.util import *

from eveapi.models import APIKey

class Corporation(models.Model):
    corporation_id = models.IntegerField(primary_key=True)
    apikey = models.ForeignKey(APIKey)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)

    def contracts(self):
        """Get corp contract list."""
        rows = self._get_api_result('corp/Contracts').rowset
        contracts = []
        for row in rows.iterchildren():
            contract_state = row.get('status')
            if contract_state != 'Outstanding':
                continue

            contract_id = int(row.get('contractID'))
            contract_type = row.get('type')
            start_station = int(row.get('startStationID'))
            end_station = int(row.get('endStationID'))
            contracts.append(Contract(contract_id, contract_type,
                                      start_station, end_station))

        return contracts

    def _get_api_result(self, query, args={}):
        return self.apikey.query(query, merge_dict({'corporationID': self.pk},
                                                   args))

class Contract(object):
    def __init__(self, contract_id, contract_type, start_station, end_station):
        self.contract_id = contract_id
        self.contract_type = contract_type
        self.start_station = start_station
        self.end_station = end_station

    def __str__(self):
        return "{0} {1} -> {2}".format(self.contract_type, self.start_station, self.end_station)
