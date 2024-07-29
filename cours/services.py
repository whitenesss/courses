import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

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
