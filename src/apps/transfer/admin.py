from django.contrib import admin
from .models import Transfer, Error
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource


class ErrorResources(ModelResource):
    class Meta:
        model = Error


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):

    list_display = ("id", "ext_id", "sender_card_number", "receiver_card_number", "sending_amount", "receiving_amount", "currency", "state", "try_count", "created_at")

    search_fields = ("ext_id", "sender_card_number", "receiver_card_number", "sender_phone", "receiver_phone")

    list_filter = ("state", "currency", "created_at")

    readonly_fields = ("created_at", "updated_at", "confirmed_at", "cancelled_at")

    ordering = ("-created_at",)


@admin.register(Error)
class ErrorAdmin(ImportExportModelAdmin):

    list_display = ("code", "en", "ru", "uz")

    search_fields = ("code", "en", "ru", "uz")

    ordering = ("code",)
    resource_classes = (ErrorResources,)