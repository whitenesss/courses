import stripe
from forex_python.converter import CurrencyRates

stripe.api_key = "sk_test_51PhIUDGPilVWlYfYrhuL15fDnbUU7shJhXuqs0MhQUxbRrkvDSoBcETALeV035Obwcd63Xj1pU9oP2vHHyvJXmJC0090eplRkn"


def create_stripe_price(amount):
    """создание цены в страпйпе"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount*100),
        product_data={"name": "Gold Plan"},
    )


def crate_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
