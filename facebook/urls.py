from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.signin, name = "signin"),
    path('signin',views.signin, name = "signin"),
    path('login',views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('home',views.home, name = 'home'),
    #path('btntest',views.btntest,name = 'btntest')
    path('btntest',views.Btntest.as_view(), name='btntest'),
    #path('like', csrf_exempt(views.Like.as_view()), name = 'like')
    path('like',csrf_exempt(views.like), name = 'like'),
    path('unlike', csrf_exempt(views.unlike), name = 'unlike'),
    path('searchtrial', views.searchtrial, name = 'searchtrial'),
    path('signup',views.signup, name = 'signup'),
    path('user_registration', csrf_exempt(views.user_registration), name = 'user_registration'),
    path('comment', csrf_exempt(views.comment), name = 'comment'),
    path('post', csrf_exempt(views.post), name = 'post'),
    path('testpage/<id>', views.testpage, name = "testpage"),
    path('logintest', csrf_exempt(views.logintest), name = 'logintest'),
    path('messages/<id>',views.messages, name = 'messages'),
    path('chat', views.chat, name = 'chat'),
    path('send_message/<receiver>', views.send_message, name = 'send_message')
    
]

urlpatterns = urlpatterns+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)