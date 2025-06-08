import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = {
            'conversation': ['exact'],
            'sender': ['exact'],
            # You can add more filters here if needed
        }
