"""
Africa's Talking API integration for M-Shamba USSD service.
"""
import os
import africastalking
from django.conf import settings

# Initialize Africa's Talking
username = os.environ.get('AT_USERNAME', 'sandbox')
api_key = os.environ.get('AT_API_KEY', 'your_api_key')
africastalking.initialize(username, api_key)

# Initialize services
sms = africastalking.SMS
ussd = africastalking.USSD
airtime = africastalking.Airtime
payment = africastalking.Payment

def send_sms(phone_number, message):
    """
    Send SMS using Africa's Talking API
    
    Args:
        phone_number (str): Recipient phone number in international format
        message (str): Message content
        
    Returns:
        dict: Response from Africa's Talking API
    """
    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return {"error": str(e)}

def send_airtime(phone_number, amount, currency="KES"):
    """
    Send airtime using Africa's Talking API
    
    Args:
        phone_number (str): Recipient phone number in international format
        amount (float): Amount to send
        currency (str): Currency code (default: KES)
        
    Returns:
        dict: Response from Africa's Talking API
    """
    try:
        recipients = [{
            "phoneNumber": phone_number,
            "amount": amount,
            "currency": currency
        }]
        response = airtime.send(recipients=recipients)
        return response
    except Exception as e:
        print(f"Error sending airtime: {e}")
        return {"error": str(e)}

def mobile_checkout(phone_number, amount, product_name="M-Shamba", currency="KES"):
    """
    Initiate mobile checkout using Africa's Talking API
    
    Args:
        phone_number (str): Customer phone number in international format
        amount (float): Amount to charge
        product_name (str): Product name (default: M-Shamba)
        currency (str): Currency code (default: KES)
        
    Returns:
        dict: Response from Africa's Talking API
    """
    try:
        response = payment.mobile_checkout(
            product_name=product_name,
            phone_number=phone_number,
            currency=currency,
            amount=amount
        )
        return response
    except Exception as e:
        print(f"Error initiating mobile checkout: {e}")
        return {"error": str(e)}

def mobile_b2c(phone_number, amount, reason="Crop Payment", currency="KES"):
    """
    Send money to customer using Africa's Talking API
    
    Args:
        phone_number (str): Customer phone number in international format
        amount (float): Amount to send
        reason (str): Reason for payment (default: Crop Payment)
        currency (str): Currency code (default: KES)
        
    Returns:
        dict: Response from Africa's Talking API
    """
    try:
        # Consumer = customer receiving the money
        # BusinessPayment = payment for goods or services
        response = payment.mobile_b2c(
            product_name="M-Shamba",
            consumers=[{
                "phoneNumber": phone_number,
                "currencyCode": currency,
                "amount": amount,
                "reason": "BusinessPayment",
                "metadata": {
                    "description": reason
                }
            }]
        )
        return response
    except Exception as e:
        print(f"Error sending B2C payment: {e}")
        return {"error": str(e)}
