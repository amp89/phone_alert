from django.core.management.base import BaseCommand, CommandError
import requests
from api.models import *
import json

from django.contrib.auth.models import User

from api.exceptions import ButtonNotPressedException

class Command(BaseCommand):
    help = 'Press the button (There is only one, will extend this later if we add more)'

    def add_arguments(self, parser):
       parser.add_argument('--button_id', type=int, help='button id')
       parser.add_argument('--user_id', type=int, help='user id')

    def handle(self, *args, **options):

        ac = AccountConnection.load()
        assert ac
        user = User.objects.get(id=options['user_id'])

        code = ac.code
        url = ac.button_url

        body = json.dumps({

            "virtualButton": options['button_id'],

            "accessCode": code

        })

        res = requests.post(url = url, data = body)
        if res.status_code == 202:
            Alert.objects.create(user=user)
        else:
            raise ButtonNotPressedException(f"Failed to push button: {res.status_code} {res.content}")

