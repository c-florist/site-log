from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import JobSite, Technician, SiteVisitLog

@admin.register(JobSite)
class JobSiteAdmin(LeafletGeoAdmin):
    list_display = ("name", "address", "radius_meters")
    fields = ("name", "address", "radius_meters", "location")
    leaflet_is_editable = False

admin.site.register(Technician)
admin.site.register(SiteVisitLog)
