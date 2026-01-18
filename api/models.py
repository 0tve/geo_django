from django.contrib.gis.db import models


class Point(models.Model):
    location = models.PointField()


class Message(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    text = models.TextField()
