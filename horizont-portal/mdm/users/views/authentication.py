from rest_framework import permissions
from common.response import MdmResponse as Response
from rest_framework import generics, views
from users.serializers.users import UserSerializer

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class Authentication(views.APIView):

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response("Invalid credentials", status=400)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=200)
        else:
            return Response({"detail": "You don't have permissions to perform this action."}, status=403)


class Deauthentication(views.APIView):

    def get(self, request):
        logout(request)
        return Response({"detail": "Logout Success"}, status=200)
