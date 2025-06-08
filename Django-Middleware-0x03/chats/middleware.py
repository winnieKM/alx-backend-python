import logging
from datetime import datetime, time
import time as time_module
from django.http import HttpResponseForbidden, JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger('django.request')
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Allowed time window: 6:00 AM to 9:00 PM
        self.start_time = time(6, 0)
        self.end_time = time(21, 0)

    def __call__(self, request):
        current_time = datetime.now().time()
        if current_time < self.start_time or current_time > self.end_time:
            return HttpResponseForbidden("Access to chat is restricted during this time.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track {ip: [timestamps_of_requests]}
        self.ip_request_times = {}

    def __call__(self, request):
        # Only count POST requests (assuming chat messages are sent as POST)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time_module.time()
            request_times = self.ip_request_times.get(ip, [])

            # Remove timestamps older than 60 seconds (1 minute)
            request_times = [t for t in request_times if now - t < 60]

            if len(request_times) >= 5:
                return JsonResponse(
                    {'error': 'Message rate limit exceeded. Please wait before sending more messages.'},
                    status=429  # Too Many Requests
                )

            # Add current timestamp and update dictionary
            request_times.append(now)
            self.ip_request_times[ip] = request_times

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Try to get the real IP if behind a proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        # Only check authenticated users
        if user.is_authenticated:
            # Assume user has a 'role' attribute; adjust if your User model differs
            user_role = getattr(user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        else:
            # If user is anonymous, deny access
            return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)
