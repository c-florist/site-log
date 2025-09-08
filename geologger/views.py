from logging import getLogger
from django.db.models import F
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from geologger.models import JobSite, SiteVisitLog, Technician

logger = getLogger(__name__)

class TechnicianLocationPingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, technician_id: int) -> Response:
        lat = request.data.get("latitude")
        lon = request.data.get("longitude")
        if not lat or not lon:
            return Response({"error": "Missing latitude or longitude"}, status=400)

        technician = Technician.objects.get(id=technician_id)
        current_location = Point(float(lon), float(lat), srid=4326)

        technician.last_location = current_location
        technician.save()

        site_in_range = JobSite.objects.annotate(
            distance=Distance("location", current_location)
        ).filter(distance__lte=F("radius_meters")).order_by("distance").first()

        open_visit = SiteVisitLog.objects.filter(
            technician=technician,
            departure_time__isnull=True
        ).first()

        if site_in_range:
            if open_visit and open_visit.job_site == site_in_range:
                logger.info(f"Technician {technician.name} still on site at {site_in_range.name}")
                return Response({"message": "Still on site"}, status=200)
            elif not open_visit:
                logger.info(f"Technician {technician.name} arrived at {site_in_range.name}")
                _ = SiteVisitLog.objects.create(
                    technician=technician,
                    job_site=site_in_range,
                    arrival_time=timezone.now()
                )
                return Response({"message": "Arrival logged"}, status=200)
        else:
            if open_visit:
                open_visit.departure_time = timezone.now()
                open_visit.save()

                return Response({"message": "Departure logged"}, status=200)

        return Response(status=204)
