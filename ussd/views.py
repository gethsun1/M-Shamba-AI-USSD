import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.encoding import smart_str

@csrf_exempt
def ussd_callback(request):
    """
    Handles incoming USSD requests from the gateway.
    """
    if request.method == 'POST':
        payload = request.POST or json.loads(request.body)
        session_id   = payload.get('sessionId')
        service_code = payload.get('serviceCode')
        phone        = payload.get('phoneNumber')
        text         = payload.get('text', '')

        # Split user inputs by “*” to track menu depth
        inputs = text.split('*') if text else []

        # Session‑backed state storage
        session = request.session
        session['phone'] = phone
        session_key = f"ussd:{session_id}"
        session_data = session.get(session_key, {'level': 0})
        level = session_data['level']

        # Build USSD response
        if level == 0:
            response = "CON Karibu M‑Shamba AI\n1. Uza Mazao\n2. Angalia Bei\n3. Akaunti\n4. Msaada"
            session_data['level'] = 1
        elif level == 1 and inputs[0] == '1':
            response = "CON Chagua zao:\n1. Mahindi\n2. Mihogo\n3. Nyanya"
            session_data['level'] = 2
        # … add further branches here …
        else:
            response = "END Asante kwa kutumia M‑Shamba AI."

        # Persist session state
        session[session_key] = session_data
        session.save()

        return HttpResponse(smart_str(response), content_type="text/plain")
    return HttpResponse("Method not allowed", status=405)
