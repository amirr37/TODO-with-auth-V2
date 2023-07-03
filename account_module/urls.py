from django.urls import path
from account_module import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout',views.LogoutView.as_view() , name='logout' ),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
]
