from django.urls import path
from app import views
from .views import ContactView, ContactResultView, HistoryView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('area/<str:area>/', views.IndexView.as_view(), name='index'),
    path('area/<str:attraction>/', views.IndexView.as_view(), name='index'),
    path('area/<str:area>/<str:category>/', views.IndexView.as_view(), name='index'),
    path('area/<str:area>/<str:attraction>/<str:category>/', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/preview/', views.PreviewPostView.as_view(), name='preview'),
    path('about', views.AboutView.as_view(), name='about_top'),
    path('category/<str:category>/', views.CategoryNameView.as_view(), name='category_name'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('like/', views.LikeView, name='like'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/result/', ContactResultView.as_view(), name='contact_result'),
    path('histroy', HistoryView.as_view(), name='history'),
]

