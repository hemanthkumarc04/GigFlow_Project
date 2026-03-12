from django.core.management.base import BaseCommand
from core.models import CustomUser, Job, Transaction, Review

class Command(BaseCommand):
    help = 'Populates the database with dummy data for testing'

    def handle(self, *args, **kwargs):
        # Create Users
        admin, created = CustomUser.objects.get_or_create(username='admin', defaults={'email': 'admin@gigflow.test', 'user_type': 'ADMIN'})
        if created:
            admin.set_password('admin123')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

        provider, precreated = CustomUser.objects.get_or_create(username='johndoe', defaults={'email': 'provider@gigflow.test', 'user_type': 'PROVIDER', 'wallet_balance': 1000.00, 'is_verified': True})
        if precreated:
            provider.set_password('provider123')
            provider.save()

        worker, wcreated = CustomUser.objects.get_or_create(username='jane_dev', defaults={'email': 'worker@gigflow.test', 'user_type': 'WORKER', 'wallet_balance': 0.00, 'skills': 'Python, Django, Tailwind', 'is_verified': True})
        if wcreated:
            worker.set_password('worker123')
            worker.save()

        # Create Jobs
        job1, j1created = Job.objects.get_or_create(
            title='Build a React Frontend',
            provider=provider,
            defaults={
                'description': 'Looking for a skilled dev to build a responsive UI.',
                'budget': 300.00,
                'status': 'OPEN',
                'is_deposited': True
            }
        )

        job2, j2created = Job.objects.get_or_create(
            title='Django Backend API Fixes',
            provider=provider,
            defaults={
                'description': 'Need help resolving some N+1 query issues.',
                'budget': 150.00,
                'status': 'IN_PROGRESS',
                'worker': worker,
                'is_deposited': True
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data.'))
