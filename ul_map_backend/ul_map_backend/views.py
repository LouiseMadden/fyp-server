#entry point for frontend and database (could put in other file)
#restframework
#serachview inside use create http function - don't use get use push
#would also need roomsearchview and directionsview

from rest_framework import response
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from ul_map_backend import models, settings
from django.db.models import Q
from django.core import exceptions
from collections import OrderedDict

import requests


def _init_building_codes():
    building_codes = OrderedDict()
    building_codes['AD'] = 'Analog Devices'
    building_codes['A'] = 'Main Building, Block A'
    building_codes['B'] = 'Main Building, Block B'
    building_codes['CS'] = 'Computer Science'
    building_codes['C'] = 'Main Building, Block C'
    building_codes['D'] = 'Main Building, Block D'
    building_codes['ER'] = 'Engineering Research'
    building_codes['E'] = 'Main Building, Block E'
    building_codes['F'] = 'Foundation Building'
    building_codes['GEMS'] = 'Graduate Entry Medical School'
    building_codes['HS'] = 'Health Sciences'
    building_codes['IB'] = 'International Business Centre'
    building_codes['KB'] = 'Kemmy Business School'
    building_codes['LC'] = 'Languages Building'
    building_codes['L'] = 'Lonsdale'
    building_codes['MC'] = 'Millstream'
    building_codes['P'] = 'PESS'
    building_codes['SR'] = 'Schrodinger'
    building_codes['S'] = 'Schumann'
    building_codes['T'] = 'Tierney Building'
    return building_codes


BUILDING_CODES = _init_building_codes()


class RoomSearchViewset(ViewSet):
    def list(self, request):

        code = request.query_params['code']

        resp = {}
        for key, value in BUILDING_CODES.items():
            if key in code:
                resp['building'] = value
                resp['floor'] = code[len(key):len(key) + 1]
                resp['room'] = code[len(key) + 1:]
                return Response(resp)

        resp['error'] = 'Building not Found'
        return Response(resp)

 


class SearchViewset(ViewSet):

    def list(self, request):
        query_params = request.query_params
        name = query_params["name"]
        resp = nameLookup(name)

        return Response(resp)


class DirectionViewset(ViewSet):

    def list(self,request):
        query_params = request.query_params
        start_name = query_params["start"]
        end_name = query_params["end"]

        # Call nameLookup for both to use for directions
        start_coords = nameLookup(start_name)
        end_coords = nameLookup(end_name)
        
        start_coords = validateCoords(start_coords)
        end_coords = validateCoords(end_coords)

        start = f"{start_coords['latitude']},{start_coords['longitude']}"
        end = f"{end_coords['latitude']},{end_coords['longitude']}"

        url = f'http://router.project-osrm.org/route/v1/foot/{start};{end}'
        resp = requests.get(url)

        breakpoint()
        return resp

def nameLookup(name):
    try:
        location = models.Location.objects.get(
            Q(name_1__contains=name) | 
            Q(name_2__contains=name) |
            Q(name_3__contains=name)
        )
    except models.Location.DoesNotExist:
        return {
            "error": "Location not found"
        }
    else:
        return {
            "latitude": location.door_1.latitude,
            "longitude": location.door_1.longitude
        }

def validateCoords(coords):
    try:
        latitude = coords['latitude']
        longitude = coords['longitude']
    except KeyError:
        raise exceptions.FieldError()
    else:
        return coords

