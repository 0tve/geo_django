from django.contrib.gis import geos, measure
from rest_framework import filters

from . import serializers


class GeoDistanceFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        serializer = serializers.GeoParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        point = geos.Point(data['longitude'], data['latitude'], srid=4326)
        lookup_field = getattr(view, 'geo_filter_field', 'location')
        return queryset.filter(**{f"{lookup_field}__distance_lte": (point, measure.Distance(km=data['radius']))})
