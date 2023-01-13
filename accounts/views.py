from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer

from accounts.serializers import UserSerializer, RegisterSerializer

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context = self.get_serializer_context()).data,
            "token": Token.objects.create(user = user).key
        })

class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        serializer = AuthTokenSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']

        return Response({
            "user": UserSerializer(user, context = self.get_serializer_context()).data,
            "token": Token.objects.get(user = user).key
        })
        
class UserDetail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):

        try:
            user = User.objects.get(id = request.user.id)
        except User.DoesNotExist:
            data = {
                "message": "User with this credential does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request):

        try:
            user = User.objects.get(id = request.user.id)
        except User.DoesNotExist:
            data = {
                "message": "User with this credential does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        try:
            user = User.objects.get(id = request.user.id)
        except User.DoesNotExist:
            data = {
                "message": "User with this credential does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# @csrf_exempt
# @api_view(['POST'])
# def create_user(request):

#     serializer = UserSerializer(data = request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status = status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# @api_view(['GET'])
# def show_user(request, id):

#     try:
#         user = User.objects.get(id = id)
#     except User.DoesNotExist:
#         return Response(status = status.HTTP_404_NOT_FOUND)

#     serializer = UserSerializer(user)

#     return Response(serializer.data)

# @csrf_exempt
# @api_view(['PUT'])
# def update_user(request, id):

#     try:
#         user = User.objects.get(id = id)
#     except User.DoesNotExist:
#         return Response(status = status.HTTP_404_NOT_FOUND)

#     serializer = UserSerializer(user, data = request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
    
#     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# @api_view(['DELETE'])
# def delete_user(request, id):

#     try:
#         user = User.objects.get(id = id)
#     except User.DoesNotExist:
#         return Response(status = status.HTTP_404_NOT_FOUND)

#     user.delete()
#     return Response(status = status.HTTP_204_NO_CONTENT)