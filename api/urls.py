from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

urlpatterns = [
    #Manager
    path('managers/', views.ManagerUserListView.as_view(), name="managers"),
    path('signup/', views.ManagerUserCreateView.as_view(), name="signup"),
    path('change-password/', views.ChangePasswordView.as_view(), name="change-password"),


    #Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]