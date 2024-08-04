import datetime
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import UserSession
from django.contrib.auth.signals import user_logged_in

def create_user_session(sender, request, user, **kwargs):
    UserSession.objects.create(user=user)


class LoginHistoryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass  # This can be left empty or used for other request-based logic


user_logged_in.connect(create_user_session)