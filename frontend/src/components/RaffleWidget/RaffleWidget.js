import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { storyAPI } from '../../services/api';
import './RaffleWidget.css';

// Initialize Stripe with your publishable key
const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY);

const RaffleWidget = () => {
  const [tickets, setTickets] = useState(0);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  // Free ticket (existing functionality)
  const handleFreeTicket = async () => {
    setLoading(true);
    setStatus(null);

    try {
      const data = await storyAPI.buyRaffleTicket();
      
      if (data.success) {
        setTickets(data.tickets);
        setStatus('success');
      } else {
        setStatus('error');
      }
    } catch (error) {
      console.error('Error buying ticket:', error);
      setStatus('error');
    } finally {
      setLoading(false);
    }
  };

  // ✅ NEW: Stripe payment
  const handleStripePayment = async () => {
    setLoading(true);
    setStatus(null);

    try {
      console.log('Creating checkout session...');
      
      // Create checkout session
      const data = await storyAPI.createCheckoutSession(100); // €1 in cents
      
      console.log('Checkout session created:', data);
      
      if (data.sessionId) {
        const stripe = await stripePromise;
        
        console.log('Redirecting to Stripe checkout...');
        
        // Redirect to Stripe checkout
        const { error } = await stripe.redirectToCheckout({
          sessionId: data.sessionId
        });
        
        if (error) {
          console.error('Stripe redirect error:', error);
          setStatus('error');
        }
      } else {
        console.error('No session ID received');
        setStatus('error');
      }
    } catch (error) {
      console.error('Error with Stripe payment:', error);
      setStatus('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="raffle-widget">
      <h3 className="raffle-widget__title">🎟️ Raffle Tickets</h3>
      
      <div className="raffle-widget__count">
        <p>You have <strong>{tickets}</strong> tickets</p>
      </div>

      {/* ✅ Stripe Payment Button */}
      <button 
        className="raffle-widget__btn raffle-widget__btn--primary"
        onClick={handleStripePayment}
        disabled={loading}
      >
        {loading ? 'Processing...' : 'Buy €1 Raffle Ticket'}
      </button>

      {/* Free ticket button for testing */}
      <button 
        className="raffle-widget__btn raffle-widget__btn--free"
        onClick={handleFreeTicket}
        disabled={loading}
      >
        Get Free Ticket (Demo)
      </button>

      {status === 'success' && (
        <div className="raffle-widget__message raffle-widget__message--success">
          ✅ You have {tickets} tickets
        </div>
      )}

      {status === 'error' && (
        <div className="raffle-widget__message raffle-widget__message--error">
          ❌ Error, please try again
        </div>
      )}
    </div>
  );
};

export default RaffleWidget;
