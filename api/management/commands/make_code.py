from django.core.management.base import BaseCommand, CommandError
import requests
from api.models import *
import json
import time
from django.contrib.auth.models import User

from api.exceptions import ButtonNotPressedException

class Command(BaseCommand):
    help = 'Activation Code'

    def add_arguments(self, parser):
       parser.add_argument('--hours', type=int, help='How many hours')
       

    def handle(self, *args, **options):
        live_hours = options['hours']
        assert live_hours
        expiration_timestamp = int(time.time()) + int(live_hours*60*60)
        activaton_code = ActivationCode.objects.create(expiration_timestamp=expiration_timestamp)

        print(f"Created: {activaton_code}")

