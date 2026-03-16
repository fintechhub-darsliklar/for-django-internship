from django.contrib import admin
from .models import Transfer, Error


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):

    list_display = ("id", "ext_id", "sender_card_number", "receiver_card_number", "sending_amount", "receiving_amount", "currency", "state", "try_count", "created_at")

    search_fields = ("ext_id", "sender_card_number", "receiver_card_number", "sender_phone", "receiver_phone")

    list_filter = ("state", "currency", "created_at")

    readonly_fields = ("created_at", "updated_at", "confirmed_at", "cancelled_at")

    ordering = ("-created_at",)


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):

    list_display = ("code", "en", "ru", "uz")

    search_fields = ("code", "en", "ru", "uz")

    ordering = ("code",)