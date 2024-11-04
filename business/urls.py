from django.urls import path
from business.views import login_view, home, logout_view, create_user, view_user, create_chat, display_chat,display_other_chat, profile,registeruser, job_search, create_post

urlpatterns = [
    path('', home, name="home"),
    path('user/', profile, name="profile"),
    path('login/', login_view, name="login"),
    path('register/', registeruser, name="registration"),
    path('logout/',logout_view, name="logout"),
    path('adduser/', create_user, name="adduser"),
    path('viewusers/', view_user, name="viewuser"),
    path('viewchat/', display_chat, name="viewchat"),
    path('createchat/',create_chat, name="message"),
    path('user-chat/<int:user_id>/', display_other_chat, name="othermessages"),
    path('jobs', job_search, name="jobs"),
    path('posts', create_post, name='posts'),
]

