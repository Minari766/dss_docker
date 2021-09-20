from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    # path('profile/', views.MyFavoriteView.as_view(), name='profile'),
    path('myfavorite/', views.MyFavoriteView.as_view(), name='myfavorite'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('mypost/', views.MyPostView.as_view(), name='mypost'),
    path('guest_login/', views.guest_login, name='guest_login'),
]