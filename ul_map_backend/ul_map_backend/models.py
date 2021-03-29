from django.db import models


class Door(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    accessible = models.BooleanField()

class Location(models.Model):
    name_1 = models.CharField(max_length=50, null=True, blank=True)
    name_2 = models.CharField(max_length=50, null=True, blank=True)
    name_3 = models.CharField(max_length=50, null=True, blank=True)

    door_1 = models.ForeignKey(
        Door, on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )
    door_2 = models.ForeignKey(
        Door, on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )
    door_3 = models.ForeignKey(
        Door, on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )
    door_4 = models.ForeignKey(
        Door, on_delete=models.CASCADE, related_name='+', null=True, blank=True
    )

    tag = models.CharField(max_length=50)
