from .models import Card
from import_export import resources
from import_export.exceptions import ImportError
# Register your models here.


def format_card(raw_card) -> str:
    card_number = raw_card.strip().replace("-", "").replace(" ", "")
    return card_number


def format_phone(raw_phone) -> str: 
    phone_number = raw_phone.strip().replace("-", "").replace(" ", "")
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number
    if not phone_number.startswith("+998"):
        phone_number = "+998" + phone_number[1:]

    return phone_number


def check_card_number_is_valid(card_number) -> str:
    """
    Docstring for check_card_number_is_valid
    bu funksiya karta raqam reallikda mavjud yoki yoq tekshiradi.
    """

    card_number = str(card_number).replace(" ", "")
    
    if not card_number.isdigit():
        return False

    digits = [int(d) for d in card_number]
    
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    total = sum(digits)

    return total % 10 == 0


class CardResource(resources.ModelResource):
    class Meta:
        model = Card
        fields = ('card_number', 'phone', 'balance', 'status', 'expire', 'id',) 
        import_id_fields = ('id',)

   

    def before_import_row(self, row, row_number=None, **kwargs):
        if "card_number" not in row:
            raise ImportError("Karta raqam bo'lishi majburiy!")
        elif "phone" not in row:
            raise ImportError("Telefon raqam bo'lishi majburiy!")
        
        card_number = format_card(str(row.get("card_number")))
        phone_number = format_phone(str(row.get("phone")))

        if len(card_number) != 16:
            raise ImportError(f"Karta raqam 16 xonadan iborat bo'lishi kerak!\nSizdagi ko'rinish: {card_number}")
        elif len(phone_number) != 13:
            raise ImportError(f"Telefon raqam ko'rinishi +998901234567 formatda bo'lishi kerak!\nSizdagi ko'rinish: {phone_number}")
       
        # elif not check_card_number(card_number):
        #     raise ImportError(f"Karta raqam xaqiqiy emas!\n Raqam: {card_number}")

        row['phone'] = phone_number
        row['card_number'] = card_number
        return row
