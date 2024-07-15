from django.core.management.base import BaseCommand
from users.models import User
from cours.models import Payment, Well


class Command(BaseCommand):
    help = 'Loads payment data into the database'

    def handle(self, *args, **options):
        payment_data = [
            {
                "user": User.objects.get(pk=1),
                "payment_date": "2023-01-01T00:00:00Z",
                "paid_course": Well.objects.get(pk=1),
                "amount": "100.00",
                "payment_method": "cash"
            }
        ]

        for data in payment_data:
            payment = Payment(**data)
            payment.save()

        self.stdout.write(self.style.SUCCESS('Payment data loaded successfully!'))
