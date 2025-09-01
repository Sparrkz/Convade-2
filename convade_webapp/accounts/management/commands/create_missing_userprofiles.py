from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile for all users who do not have one.'

    def handle(self, *args, **options):
        User = get_user_model()
        created_count = 0
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created UserProfile for {user.username}'))
        self.stdout.write(self.style.SUCCESS(f'Total new UserProfiles created: {created_count}'))
