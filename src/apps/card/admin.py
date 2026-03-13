from django.contrib import admin
from .models import Card
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.exceptions import ImportError
# Register your models here.


class CardResource(resources.ModelResource):
    class Meta:
        model = Card
        fields = ('card_number', 'phone', 'balance', 'status', 'expire', 'id',) 
        import_id_fields = ('id',)

    def check_card_number(self, card_number):
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

    def before_import_row(self, row, row_number=None, **kwargs):
        print(row)
        if "card_number" not in row:
            raise ImportError("Karta raqam bo'lishi majburiy!")
        elif "phone" not in row:
            raise ImportError("Telefon raqam bo'lishi majburiy!")
        
        card_number = str(row.get("card_number"))
        card_number = card_number.strip().replace("-", "").replace(" ", "")
        phone_number = str(row.get("phone"))
        phone_number = phone_number.strip().replace("-", "").replace(" ", "")
        if not phone_number.startswith("+"):
            phone_number = "+" + phone_number
        if not phone_number.startswith("+998"):
            phone_number = "+998" + phone_number[1:]


        if len(card_number) != 16:
            raise ImportError(f"Karta raqam 16 xonadan iborat bo'lishi kerak!\nSizdagi ko'rinish: {card_number}")
        elif len(phone_number) != 13:
            raise ImportError(f"Telefon raqam ko'rinishi +998901234567 formatda bo'lishi kerak!\nSizdagi ko'rinish: {phone_number}")
       
        # elif not self.check_card_number(card_number):
        #     raise ImportError(f"Karta raqam xaqiqiy emas!\n Raqam: {card_number}")







@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    resource_classes = [CardResource]
    list_display = ("formated_card", "formated_phone", "balance", "status", "expire")
    list_filter = ("status", "expire")
    search_fields = ("phone", "formated_card")

    def formated_card(self, obj):
        # 8600 0000 0000 0000 shu kabi format qilib berish uchun
        return f"{obj.card_number[:4]} {obj.card_number[4:8]} {obj.card_number[8:12]} {obj.card_number[12:]}"
    
    def formated_phone(self, obj):
        # +998 90 123 45 67 shu kabi format qilib berish uchun
        return f"{obj.phone[:4]} {obj.phone[4:6]} {obj.phone[6:9]} {obj.phone[9:11]} {obj.phone[11:13]}"

    # bular yuqorida adminda ko'rinishi uchun
    formated_card.short_description = "Card Number"
    formated_phone.short_description = "Phone Number"

