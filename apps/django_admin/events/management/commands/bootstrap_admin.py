import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update the local Django admin account from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_ADMIN_USERNAME", "operations")
        email = os.getenv("DJANGO_ADMIN_EMAIL", "operations@letsgo.local")
        password = os.getenv("DJANGO_ADMIN_PASSWORD")
        if not password:
            raise CommandError("DJANGO_ADMIN_PASSWORD is required")

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} Django admin user: {username}"))
