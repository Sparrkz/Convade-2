from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Backfill phone_number and date_of_birth from UserProfile to User if missing.'

    def handle(self, *args, **options):
        User = get_user_model()
        updated_count = 0
        for user in User.objects.all():
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                continue
            changed = False
            if not user.phone_number and profile.emergency_contact_phone:
                user.phone_number = profile.emergency_contact_phone
                changed = True
            if not user.date_of_birth and profile.preferred_start_date:
                user.date_of_birth = profile.preferred_start_date
                changed = True
            if changed:
                user.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated {user.username}'))
        self.stdout.write(self.style.SUCCESS(f'Total users updated: {updated_count}'))
