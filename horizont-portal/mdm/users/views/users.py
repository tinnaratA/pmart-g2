import django
from django.contrib.auth.models import User
from rest_framework import generics, views
from rest_framework import permissions
from rest_framework import pagination

from common.response import MdmResponse as Response
from users.permissions import users as user_permissions
from users.serializers.users import UserSerializer 

true = True
false = False

class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        user_permissions.CouldListUserProfile
    ]
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return Response(data=response.data, status=200)


class DeleteUserView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    ]

    def get_objects(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise e

    def delete(self, request, username):
        try:
            user = self.get_objects(username)
            user.delete()
            return Response(data='User has been deleted.', status=200)
        except User.DoesNotExist as e:
            return Response(data="User Not Found.", status=204)
        except Exception as e:
            return Response(data="Something went wrong.", status=500)


class UserView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        user_permissions.CouldActionUserProfile
    ]

    def get_objects(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise e

    def get(self, request, username=None):
        try:
            if username:
                user = self.get_objects(username)
            else:
                user = request.user
            serializer = UserSerializer(user, many=False)
            return Response(data=serializer.data, status=200)
        except User.DoesNotExist as e:
            return Response(data="User Not Found.", status=204)
        except Exception as e:
            return Response(data="Something went wrong.", status=500)

    def post(self, request):
        try:
            data = request.data
            if not isinstance(data, (tuple, list)):
                data = [data]
            serializer = UserSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                return Response(data="User has been created.", status=201)
            else:
                return Response(data=serializer.errors, status=400)
        except django.db.utils.IntegrityError as e:
            return Response(data=str(e), status=400)
        except Exception as e:
            return Response(data="Something went wrong.", status=500)

    def put(self, request, username=None):
        try:
            partial = eval(request.GET.get('partial', 'false'))
            if username:
                user = self.get_objects(username)
            else:
                user = request.user
            serializer = UserSerializer(user, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.update(serializer.instance, serializer.validated_data)
                return Response(data="User has been updated.", status=200)
            else:
                return Response(data=serializer.errors, status=400)
        except NameError as e:
            return Response(data="`partial` require only boolean.", status=400)
        except Exception as e:
            return Response(data="Something went wrong.", status=500)
