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
from somethingblueapi.models import VisionBoard, Wedding, Bride


class VisionBoards(ViewSet):
    def create(self, request):
        """Handle POST operations for vision board images"""

        bride = Bride.objects.get(user=request.auth.user)
        wedding = Wedding.objects.get(bride=bride)

        board_item = VisionBoard()

        board_item.wedding = wedding

        if "vb_img" in request.data:
                format, imgstr = request.data["vb_img"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'"vb_img"-{uuid.uuid4()}.{ext}')

                board_item.vb_img = data

        try:
            board_item.save()
            serializer = VisionBoardSerializer(board_item, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET request for single vision board image"""
        try:
            image = VisionBoard.objects.get(pk=pk)
            serializer = VisionBoardSerializer(image, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an image"""
        try:
            image = VisionBoard.objects.get(pk=pk)
            image.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except VisionBoard.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list (self, request):
        """Handles get request for images for logged in user"""
        bride = Bride.objects.get(user=request.auth.user)
        wedding = Wedding.objects.get(bride=bride)
        images = VisionBoard.objects.filter(wedding=wedding)

        serializer = VisionBoardSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

class VisionBoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisionBoard
        fields = ('id', 'vb_img', 'wedding')