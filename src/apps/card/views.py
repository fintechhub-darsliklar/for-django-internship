import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Card


@csrf_exempt
def json_rpc(request):
    body = json.loads(request.body)
    
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    result = None

    if method == "card_list":
        cards = Card.objects.all()
        result = [
            {
                "id": c.id,
                "card_number": c.card_number,
                "phone": c.phone,
                "balance": str(c.balance),
                "status": c.status,
                "expire": str(c.expire)
            }
            for c in cards
        ]

    elif method == "card_create":
        card = Card.objects.create(
            card_number=params.get("card_number"),
            phone=params.get("phone"),
            balance=params.get("balance"),
            status=params.get("status"),
            expire=params.get("expire"),
        )

        result = {
            "id": card.id,
            "card_number": card.card_number
        }

    elif method == "card_detail":
        card = Card.objects.get(id=params.get("id"))

        result = {
            "id": card.id,
            "card_number": card.card_number,
            "phone": card.phone,
            "balance": str(card.balance),
            "status": card.status,
            "expire": str(card.expire)
        }

    return JsonResponse({
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    })