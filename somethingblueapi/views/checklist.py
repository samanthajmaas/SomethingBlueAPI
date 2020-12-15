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
from somethingblueapi.models import Wedding, ChecklistItem, WeddingChecklist, Bride
from somethingblueapi.views.wedding import WeddingSerializer

class Checklists(ViewSet):
    def create(self, request):
        """Handle POST operations for check list items for a wedding"""
        item = ChecklistItem()
        item.toDo = request.data["toDo"]
        item.default= False
        try:
            item.save()
            serializer = ChecklistItemSerializer(item, context={'request': request})

            bride = Bride.objects.get(user=request.auth.user)
            wedding = Wedding.objects.get(bride=bride)

            wedding_checklist = WeddingChecklist()
            wedding_checklist.wedding = wedding
            wedding_checklist.checklist_item = int(serializer.data["id"])
            wedding_checklist.completed_date = ""

            wedding_checklist.save()
            weddingSerializer = WeddingChecklistSerializer(wedding_checklist, context={'request': request})
            return Response(weddingSerializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET request for single checklist relationship"""
        try:
            item = WeddingChecklist.objects.get(pk=pk)
            serializer = WeddingChecklistSerializer(item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a relationship item"""
        try:
            item = WeddingChecklist.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except WeddingChecklist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handles updating a wedding checklist"""
        wedding_checklist = WeddingChecklist.objects.get(pk=pk)
        
        wedding_checklist.completed_date = request.data["completed_date"]

        wedding_checklist.save()
        serializer = WeddingChecklistSerializer(wedding_checklist, context={'request': request})
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request):
        """handles getting a list of all checklist items special to a wedding"""
        checklist = WeddingChecklist.objects.all()

        wedding = self.request.query_params.get('wedding', None)

        if wedding is not None:
            checklist = checklist.filter(wedding_id=wedding)

        serializer = WeddingChecklistSerializer(
            checklist, many=True, context={'request': request})
        return Response(serializer.data)

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ('id', 'toDo', 'default')

class WeddingChecklistSerializer(serializers.ModelSerializer):
    checklist_item = ChecklistItemSerializer(many=False)
    wedding = WeddingSerializer(many=False)

    class Meta:
        model = WeddingChecklist
        fields = ('id', 'wedding', 'checklist_item', 'completed_date')
        depth = 1

