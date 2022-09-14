from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenRefreshView
from music.views import ModelViewSet
urlpatterns = [

    path('register/', views.RegistrationView.as_view()),
    path('activate/<uuid:activation_code>/',views.ActivationView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('forgot/', views.ForgorPasswordView.as_view()),
    path('restore/',views.RestorePasswordView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('list/', views.UserListView.as_view()),
    path('spam-follow/', views.FollowSpamApi.as_view()),
]