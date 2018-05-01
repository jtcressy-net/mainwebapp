from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Creates the default admin user based on DEFAULT_ADMIN_USER and DEFAULT_ADMIN_PASS with DEFAULT_ADMIN_EMAIL'

    def add_arguments(self, parser):
        ""

    def handle(self, *args, **options):
        default_uname = os.environ.get("DEFAULT_ADMIN_USER")
        default_email = os.environ.get("DEFAULT_ADMIN_EMAIL")
        default_pass = os.environ.get("DEFAULT_ADMIN_PASS")
        if default_uname and default_pass and not User.objects.filter(username=default_uname).exists():
            call_command("createsuperuser", username=default_uname, email=default_email, interactive=False)
        else:
            raise CommandError('Superuser could not be created because it either already exists or no username specified')
        usr = User.objects.get(username=default_uname)
        usr.set_password(default_pass)
        usr.save()
        self.stdout.write(self.style.SUCCESS('Successfully created default admin user.'))
