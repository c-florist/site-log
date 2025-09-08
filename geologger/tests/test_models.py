from unittest.mock import patch

from django.contrib.gis.geos import Point
from django.test import TestCase

from geologger.models import JobSite


class JobSiteTestCase(TestCase):
    @patch("geologger.models.geocode_address")
    def test_save_geocodes_address(self, mock_geocode_address):
        """Test that the save method geocodes the address if no location is present."""
        mock_geocode_address.return_value = Point(1, 1)
        site = JobSite.objects.create(
            name="Test Site",
            address="123 Test St",
        )
        self.assertEqual(site.location.x, 1)
        self.assertEqual(site.location.y, 1)
        mock_geocode_address.assert_called_once_with("123 Test St")

    @patch("geologger.models.geocode_address")
    def test_save_does_not_geocode_if_location_exists(self, mock_geocode_address):
        """Test that the save method does not geocode if a location is already present."""
        JobSite.objects.create(
            name="Test Site",
            address="123 Test St",
            location=Point(2, 2),
        )
        mock_geocode_address.assert_not_called()
