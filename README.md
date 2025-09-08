# site-log

Geofenced time-on-site logger.

A short spike to test out how this feature might work in a real world scenario. A client (likely a lightweight daemon process on a mobile device or similar) would call the location ping endpoint periodically to verify the user's location and automatically log site visits.

Another way this could work that may be more palatable for some users is to have the client show an on-screen notification when the user enters or exits a geofence, styled as a reminder to log the site visit instead of an automatic tracker.

What this doesn't cover:
* Verifying accurate geofence bounds and accurate/relevant location request data, i.e. is the user pinging within Australia
* The client that calls the location ping endpoint to log site visits
* Network connectivity drop outs and packet loss

## Getting started

### Prerequisites

* Python 3.12+
* [GEOS, GDAL, and SpatiaLite installed](https://docs.djangoproject.com/en/5.2/ref/contrib/gis/tutorial/#setting-up).

### Setup

Clone the repo, then:

```shell
# Create the virtual environment and install dependencies
uv sync

# Activate the venv
source .venv/bin/activate

# Run the database migrations and create a super user
python manage.py migrate
python manage.py createsuperuser

# Start the dev server
python manage.py runserver
```

Access the admin interface at http://127.0.0.1:8000/admin/ to create job sites and technicians.

Run a demo using a dummy test client:
```shell
python demo.py
```
