from django.contrib.auth.models import User
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import UserPermission
from users.serializers import UserSerializer, UserListSerializer
from django.shortcuts import get_object_or_404


class UserListAPI(APIView):
    """
    Endpoint de listado de usuarios
    """

    permission_classes = (UserPermission,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data) #en rest framework los datos que se envían están en data, y no en POST
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserDetailAPI(APIView):
    """
    Endpoint of user detail
    """
    permission_classes = (UserPermission,)

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk) #si no encuentra ningún usuario, devuelve una respuesta 404
        self.check_object_permissions(request, user)  # llama a has_object_permission
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)  # llama a has_object_permission
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)  # llama a has_object_permission
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)