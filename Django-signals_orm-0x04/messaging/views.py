from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message
from .managers import MessageManager
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    """View to delete user account"""
    user = request.user
    user.delete()
    return redirect('login')

@login_required
@cache_page(60)
def inbox(request):
    """Inbox showing unread messages using custom manager, optimized with only()"""
    unread_messages = Message.unread.unread_for_user(request.user).select_related('sender').only('sender__username', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})

@login_required
@cache_page(60)
def conversation_view(request):
    """Example conversation view optimized with select_related and prefetch_related"""
    messages = Message.objects.filter(sender=request.user).select_related('sender').prefetch_related('replies')
    return render(request, 'messaging/conversation.html', {'messages': messages})

def get_message_thread(message):
    """Recursively fetch all replies to a message"""
    thread = []
    replies = Message.objects.filter(parent_message=message).select_related('sender')
    for reply in replies:
        thread.append(reply)
        thread.extend(get_message_thread(reply))  # recursion
    return thread

@login_required
@cache_page(60)
def threaded_conversation_view(request, message_id):
    """Display threaded messages starting from a root"""
    root_message = get_object_or_404(Message, id=message_id)
    replies = get_message_thread(root_message)
    return render(request, 'messaging/thread.html', {
        'root': root_message,
        'replies': replies,
    })
