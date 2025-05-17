import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.encoding import smart_str
from web3 import Web3
from decimal import Decimal
import os

logger = logging.getLogger(__name__)

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
        # TODO: implement actual smart contract interaction
        logger.info(f"Processing USDC payment of {amount_usdc} for {phone_number}")
        return True
    except Exception as e:
        logger.error(f"Blockchain payment error: {e}")
        return False

@csrf_exempt
def ussd_callback(request):
    """Stateless USSD callback handler based entirely on text input history."""
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        payload = request.POST or json.loads(request.body)
        session_id = payload.get('sessionId')
        phone = payload.get('phoneNumber')
        text = payload.get('text', '').strip()

        # Input validation
        if not all([session_id, phone]):
            return HttpResponse("END Invalid request parameters.", content_type="text/plain")

        # Split the entire input history by '*'
        inputs = text.split('*') if text else []
        level = len(inputs)
        response = ''

        # Level 0: initial menu
        if level == 0:
            response = (
                "CON Welcome to M‑Shamba AI\n"
                "1. Sell Produce\n"
                "2. View Prices\n"
                "3. Account Balance\n"
                "4. Help"
            )

        # Level 1: handle first choice
        elif level == 1:
            choice = inputs[0]
            if choice == '1':  # Sell Produce
                response = "CON Choose a product:\n"
                for key, prod in MOCK_PRODUCTS.items():
                    response += f"{key}. {prod['name']} (USDC {prod['usdc_price']})\n"
            elif choice == '2':  # View Prices
                response = "CON Today's market prices:\n"
                for prod in MOCK_PRODUCTS.values():
                    response += f"{prod['name']}: USDC {prod['usdc_price']}\n"
                response += "\nEND Thank you for using M‑Shamba AI."
            elif choice == '3':  # Account Balance
                response = "END Your account balance is USDC 10.00"
            elif choice == '4':  # Help
                response = "END Help: Call 0800-xxx for support."
            else:
                response = "END Invalid option."

        # Level 2: after product selected, ask quantity
        elif level == 2:
            prod_key = inputs[1]
            product = MOCK_PRODUCTS.get(prod_key)
            if product:
                response = f"CON Enter quantity (kg) for {product['name']}:"
            else:
                response = "END Invalid product choice."

        # Level 3: after quantity, confirm payment
        elif level == 3:
            prod_key, qty = inputs[1], inputs[2]
            product = MOCK_PRODUCTS.get(prod_key)
            if product and qty.isdigit() and 0 < int(qty) <= 1000:
                amount_usdc = Decimal(str(int(qty) * product['usdc_price']))
                response = (
                    f"CON You are about to sell {qty}kg of {product['name']}\n"
                    f"Total price: USDC {amount_usdc:.2f}\n"
                    "1. Confirm payment\n"
                    "2. Cancel"
                )
            else:
                response = "END Please enter a valid number (1-1000 kg)."

        # Level 4: payment confirmation
        elif level == 4:
            prod_key, qty, confirm = inputs[1], inputs[2], inputs[3]
            product = MOCK_PRODUCTS.get(prod_key)
            if confirm == '1' and product:
                amount_usdc = Decimal(str(int(qty) * product['usdc_price']))
                success = handle_blockchain_payment(phone, amount_usdc, product)
                if success:
                    response = (
                        f"END Thank you! Your sale of {qty}kg {product['name']} for USDC {amount_usdc:.2f} "
                        f"has been received. Confirmation will follow."
                    )
                else:
                    response = "END Sorry, technical issue. Please try again later."
            else:
                response = "END Your request has been cancelled."

        else:
            response = "END Thank you for using M‑Shamba AI."

        return HttpResponse(smart_str(response), content_type="text/plain")

    except Exception as e:
        logger.error(f"USSD handler error: {e}")
        return HttpResponse("END Sorry, technical error.", content_type="text/plain")

