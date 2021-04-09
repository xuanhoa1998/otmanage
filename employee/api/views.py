from django.contrib.auth import login
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView, LoginView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .serializers import ChangePasswordSerializer
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


# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        response = {}
        data = request.data
        serializer = AuthTokenSerializer(data=data)
        user = None
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response.update({
                'status': 'success',
                'message': 'Login',
                'user': data['username'],
            })
        try:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            email_user = user.email
            user_set_token = User.objects.filter(email=email_user)
            token = Token.objects.get_or_create(user=user_set_token[0])
            try:
                token = token[0].key
            except Exception as e:
                token = ''
            response.update({
                'token': token,
                'code': status.HTTP_200_OK,
            })
            return Response(response, HTTP_200_OK)

        except Exception as e:
            response.update({
                'code': status.HTTP_404_NOT_FOUND,
            })
            return Response(response, HTTP_404_NOT_FOUND)


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
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


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return DBOTRequest.objects.get(pk=pk)
        except DBOTRequest.DoesNotExist:
            raise Http404

    # def post(self, request):
    #     serializer = InvoiceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
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
