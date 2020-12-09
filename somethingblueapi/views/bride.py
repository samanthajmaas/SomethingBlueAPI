"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from somethingblueapi.models import Bride
from rest_framework.decorators import action

class Brides(ViewSet):
    """Viewset managing all brides/users"""
    def list(self, request):
        """Handle GET requests to users resource
        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handles GET requests to users resource for single User
        Written for User Profile View
        Returns:
            Response -- JSON serielized rareuser instance
        """
        try:
            bride = Bride.objects.get(pk=pk)

            bride.is_current_user = None
            current_bride = Bride.objects.get(user=request.auth.user)

            if current_bride.id == int(pk):
                bride.is_current_user = True
            else:
                bride.is_current_user = False

            bride = BrideSerializer(bride, many=False, context={'request': request})

            return Response(bride.data)

        except Bride.DoesNotExist:
            return Response(
                {'message': 'User does not exist.'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def current_user(self, request):
        current_user = request.auth.user

        serializer = UserSerializer(current_user, context={'request': request})

        return Response(serializer.data)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id','username', 'is_staff', 'is_active', 'first_name', 'last_name', 'email', 'date_joined')

class BrideSerializer(serializers.ModelSerializer):
    """JSON serializer for Bride info in profile detail view"""
    class Meta:
        model = Bride
        fields = ("id", "is_staff", "is_active", "full_name", "profile_image_url", "is_current_user", "email", "date_joined")