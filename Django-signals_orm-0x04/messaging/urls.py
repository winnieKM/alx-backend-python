from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('unread/', views.unread_messages_view, name='unread_messages'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('messaging/', include('messaging.urls')),
]
