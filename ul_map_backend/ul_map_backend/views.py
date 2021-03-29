#entry point for frontend and database (could put in other file)
#restframework
#serachview inside use create http function - don't use get use push
#would also need roomsearchview and directionsview

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from ul_map_backend import models, settings
from django.db.models import Q
from django.core import exceptions
import requests


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

