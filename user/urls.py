from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from user import views

urlpatterns = [
    # path('', views.user_admin, name='user_admin'),
    path('registration', views.registration_views, name='Registration'),
    path('', views.home, name='home'),
    path('registration/', views.userregistration, name='registration'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('<str:username>/', views.users_pos, name='users'),
    path('<str:username>/posts', views.users_posts, name='users_posts'),
    # path('<str:username>/posts', views.like_create_view, name='like'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)