import stripe
from forex_python.converter import CurrencyRates

stripe.api_key = "sk_test_51PhIUDGPilVWlYfYrhuL15fDnbUU7shJhXuqs0MhQUxbRrkvDSoBcETALeV035Obwcd63Xj1pU9oP2vHHyvJXmJC0090eplRkn"


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
