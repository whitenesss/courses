import stripe
from django_celery_beat.models import PeriodicTask
from forex_python.converter import CurrencyRates
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from datetime import datetime, timedelta

from config.settings import STRIPE_API_KEY
from cours.tasks import check_last_login

stripe.api_key = STRIPE_API_KEY


def get_or_create_stripe_product():
    products = stripe.Product.list(limit=1)
    if not products['data']:
        product = stripe.Product.create(name="Gold Plan")
        return product.id
    return products['data'][0].id


def create_stripe_price(amount):
    """создание цены в страпйпе"""
    product_id = get_or_create_stripe_product()
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product=product_id,
    )


def crate_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    check_last_login()
    task_name = f'Checking last login - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    PeriodicTask.objects.create(
        interval=schedule,
        name=task_name,
        task='tasks.check_last_login',
        expires=datetime.utcnow() + timedelta(seconds=30)
    )


