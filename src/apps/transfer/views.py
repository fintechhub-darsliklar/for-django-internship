import random
from decimal import Decimal
from datetime import datetime
from jsonrpcserver import method, dispatch
from django.http import JsonResponse
from cards.models import Card
from .models import Transfer, TransferState, Error

# OTP yuborishni simulyatsiya qilamiz
def send_otp_via_telegram(phone, otp):
    # real Telegram bot ishlatilsa shu yerda API chaqiriladi
    print(f"Sending OTP {otp} to phone {phone}")
    return True


@method
def transfer_create(ext_id, sender_card_number, sender_card_expiry,
                    receiver_card_number, sending_amount, currency):
    
    # 1️⃣ ext_id uniqueness
    if Transfer.objects.filter(ext_id=ext_id).exists():
        error = Error.objects.get(code=32701)
        return {"error": {"code": error.code, "message": error.en}}

    # 2️⃣ sender card validation
    try:
        sender_card = Card.objects.get(card_number=sender_card_number,
                                       expire=sender_card_expiry)
    except Card.DoesNotExist:
        error = Error.objects.get(code=32704)
        return {"error": {"code": error.code, "message": error.en}}

    if sender_card.status != "active":
        error = Error.objects.get(code=32705)
        return {"error": {"code": error.code, "message": error.en}}

    if sender_card.balance < Decimal(sending_amount):
        error = Error.objects.get(code=32702)
        return {"error": {"code": error.code, "message": error.en}}

    # 3️⃣ receiver card exists
    try:
        receiver_card = Card.objects.get(card_number=receiver_card_number)
    except Card.DoesNotExist:
        error = Error.objects.get(code=32704)
        return {"error": {"code": error.code, "message": error.en}}

    # 4️⃣ currency validation
    if currency not in [643, 840]:
        error = Error.objects.get(code=32707)
        return {"error": {"code": error.code, "message": error.en}}

    # 5️⃣ Generate OTP
    otp = f"{random.randint(100000, 999999)}"

    # 6️⃣ Create transfer
    transfer = Transfer.objects.create(
        ext_id=ext_id,
        sender_card_number=sender_card_number,
        sender_card_expiry=sender_card_expiry,
        receiver_card_number=receiver_card_number,
        sending_amount=sending_amount,
        currency=currency,
        receiving_amount=sending_amount,  # static rate for now
        state=TransferState.CREATED,
        otp=otp,
        try_count=0
    )

    # 7️⃣ Send OTP via Telegram
    otp_sent = send_otp_via_telegram(sender_card.sender_phone, otp)

    return {
        "ext_id": transfer.ext_id,
        "state": transfer.state,
        "otp_sent": otp_sent
    }


# Django view wrapper
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def json_rpc_view(request):
    response = dispatch(request.body)
    return JsonResponse(response, safe=False)