from phone_alert.settings import TIME_BETWEEN_REQUEST_SECONDS
from django.shortcuts import render


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from django.http import QueryDict
import time
from django.conf import settings
from api.exceptions import ButtonNotPressedException
from django.core.management import call_command

class APIAuthView(APIView):
    authentication_classes = [
            authentication.SessionAuthentication,
            # authentication.BasicAuthentication
        ]
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args,**kwargs)


class PushButton(APIAuthView):
    def post(self, request, *args, **kwargs):
        now = time.time()

        last_push_window = now - settings.TIME_BETWEEN_REQUEST_SECONDS

        if Alert.objects.filter(user=request.user, timestamp__gt=last_push_window).count() > 0:
            return Response({
                    'message':f'Wait at least {settings.TIME_BETWEEN_REQUEST_SECONDS} seconds until clicking again.',
                }, status=200)

        try:
            call_command('push_button', user_id=request.user.id, button_id=1) # TODO....
            return Response({'message':"Message sent! Please wait a minute for it to execute."}, status=200)
        except ButtonNotPressedException as e:
            return Response({
                'message':'The message was not able to send. Please try again later.',
            }, status=200)


class PasswordView(APIAuthView):
    def post(self, request, *args, **kwargs):
        raise NotImplementedError