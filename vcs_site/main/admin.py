from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Event)
admin.site.register(VideoConf)
admin.site.register(ReservedRoom)
admin.site.register(Organization)
admin.site.register(Room)
admin.site.register(Application)
admin.site.register(Staffer)