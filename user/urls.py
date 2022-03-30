from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from user import views

urlpatterns = [

    path('', views.home, name='home'),
    path('registration/', views.user_registration, name='registration'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('<str:username>/', views.users_pos, name='users'),
    path('<str:username>/posts', views.users_posts_create, name='users_posts'),
    # path('<str:username>/users_posts', views.my_posts, name='my_posts'),
    path('<str:username>/edit_profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/photos/', views.photos, name='photos'),
    path('<str:username>/photos/<int:id>', views.photos_viwes, name='photo_view'),
    path('<str:username>/friends/', views.friend, name='friends'),
    path('<str:username>/People/', views.people, name='people'),
    path("<str:username>/search/", views.search, name="search"),
    path('<str:username>/posts/<int:post_id>', views.post_view, name="post_views"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
