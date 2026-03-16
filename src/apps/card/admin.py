from django.contrib import admin
from .models import Card
from import_export.admin import ImportExportModelAdmin
from .resources import CardResource
# Register your models here.


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

