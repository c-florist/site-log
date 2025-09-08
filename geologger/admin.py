from django.contrib import admin
from django.contrib.admin import ModelAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import JobSite, Technician, SiteVisitLog

@admin.register(JobSite)
class JobSiteAdmin(LeafletGeoAdmin):
    list_display = ("name", "address", "radius_meters")
    fields = ("name", "address", "radius_meters", "location")
    leaflet_is_editable = False


@admin.register(SiteVisitLog)
class SiteVisitLogAdmin(ModelAdmin[SiteVisitLog]):
    list_display = ("technician", "job_site", "arrival_time", "departure_time")
    fields = ("technician", "job_site", "arrival_time", "departure_time")
    readonly_fields = ("technician", "job_site", "arrival_time", "departure_time")


admin.site.register(Technician)
