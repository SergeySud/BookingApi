from rest_framework import serializers

from booking.models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'price_per_day', 'guests_number']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'room', 'reservation_start_date', 'reservation_end_date', 'reserved_by_user']
