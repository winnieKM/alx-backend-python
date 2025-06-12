from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message
from django.db.models import Prefetch

@cache_page(60)
@login_required
def inbox(request):
    messages = (
        Message.objects
        .filter(receiver=request.user)
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender'))
        )
        .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp', 'read')
        .order_by('-timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})

@cache_page(60)
@login_required
def sent_messages(request):
    messages = (
        Message.objects
        .filter(sender=request.user)
        .select_related('receiver')
        .only('id', 'receiver__username', 'content', 'timestamp', 'read')
        .order_by('-timestamp')
    )
    return render(request, 'messaging/sent.html', {'messages': messages})
