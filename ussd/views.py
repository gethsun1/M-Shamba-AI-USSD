import json
import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.encoding import smart_str
from .session_manager import USSDSessionManager
from web3 import Web3
from decimal import Decimal
import os

logger = logging.getLogger(__name__)
session_manager = USSDSessionManager()

# Initialize Web3 with Base testnet
w3 = Web3(Web3.HTTPProvider(os.getenv('BASE_RPC_URL', 'https://goerli.base.org')))
USDC_CONTRACT_ADDRESS = os.getenv('USDC_CONTRACT_ADDRESS')
ESCROW_CONTRACT_ADDRESS = os.getenv('ESCROW_CONTRACT_ADDRESS')

# Mock products for demo purposes
MOCK_PRODUCTS = {
    '1': {'name': 'Maize', 'price': 100, 'usdc_price': 0.7},
    '2': {'name': 'Cassava', 'price': 150, 'usdc_price': 1.05},
    '3': {'name': 'Tomato', 'price': 200, 'usdc_price': 1.4},
}

def handle_blockchain_payment(phone_number: str, amount_usdc: Decimal, product_data: dict) -> bool:
    """Handle USDC payment via Base OnchainKit."""
    try:
        # TODO: Implement actual smart contract interaction
        logger.info(f"Processing USDC payment of {amount_usdc} for {phone_number}")
        return True
    except Exception as e:
        logger.error(f"Blockchain payment error: {e}")
        return False

@csrf_exempt
def ussd_callback(request):
    """Enhanced USSD callback handler with improved error handling and blockchain integration."""
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        payload = request.POST or json.loads(request.body)
        session_id = payload.get('sessionId')
        phone = payload.get('phoneNumber')
        text = payload.get('text', '')

        # Input validation
        if not all([session_id, phone]):
            logger.error(f"Invalid request parameters: {payload}")
            return HttpResponse("END Invalid request parameters.", content_type="text/plain")

        inputs = text.split('*') if text else []
        state = session_manager.get_session(session_id)
        level = state['level']
        data = state.get('data', {})
        response = ''

        # Retry limit
        if state.get('retries', 0) >= 3:
            session_manager.clear_session(session_id)
            return HttpResponse("END Session expired. Please try again.", content_type="text/plain")

        # Main menu
        if level == 0:
            response = (
                "CON Welcome to M‑Shamba AI\n"
                "1. Sell Produce\n"
                "2. View Prices\n"
                "3. Account Balance\n"
                "4. Help"
            )
            state['level'] = 1

        # Main menu selection
        elif level == 1:
            choice = inputs[0] if inputs else ''
            if choice == '1':
                response = "CON Choose a product:\n"
                for key, prod in MOCK_PRODUCTS.items():
                    response += f"{key}. {prod['name']} (USDC {prod['usdc_price']})\n"
                state['level'] = 2
            elif choice == '2':
                response = "CON Today's market prices:\n"
                for prod in MOCK_PRODUCTS.values():
                    response += f"{prod['name']}: USDC {prod['usdc_price']}\n"
                response += "\nEND"
                state['level'] = 0
            elif choice == '3':
                # Fetch wallet balance from Base (mock)
                response = "END Your account balance is USDC 10.00"
                state['level'] = 0
            elif choice == '4':
                response = "END Help: Call 0800-xxx for support."
                state['level'] = 0
            else:
                response = "END Invalid option."
                state['level'] = 0

        # Product selection
        elif level == 2:
            prod_choice = inputs[1] if len(inputs) > 1 else ''
            product = MOCK_PRODUCTS.get(prod_choice)
            if product:
                data['product'] = product
                response = f"CON Enter quantity (kg) for {product['name']}:"
                state['level'] = 3
                state['data'] = data
            else:
                session_manager.increment_retry(session_id)
                response = "END Invalid product choice."
                state['level'] = 0

        # Quantity input
        elif level == 3:
            quantity = inputs[2] if len(inputs) > 2 else ''
            if quantity.isdigit() and 0 < int(quantity) <= 1000:
                product = data.get('product')
                amount_usdc = Decimal(str(float(quantity) * product['usdc_price']))
                response = (
                    f"CON You are about to sell {quantity}kg of {product['name']}\n"
                    f"Total price: USDC {amount_usdc:.2f}\n"
                    "1. Confirm payment\n"
                    "2. Cancel"
                )
                data['quantity'] = quantity
                data['amount_usdc'] = str(amount_usdc)
                state['level'] = 4
                state['data'] = data
            else:
                session_manager.increment_retry(session_id)
                response = "END Please enter a valid number (1-1000 kg)."
                state['level'] = 0

        # Payment confirmation
        elif level == 4:
            confirm = inputs[3] if len(inputs) > 3 else ''
            if confirm == '1':
                amount_usdc = Decimal(data['amount_usdc'])
                if handle_blockchain_payment(phone, amount_usdc, data):
                    response = (
                        f"END Thank you! Your request to sell {data['quantity']}kg of {data['product']['name']} "
                        f"for USDC {amount_usdc:.2f} has been received. You will receive a confirmation soon."
                    )
                else:
                    response = "END Sorry, technical issue. Please try again."
            else:
                response = "END Your request has been cancelled."
            state['level'] = 0
            state['data'] = {}

        else:
            response = "END An error occurred."
            state['level'] = 0
            state['data'] = {}

        # Persist session
        session_manager.save_session(session_id, state)
        return HttpResponse(smart_str(response), content_type="text/plain")

    except Exception as e:
        logger.error(f"USSD handler error: {e}")
        return HttpResponse("END Sorry, technical error.", content_type="text/plain")
