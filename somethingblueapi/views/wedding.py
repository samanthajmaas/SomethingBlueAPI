from django.http.response import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import uuid
import base64
from django.core.files.base import ContentFile
from somethingblueapi.models import Bride, Wedding
from somethingblueapi.views.bride import BrideSerializer
from datetime import datetime, date



class Weddings(ViewSet):
    def create(self, request):
        """Handle POST operations for weddings"""

        bride = Bride.objects.get(user=request.auth.user)

        wedding = Wedding()

        wedding.bride = bride
        wedding.event_date = request.data["event_date"]
        wedding.location = request.data["location"]
        wedding.budget = request.data["budget"]

        try:
            wedding.save()
            serializer = WeddingSerializer(wedding, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET request for single wedding"""
        try:
            wedding = Wedding.objects.get(pk=pk)
            serializer = WeddingSerializer(wedding, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for weddings"""

        bride = Bride.objects.get(user=request.auth.user)

        wedding = Wedding.objects.get(pk=pk)
        wedding.event_date = request.data["event_date"]
        wedding.location = request.data["location"]
        wedding.budget = request.data["budget"]
        wedding.bride = bride

        wedding.save()

        serializer = WeddingSerializer(wedding, context={'request': request})
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a wedding"""
        try:
            wedding = Wedding.objects.get(pk=pk)
            wedding.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Wedding.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def current_brides_wedding(self, request):

        bride = Bride.objects.get(user=request.auth.user)
        current_wedding = Wedding.objects.get(bride=bride)
        wedding_date = current_wedding.event_date

        countdown = (wedding_date - date.today())/60/60/24
        current_wedding.countdown = countdown.seconds

        serializer = WeddingSerializer(current_wedding, context={'request': request})

        return Response(serializer.data)

"""Basic Serializer for wedding"""
class WeddingSerializer(serializers.ModelSerializer):
    bride = BrideSerializer(many=False)

    class Meta:
        model = Wedding
        fields = ('id', 'bride', 'event_date', 'location', 'budget', 'countdown')
        depth = 1