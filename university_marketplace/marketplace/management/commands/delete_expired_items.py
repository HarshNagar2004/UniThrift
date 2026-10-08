# myapp/management/commands/delete_expired_items.py

from django.core.management.base import BaseCommand
from ...models import *
from django.utils import timezone
from django.db.models import F


class Command(BaseCommand):
    help = 'Delete expired items'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_items = Item.objects.filter(created_at__lt=now - timedelta(days=F('How_many_days_you_want_to_advertise_this_on_the_website')))
        count = expired_items.count()
        expired_items.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired items.'))
