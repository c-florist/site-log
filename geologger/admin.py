from django.contrib.admin import register, ModelAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import JobSite, Technician, SiteVisitLog


@register(JobSite)
class JobSiteAdmin(LeafletGeoAdmin):
    list_display = ("name", "address", "location", "radius_m")


@register(Technician)
class TechnicianAdmin(ModelAdmin):
    list_display = ("name",)


@register(SiteVisitLog)
class SiteVisitLogAdmin(ModelAdmin):
    list_display = ("technician", "job_site", "arrival_time", "departure_time", "duration")
    list_filter = ("job_site", "technician")
