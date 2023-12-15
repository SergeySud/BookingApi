# filters.py
import django_filters
from django_filters import rest_framework as filters

from .models import Room, Reservation


class RoomFilter(django_filters.FilterSet):
    guests_number = django_filters.NumberFilter(field_name='guests_number', lookup_expr='gte')
    price_per_day = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')

    class Meta:
        model = Room
        fields = ['guests_number', 'price_per_day']


class ReservationFilter(filters.FilterSet):
    class Meta:
        model = Reservation
        fields = ['id', 'room', 'reservation_start_date', 'reservation_end_date']
