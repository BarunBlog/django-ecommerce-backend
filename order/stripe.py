import stripe
from django.contrib.auth.models import User
from user.models import StripeCustomer


class StripeApiHandler:
    """ A class which will call the stripe APIs """

    Api_key = None

    def __init__(self, stripe_secret_key):
        self.Api_key = stripe_secret_key

    def get_or_create_customer(self, email, username):
        """ method to get or create a stripe customer """
        stripe.api_key = self.Api_key

        # get a user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        try:
            stripe_customer = StripeCustomer.objects.get(user=user)
        except StripeCustomer.DoesNotExist:
            # If the StripeCustomer does not exist, create a new one
            customer = stripe.Customer.create(email=email)
            stripe_customer = StripeCustomer.objects.create(user=user, stripe_customer_id=customer.id)

        return stripe_customer.stripe_customer_id

    def create_payment_method(self, card_number, exp_month, exp_year, cvc):
        stripe.api_key = self.Api_key

        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': card_number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
            },
        )

        return payment_method

    def create_payment_intent(self, customer_id, amount, currency, payment_method_id, confirm, metadata):
        stripe.api_key = self.Api_key

        # Convert the amount from decimal to integer
        amount_in_cents = int(amount * 100)

        payment_intent = stripe.PaymentIntent.create(
            customer=customer_id,
            amount=amount_in_cents,
            currency=currency,
            payment_method=payment_method_id,
            confirm=confirm,
            metadata=metadata
        )

        return payment_intent

    def create_invoice(self, customer_id, description, metadata):
        stripe.api_key = self.Api_key

        invoice = stripe.Invoice.create(
            customer=customer_id,
            description=description,
            metadata=metadata,
            currency='bdt'
        )

        return invoice

    def create_invoice_item(self, customer_id, invoice_id, amount, description):
        stripe.api_key = self.Api_key

        invoice_item = stripe.InvoiceItem.create(
            customer=customer_id,
            invoice=invoice_id,
            amount=int(amount * 100),  # convert to cents
            description=description,
            currency='bdt',
        )

