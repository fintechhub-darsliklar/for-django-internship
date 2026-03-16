import csv
from django.core.management.base import BaseCommand
from apps.card.models import Card


class Command(BaseCommand):

    """
    Docstring for Command

    bu command barcha cardlarni berilgan filter asosida filter qiladi 
    va csv faylga saqlaydi.
    filter uchun:
     --status=[True, False, active, inactive]
     --card_number=[biror belgi bilan boshlangan]
     --phone=[biror belgi bilan boshlangan]

    """

    help = "Export cards to CSV"

    def add_arguments(self, parser):
        parser.add_argument('--status', type=str)
        parser.add_argument('--card_number', type=str)
        parser.add_argument('--phone', type=str)

    def handle(self, *args, **options):
        cards = Card.objects.all()

        if options['status']:
            cards = cards.filter(status=options['status'])
        
        if options['card_number']:
            cards = cards.filter(card_number__startswith=options['card_number'])

        if options['phone']:
            cards = cards.filter(phone__startswith=options['phone'])

        with open('cards_export.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(['id', 'card_number', 'phone', 'status', "expire"])

            for card in cards:
                writer.writerow([
                    card.id,
                    card.card_number,
                    card.phone,
                    card.status,
                    card.expire
                ])

        self.stdout.write(self.style.SUCCESS("Cards exported successfully!"))