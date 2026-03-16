from django.core.management.base import BaseCommand
from apps.card.models import Card
import requests


class Command(BaseCommand):

    """
    Docstring for Command
    bu command telegram bot orqali hamma active cardlarni fake sms yuboradi.

    kelajakda buni:
    - aynan o'ziga yuborish imkoniyatini qoshsak boladi.
    - puli yoki muddati oz qolganlar boyicha filter qilib yuborsak bo'ladi.
    - filter asosida push notification ham yuborishimiz mumkin faqat telegram orqali.
    - va yana boshqa imkoniyatlar qoshish mumkin.
    """
    telegram_bot_token = "write here to your telegram bot token from get @botfather"
    admin_chat_id = "write here to your telegram chat id get from @RawDataBot"

    help = "Export cards to CSV"

    def prepare_message(self, card_number, balance, lang="UZ") -> str:
        msg = {
            "uz": f"Sizning kartangiz {card_number} aktiv va foydalanish uchun {balance} UZS mavjud!",
            "ru": f"Ваша карта {card_number} активна. Доступный баланс: {balance} UZS!",
            "en": f"Your card {card_number} is active. Available balance: {balance} UZS!",
        }
        return msg[lang]
    
    def send_message(self, message, chat_id=None) -> dict:
        """
            bu qismda requestsdan foydalandim example uchun lekin ertaga bu sekinlik qiladi yani
            log.(On) - 1mln data bolsa 1mln sekund kutish kerak.
            buni async io orqali yoki aiohttp orqali hal qilsa bo'ladi.
        """
        if chat_id:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendmessage?chat_id={chat_id}&text={message}"
            return requests.get(url).json()
        else:
            print("chat id not found")
            return {}


    def handle(self, *args, **options):
        cards = Card.objects.all()

        for card in cards:
            status_card = card.status
            if status_card.lower() in ["active", "true", "faol"]:
                card_number = card.card_number
                balance = card.balance
                msg = self.prepare_message(card_number, balance, "uz")
                self.send_message(msg, self.admin_chat_id)
                


        self.stdout.write(self.style.SUCCESS("Cards sended to telegram successfully!"))