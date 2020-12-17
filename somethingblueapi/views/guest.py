from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from somethingblueapi.models import Bride, Wedding, Guest


class Guests(ViewSet):
    def create(self, request):
        """Handle POST requests for guests"""
        bride = Bride.objects.get(user=request.auth.user)
        wedding = Wedding.objects.get(bride=bride)

        guest = Guest()

        guest.wedding = wedding
        guest.guest_first_name = request.data["guest_first_name"]
        guest.guest_last_name = request.data["guest_last_name"]
        guest.address = request.data["address"]
        guest.phone_number = request.data["phone_number"]
        guest.number_of_guests_in_party = request.data["number_of_guests_in_party"]
        guest.rsvp_status = request.data["rsvp_status"]

        try:
            guest.save()
            serializer = GuestSerializer(guest, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single guest"""
        try:
            guest = Guest.objects.get(pk=pk)
            serializer = GuestSerializer(guest, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all Guests for a wedding"""

        bride = Bride.objects.get(user=request.auth.user)
        wedding = Wedding.objects.get(bride=bride)

        guests = Guest.objects.filter(wedding=wedding)

        serializer = GuestSerializer(
            guests, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single guest"""
        try:
            guest = Guest.objects.get(pk=pk)
            guest.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Guest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for guests"""

        guest = Guest.objects.get(pk=pk)
        guest.guest_first_name = request.data["guest_first_name"]
        guest.guest_last_name = request.data["guest_last_name"]
        guest.address = request.data["address"]
        guest.phone_number = request.data["phone_number"]
        guest.number_of_guests_in_party = request.data["number_of_guests_in_party"]
        guest.rsvp_status = request.data["rsvp_status"]
        guest.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'wedding', 'guest_first_name', 'guest_last_name', 'address', 'phone_number', 'number_of_guests_in_party', 'rsvp_status')