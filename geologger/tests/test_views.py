from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework.test import APITestCase

from geologger.models import JobSite, Technician


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
