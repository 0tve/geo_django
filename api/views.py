from django import shortcuts
from django.contrib.auth import models as auth_models
from rest_framework import generics, permissions, response, status
from rest_framework.authtoken import models as token_models

from . import filters, models, serializers


class RegisterView(generics.CreateAPIView):
    queryset = auth_models.User.objects.all()
    serializer_class = serializers.RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = token_models.Token.objects.create(user=user)
        return response.Response({'token': token.key}, status=status.HTTP_201_CREATED)


class PointCreateView(generics.CreateAPIView):
    queryset = models.Point.objects.all()
    serializer_class = serializers.PointSerializer
    permission_classes = [permissions.IsAuthenticated]


class PointListView(generics.ListAPIView):
    queryset = models.Point.objects.all()
    serializer_class = serializers.PointSerializer
    filter_backends = [filters.GeoDistanceFilter]
    geo_filter_field = 'location'


class MessageCreateView(generics.CreateAPIView):
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Message.objects.filter(point_id=self.kwargs['point_id'])

    def perform_create(self, serializer):
        point = shortcuts.get_object_or_404(
            models.Point, id=self.kwargs['point_id'])
        serializer.save(point=point)


class MessageListView(generics.ListAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    filter_backends = [filters.GeoDistanceFilter]
    geo_filter_field = 'point__location'
