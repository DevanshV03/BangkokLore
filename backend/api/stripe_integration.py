import os
import stripe
from flask import Blueprint, request, jsonify

stripe_bp = Blueprint('stripe', __name__)

# Set your Stripe secret key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@stripe_bp.route("/api/create-checkout-session", methods=['POST'])
def create_checkout_session():
    try:
        # Get the amount from request (default €1 = 100 cents)
        data = request.get_json()
        amount = data.get('amount', 100)
        
        print(f"Creating checkout session for amount: {amount} cents")
        
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'BangkokLore Raffle Ticket',
                        'description': 'Support BangkokLore and enter our raffle!'
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://bangkoklore.netlify.app/raffle-success',
            cancel_url='https://bangkoklore.netlify.app/raffle-cancel',
        )
        
        print(f"Checkout session created: {session.id}")
        
        return jsonify({
            'sessionId': session.id
        })
        
    except Exception as e:
        print(f"Stripe error: {e}")
        return jsonify({'error': str(e)}), 400
