from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message
from .managers import UnreadMessagesManager
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    """Deletes the current user and all associated data."""
    request.user.delete()
    return redirect('home')  # Update this to your app’s landing/home URL name

@login_required
@cache_page(60)
def inbox(request):
    """Shows unread messages with manager, optimized queries."""
    unread_msgs = (
        Message.unread
        .unread_for_user(request.user)  # uses custom manager
        .select_related('sender')       # optimize joins
        .only('sender__username', 'content', 'timestamp', 'id')  # fetch only needed fields
    )
    return render(request, 'messaging/inbox.html', {
        'messages': unread_msgs
    })

@login_required
@cache_page(60)
def sent_messages(request):
    """Displays messages sent by the user, optimized for DB queries."""
    sent = (
        Message.objects
        .filter(sender=request.user)   # explicit filter using sender=request.user
        .select_related('receiver')
        .only('receiver__username', 'content', 'timestamp', 'id')
    )
    return render(request, 'messaging/sent.html', {
        'messages': sent
    })

@login_required
@cache_page(60)
def conversation_view(request):
    """Loads all messages for the user with optimization."""
    convos = (
        Message.objects
        .filter(receiver=request.user)
        .select_related('sender')
        .prefetch_related('replies')
        .only('sender__username', 'content', 'timestamp', 'parent_message', 'id')
    )
    return render(request, 'messaging/conversation.html', {
        'messages': convos
    })

def get_message_thread(message):
    """Recursively fetch replies to a given message."""
    thread = []
    replies = Message.objects.filter(parent_message=message).select_related('sender').only('sender__username','content','timestamp','id')
    for reply in replies:
        thread.append(reply)
        thread.extend(get_message_thread(reply))
    return thread

@login_required
@cache_page(60)
def threaded_conversation_view(request, message_id):
    """Displays a single threaded conversation rooted at message_id."""
    root = get_object_or_404(Message, id=message_id)
    thread = get_message_thread(root)
    return render(request, 'messaging/thread.html', {
        'root': root,
        'replies': thread
    })
