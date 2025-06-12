from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').only('sender', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})
