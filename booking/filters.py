# filters.py
import django_filters
from django.db.models import Q

from .models import Room, Reservation


class RoomFilter(django_filters.FilterSet):
    guests_number = django_filters.NumberFilter(field_name='guests_number', lookup_expr='gte')
    price_per_day = django_filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')
    reservation_start_date = django_filters.DateFilter(field_name='reservation_start_date',
                                                       method='filter_by_availability', lookup_expr="gte")
    reservation_end_date = django_filters.DateFilter(field_name='reservation_end_date', method='filter_by_availability',
                                                     lookup_expr="gte")

    class Meta:
        model = Room
        fields = []

    def filter_by_availability(self, queryset, name, value):
        reservations = Reservation.objects.filter(
            Q(reservation_start_date__lte=value, reservation_end_date__gte=value) |
            Q(reservation_start_date__lte=self.data["reservation_end_date"],
              reservation_end_date__gte=self.data["reservation_start_date"])
        )
        booked_room_ids = reservations.values_list("room", flat=True)
        return queryset.exclude(id__in=booked_room_ids)


class ReservationFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name="user", method="filter_reserved_by_user", required=True)

    class Meta:
        model = Reservation
        fields = []

    def filter_reserved_by_user(self, queryset, name, value):
        return queryset.filter(reserved_by_user=self.request.user)
