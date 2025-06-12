# messaging/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message
from django.db.models import Prefetch

@cache_page(60)  # ✅ Cache for 60 seconds
@login_required
def conversation_view(request):
    user = request.user
    # ✅ Use select_related for foreign keys, prefetch_related for reverse relations
    messages = Message.objects.filter(receiver=user).select_related('sender').prefetch_related(
        Prefetch('replies')
    ).only('sender__username', 'receiver__username', 'content', 'timestamp', 'parent_message')

    context = {
        'messages': messages,
    }
    return render(request, 'messaging/conversation.html', context)
