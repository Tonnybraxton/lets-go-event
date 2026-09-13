from django.urls import path

from . import views


app_name = "events"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("events/", views.event_list, name="event-list"),
    path("events/drafts/", views.create_event_draft, name="event-draft-create"),
    path("orders/", views.create_order, name="order-create"),
    path("scanner/scan/", views.scan_ticket, name="scanner-scan"),
    path("events/<slug:slug>/", views.event_detail, name="event-detail"),
]
