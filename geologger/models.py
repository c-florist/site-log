from datetime import datetime

from django.utils import timezone
from django.contrib.gis.db.models import PointField
from django.db.models import DateTimeField, ForeignKey, Model, TextField, PositiveIntegerField, CASCADE

from geologger.geocode import geocode_address


class JobSite(Model):
    name = TextField(unique=True)
    address = TextField()
    location = PointField()
    radius_meters = PositiveIntegerField(default=50, help_text="Radius of the geofence for this job site in meters.")

    def save(self, *args, **kwargs) -> None:
        if self.address and not self.location:
            self.location = geocode_address(self.address)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Technician(Model):
    name = TextField()
    last_location = PointField(null=True, blank=True, editable=False)

    def __str__(self) -> str:
        return self.name


class SiteVisitLog(Model):
    technician = ForeignKey(Technician, on_delete=CASCADE)
    job_site = ForeignKey(JobSite, on_delete=CASCADE)
    arrival_time = DateTimeField(auto_now_add=True)
    departure_time = DateTimeField(null=True, blank=True)

    @property
    def duration(self) -> datetime:
        if self.departure_time:
            return self.departure_time - self.arrival_time

        return timezone.now() - self.arrival_time

    def __str__(self) -> str:
        return f"{self.technician.name} at {self.job_site.name}"
