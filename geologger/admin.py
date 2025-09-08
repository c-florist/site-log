from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import JobSite, Technician, SiteVisitLog

admin.site.register(JobSite, LeafletGeoAdmin)
admin.site.register(Technician)
admin.site.register(SiteVisitLog, LeafletGeoAdmin)
