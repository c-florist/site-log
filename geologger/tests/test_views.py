from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework.test import APITestCase

from geologger.models import JobSite, SiteVisitLog, Technician


class TechnicianLocationPingViewTestCase(APITestCase):
    def setUp(self):
        self.technician = Technician.objects.create(name="Test Technician")
        self.job_site = JobSite.objects.create(
            name="Test Site",
            address="123 Test St",
            location=Point(0, 0),
            radius_meters=100,
        )
        self.url = reverse(
            "technician-ping", kwargs={"technician_id": self.technician.id}
        )

    def test_invalid_request_data(self):
        """Test that the view returns a 400 if the request data is not a dict."""
        response = self.client.post(self.url, data="invalid", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_missing_coordinates(self):
        """Test that the view returns a 400 if latitude or longitude are missing."""
        response = self.client.post(self.url, data={}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_arrival_logged(self):
        """Test that an arrival is logged when a technician enters a job site."""
        response = self.client.post(
            self.url,
            data={"latitude": 0.0001, "longitude": 0.0001},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Arrival logged")
        self.assertEqual(SiteVisitLog.objects.count(), 1)

    def test_still_on_site(self):
        """Test that the view returns 'Still on site' if the technician is already at the site."""
        SiteVisitLog.objects.create(
            technician=self.technician,
            job_site=self.job_site,
        )
        response = self.client.post(
            self.url,
            data={"latitude": 0.0001, "longitude": 0.0001},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Still on site")
        self.assertEqual(SiteVisitLog.objects.count(), 1)

    def test_departure_logged(self):
        """Test that a departure is logged when a technician leaves a job site."""
        SiteVisitLog.objects.create(
            technician=self.technician,
            job_site=self.job_site,
        )
        response = self.client.post(
            self.url,
            data={"latitude": 1, "longitude": 1},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Departure logged")
        self.assertIsNotNone(SiteVisitLog.objects.first().departure_time)

    def test_no_site_in_range(self):
        """Test that the view returns a 204 if the technician is not near any site."""
        response = self.client.post(
            self.url,
            data={"latitude": 1, "longitude": 1},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)
