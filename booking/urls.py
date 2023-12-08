from django.urls import path

from booking.views import RoomFilterView, ReservationView

app_name = 'booking'

urlpatterns = [
    path('rooms/', RoomFilterView.as_view(), name='room-list'),
    path('reservations/', ReservationView.as_view(), name='reservation-create'),
    # Add other URL patterns as needed
]
