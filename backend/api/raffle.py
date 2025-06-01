from flask import Blueprint, request, jsonify

raffle_bp = Blueprint('raffle', __name__)

# Simple in-memory storage for demo (we'll improve this later)
user_tickets = {}

@raffle_bp.route("/api/raffle-ticket", methods=['POST'])
def buy_raffle_ticket():
    try:
        # For now, we'll use a simple user identifier
        user_id = "demo_user"  # We'll make this dynamic later
        
        # Add one ticket for this user
        if user_id not in user_tickets:
            user_tickets[user_id] = 0
        
        user_tickets[user_id] += 1
        
        return jsonify({
            "success": True,
            "tickets": user_tickets[user_id]
        })
        
    except Exception as e:
        print(f"Error: {e}")  # For debugging
        return jsonify({
            "success": False,
            "error": "Error purchasing ticket, please try again"
        }), 500
