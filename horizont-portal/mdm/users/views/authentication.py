from rest_framework import permissions
from rest_framework.response import Response as JsonResponse
from rest_framework import generics, views
from users.serializers.users import UserSerializer

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class Authentication(views.APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user, many=False)
            return JsonResponse(serializer.data, status=200)
        else:
            JsonResponse({"detail": "You don't have permissions to perform this action."}, status=403)


class Deauthentication(views.APIView):

    def get(self, request):
        logout(request)
        return JsonResponse({"detail": "Logout Success"}, status=200)
