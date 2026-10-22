from django.urls import path

from . import views


app_name = "events"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("events/", views.event_list, name="event-list"),
    path("events/drafts/", views.create_event_draft, name="event-draft-create"),
    path("location-suggestions/", views.create_location_suggestion, name="location-suggestion-create"),
    path("orders/", views.create_order, name="order-create"),
    path("orders/<str:reference>/", views.order_status, name="order-status"),
    path("payments/mpesa/callback/", views.mpesa_callback, name="mpesa-callback"),
    path("scanner/scan/", views.scan_ticket, name="scanner-scan"),
    path("events/<slug:slug>/", views.event_detail, name="event-detail"),
]

