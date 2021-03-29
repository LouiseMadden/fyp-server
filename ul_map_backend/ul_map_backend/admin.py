from django.contrib import admin

from ul_map_backend import models

admin.site.register([models.Location, models.Door])