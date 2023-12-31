from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from booking.filters import RoomFilter, ReservationFilter
from booking.models import Room, Reservation
from booking.serializers import RoomSerializer, ReservationSerializer


@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
class RoomFilterView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['pricer_per_day', 'guests_number']
    filterset_class = RoomFilter


class ReservationView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter

    def create(self, request, *args, **kwargs):
        room_id = request.data.get('room')
        reservation_start_date = request.data.get('reservation_start_date')
        reservation_end_date = request.data.get('reservation_end_date')
        user = request.user

        if not room_id or not reservation_start_date or not reservation_end_date:
            return Response({'error': "'room,' 'reservation_start_date', and 'reservation_end_date' are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

        if reservation_start_date >= reservation_end_date:
            return Response({'error': 'End date must be after start date'},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_reservations = Reservation.objects.filter(
            room=room,
            reservation_end_date__gt=reservation_start_date,
            reservation_start_date__lt=reservation_end_date
        )
        if existing_reservations.exists():
            return Response({'error': 'Room is not available for the specified dates'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reserved_by_user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        reservation_id = request.data.get('id', None)
        if reservation_id is not None:
            reservations = Reservation.objects.filter(id=reservation_id)
            if reservations.exists():
                reservation = reservations.first()
                if request.user == reservation.reserved_by_user or request.user.is_staff:
                    reservation.delete()
                    return Response({'detail': 'Reservation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                return Response({'error': 'No access'}, status=status.HTTP_403_FORBIDDEN)

            return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)
