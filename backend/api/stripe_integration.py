import os
import stripe
from flask import Blueprint, request, jsonify

stripe_bp = Blueprint('stripe', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@stripe_bp.route("/api/create-checkout-session", methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        amount = data.get('amount', 100)
        
        print(f"Creating checkout session for amount: {amount} cents")
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'BangkokLore Raffle Ticket',
                        'description': 'Support BangkokLore and enter our raffle!'
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://bangkoklore.netlify.app/raffle-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://bangkoklore.netlify.app/raffle-cancel',
            metadata={
                'user_id': 'demo_user', 
                'product': 'raffle_ticket'
            }
        )
        
        print(f"Checkout session created: {session.id}")
        
        return jsonify({
            'sessionId': session.id
        })
        
    except Exception as e:
        print(f"Stripe error: {e}")
        return jsonify({'error': str(e)}), 400


@stripe_bp.route("/api/stripe-webhook", methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        else:
            import json
            event = json.loads(payload)
            print("Webhook signature verification skipped (no secret)")
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        print(f"nvalid signature: {e}")
        return 'Invalid signature', 400

    print(f"📥 Webhook received: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata'].get('user_id', 'demo_user')
        
        print(f" Payment successful for user: {user_id}")
        print(f" Session ID: {session['id']}")
        print(f" Amount paid: {session['amount_total']} cents")
        
        # Add ticket to user's count (using raffle system)
        from api.raffle import user_tickets
        if user_id not in user_tickets:
            user_tickets[user_id] = 0
        user_tickets[user_id] += 1
        
        print(f"🎟️ User {user_id} now has {user_tickets[user_id]} tickets")
        
        return jsonify({
            'success': True, 
            'tickets': user_tickets[user_id],
            'message': f'Payment successful! User now has {user_tickets[user_id]} tickets'
        })
    
    # Handle payment_intent.payment_failed event
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        print(f" Payment failed: {payment_intent['id']}")
        print(f" Failure reason: {payment_intent.get('last_payment_error', {}).get('message', 'Unknown')}")
        
        return jsonify({
            'success': False, 
            'error': 'Payment failed',
            'message': 'Payment was not successful'
        })
    
    # Handle other events
    else:
        print(f" Unhandled event type: {event['type']}")
        return jsonify({'success': True, 'message': f'Event {event["type"]} received'})


@stripe_bp.route("/api/webhook-test", methods=['GET'])
def webhook_test():
    return jsonify({
        'status': 'Webhook endpoint is working',
        'endpoint': '/api/stripe-webhook',
        'methods': ['POST'],
        'events_handled': ['checkout.session.completed', 'payment_intent.payment_failed']
    })
