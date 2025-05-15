import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.encoding import smart_str

# Mock products for demo purposes
MOCK_PRODUCTS = {
    '1': {'name': 'Mahindi', 'price': 100},
    '2': {'name': 'Mihogo', 'price': 150},
    '3': {'name': 'Nyanya', 'price': 200},
}

@csrf_exempt
def ussd_callback(request):
    """
    Handles incoming USSD requests from the gateway.
    """
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    payload = request.POST or json.loads(request.body)
    session_id   = payload.get('sessionId')
    service_code = payload.get('serviceCode')
    phone        = payload.get('phoneNumber')
    text         = payload.get('text', '')

    # Track user inputs by splitting on *
    inputs = text.split('*') if text else []

    # Session management
    session = request.session
    session_key = f"ussd:{session_id}"
    state = session.get(session_key, {'level': 0, 'data': {}})
    level = state['level']
    data = state['data']

    response = ''

    # Level 0: Main menu
    if level == 0:
        response = (
            "CON Karibu M‑Shamba AI\n"
            "1. Uza Mazao\n"
            "2. Angalia Bei\n"
            "3. Akaunti\n"
            "4. Msaada"
        )
        state['level'] = 1

    # Level 1: Handle main selection
    elif level == 1:
        choice = inputs[0] if inputs else ''
        if choice == '1':  # Sell produce
            response = "CON Chagua zao:\n"
            for key, prod in MOCK_PRODUCTS.items():
                response += f"{key}. {prod['name']}\n"
            state['level'] = 2
        elif choice == '2':  # Check prices
            response = "CON Bei za soko leo:\n"
            for prod in MOCK_PRODUCTS.values():
                response += f"{prod['name']}: KES {prod['price']} per kg\n"
            response += "\nEND"  # Single page end
            state['level'] = 0
        elif choice == '3':
            response = "END Akaunti yako ina KES 1,000."
            state['level'] = 0
        elif choice == '4':
            response = "END Msaada: Piga 0800-xxx za msaada."
            state['level'] = 0
        else:
            response = "END Chaguo batili."
            state['level'] = 0

    # Level 2: After selecting product to sell
    elif level == 2:
        prod_choice = inputs[1] if len(inputs) > 1 else ''
        product = MOCK_PRODUCTS.get(prod_choice)
        if product:
            data['product'] = product
            response = f"CON Uingize wingi (kg) ya {product['name']}:"
            state['level'] = 3
            state['data'] = data
        else:
            response = "END Chaguo batili."
            state['level'] = 0

    # Level 3: Quantity input and confirmation
    elif level == 3:
        quantity = inputs[2] if len(inputs) > 2 else ''
        if quantity.isdigit():
            product = data.get('product')
            amount = int(quantity) * product['price']
            response = (
                f"CON Umekamua kuuza {quantity}kg ya {product['name']}\n"
                f"Bei jumla: KES {amount}\n"
                "1. Thibitisha\n"
                "2. Rudia"
            )
            data['quantity'] = quantity
            data['total'] = amount
            state['level'] = 4
            state['data'] = data
        else:
            response = "END Tafadhali ingiza nambari halali."
            state['level'] = 0

    # Level 4: Final confirmation
    elif level == 4:
        confirm = inputs[3] if len(inputs) > 3 else ''
        if confirm == '1':
            # TODO: invoke payment_service 
            response = (
                f"END Asante! Ombi lako la kuuza {data['quantity']}kg ya {data['product']['name']}\n"
                "limepokelewa na tutakuwasiliana nawe hivi punde."
            )
        else:
            response = "END Umegoma ombi."
        state['level'] = 0
        state['data'] = {}

    else:
        response = "END Umefanya kosa."
        state['level'] = 0
        state['data'] = {}

    # Persist session
    session[session_key] = state
    session.save()

    return HttpResponse(smart_str(response), content_type="text/plain")
