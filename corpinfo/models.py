from django.db import models

from django.contrib.auth.models import User

from eve.util import *

from eveapi.models import APIKey
from evestatic.models import Station

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
            volume = float(row.get('volume'))
            issuer_id = int(row.get('issuerID'))
            issuer_result = self.apikey.query('eve/CharacterName', {'ids': issuer_id})
            issuer = issuer_result.rowset.row.get('name')
            contract = Contract(contract_id, contract_type,
                                start_station, end_station,
                                volume, issuer)
            contracts.append(contract)

        return contracts

    def _get_api_result(self, query, args={}):
        return self.apikey.query(query, merge_dict({'corporationID': self.pk},
                                                   args))

class Contract(object):
    def __init__(self, contract_id, contract_type,
                 start_station_id, end_station_id,
                 volume, issuer):
        self.contract_id = contract_id
        self.contract_type = contract_type
        self.start_station = Station.objects.get(pk=start_station_id)
        self.end_station = Station.objects.get(pk=end_station_id)
        self.volume = volume
        self.issuer = issuer

    def __str__(self):
        return "{0} [{1}m³] {2} -> {3} by {4}".format(
                                                   self.contract_type,
                                                   self.volume,
                                                   self.start_station.solarsystem.name,
                                                   self.end_station.solarsystem.name,
                                                   self.issuer,
                                               )
