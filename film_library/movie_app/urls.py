from django.urls import path
from .views import *

urlpatterns = [
    path('', Cats.as_view(), name='cat_list'),
    path('<slug:cat_slug>/movies', MovieCat.as_view(), name='movies_list'),
    path('<slug:cat_slug>/movies/<slug:movie_slug>', ShowMovie.as_view(), name='movie'),
    path('register', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('user: <int:user_pk>', UserAccount.as_view(), name='user_acc'),
    path('logout', logout_user, name='logout'),
    path('vote/', vote_view, name='vote'),
    path('delete_comment/<int:pk>/', delete_comment_view, name='delete_comment'),
]