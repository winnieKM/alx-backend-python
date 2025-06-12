from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user)\
        .select_related('sender')\
        .prefetch_related('histories')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def unread_messages_view(request):
    unread_msgs = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread.html', {'unread_messages': unread_msgs})

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('home')  # Replace 'home' with your home page route name
