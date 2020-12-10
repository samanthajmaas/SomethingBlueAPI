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
from somethingblueapi.models import ChecklistItem


class CheckListItems(ViewSet):
    def create(self, request):
        """Handle POST operations for checklist items"""

        item = ChecklistItem()
        item.toDo = request.data["toDo"]
        item.default= False

        try:
            item.save()
            serializer = ChecklistItemSerializer(item, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET request for single checklist item
        Returns:
            Response JSON serialized wedding instance
        """
        try:
            item = ChecklistItem.objects.get(pk=pk)
            serializer = ChecklistItemSerializer(item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def list(self, request):
        """Handles GET request for all checklist items """

        items = ChecklistItem.objects.all()

        serializer = ChecklistItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

"""Basic Serializer for wedding"""
class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ('id', 'toDo', 'default')