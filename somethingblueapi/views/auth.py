"""View module for handling authentication and new user registration"""
import json
import datetime
import uuid
import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from somethingblueapi.models import Bride

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user
    Method arguments:
        request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with true and the users token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            bride = Bride.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # if authentication fails, return false with no token
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
        request -- The full HTTP request object
    '''
    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        is_active=True,
        is_staff=False
    )
    format, imgstr = req_body["profile_image_url"].split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name=f'{req_body["email"]}-{uuid.uuid4()}.{ext}')

    #bride has a property `user` which makes all `user` properties accessible through the bride
    bride = Bride.objects.create(
        user=new_user,
        profile_image_url = data
    )

    # save it all to the db
    bride.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)