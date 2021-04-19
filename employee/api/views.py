from django.contrib.auth import login
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from knox.views import LoginView as KnoxLoginView, LoginView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .serializers import ChangePasswordSerializer, LoginUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, InvoiceSerializer
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, permissions

# Change Password
from rest_framework.views import APIView

# Register API
from ..models import DBOTRequest

# Make token
from rest_framework.authtoken.models import Token


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        response = {}
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token = AuthToken.objects.create(user)[1]
            user_res = request.data
            response.update({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Login',
                'user': user_res,
                'token': token,
            })
        except Exception as e:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_201_CREATED)


# Get User API
class UserAPI(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ListOTRequest(APIView):
#     def get(self, request, format=None):
#         response_data = OTrequest.objects.all()
#         return Response(response_data)


class InvoiceAPIView(APIView):
    def get(self, request, format=None):
        DBOTRequests = DBOTRequest.objects.all()
        serializer = InvoiceSerializer(DBOTRequests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):

    def get_object(self, pk):
        try:
            return DBOTRequest.objects.get(pk=pk)
        except DBOTRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = InvoiceSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = InvoiceSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class RegisterUserAPI(APIView):
#     def post(self, request):
#         serializer = Register(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(status=status.HTTP_200_OK)
#login moi
# class RegisterUserAPI(APIView):
#     permission_classes_by_action = {'create': [AllowAny],
#                                     'list': [IsAdminUser]}
#
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
