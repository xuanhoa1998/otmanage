from knox import views as knox_views
from .views import LoginAPI, RegisterAPI, UserAPI, ChangePasswordView, InvoiceAPIView, SnippetDetail
from django.urls import path
# from . import views
urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('api/registers', RegisterUserAPI.as_view(), name='registers'),
    path('api/login', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/OTRequests/', InvoiceAPIView.as_view(), name='listviewsOT'),
    path('api/OTRequest/<int:pk>/', SnippetDetail.as_view(), name='listviewsOT'),

]
