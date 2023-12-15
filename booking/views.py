from django.db.models import Q
from rest_framework import status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import Room, Reservation
from booking.serializers import RoomSerializer, ReservationSerializer


class RoomList(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        price_per_day = self.request.data.get('price_per_day', None)
        queryset = Room.objects.all()

        if price_per_day is not None:
            queryset = queryset.filter(price_per_day=price_per_day)

        return queryset


@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
class RoomFilterView(APIView):
    def get(self, request, *args, **kwargs):
        price_per_day = request.data.get('price_per_day', None)
        guests_number = request.data.get('guests_number', None)
        sort_by = request.data.get('sort_by', None)
        start_date = self.request.data.get('reservation_start_date', None)
        end_date = self.request.data.get('reservation_end_date', None)

        filter_kwargs = {}
        if price_per_day is not None:
            filter_kwargs['price_per_day'] = price_per_day
        if guests_number is not None:
            filter_kwargs['guests_number'] = guests_number

        rooms = Room.objects.filter(**filter_kwargs)

        if start_date and end_date:
            rooms = rooms.filter(
                ~Q(reservation__reservation_start_date__lte=end_date,
                   reservation__reservation_end_date__gte=start_date)
            )

            if sort_by is not None:
                rooms = rooms.order_by(sort_by)

        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = {'reserved_by_user': request.user.id}
        reservations = Reservation.objects.filter(**user_id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        room_id = request.data.get('room')
        start_date = request.data.get('reservation_start_date')
        end_date = request.data.get('reservation_end_date')

        conflicting_reservations = Reservation.objects.filter(
            room=room_id,
            reservation_start_date__lte=end_date,
            reservation_end_date__gte=start_date
        )

        if conflicting_reservations.exists():
            return Response({"error": "Room is already reserved for the specified time period."},
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        request.data['reserved_by_user'] = user_id
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        reservation_id = request.data.get('id', None)
        if reservation_id is not None:
            reservations = Reservation.objects.filter(id=reservation_id)
            if reservations.exists():
                reservation = reservations.first()
                user = request.user
                if reservation.reserved_by_user == user or user.is_staff is True:
                    reservation.delete()
                    return Response({"detail": "Reservation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No such reservation found. Check reservation ID and authentication."},
                        status=status.HTTP_400_BAD_REQUEST)
