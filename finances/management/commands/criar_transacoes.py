from django.core.management import BaseCommand
from faker import Faker

from finances.models import Transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("en_PH")

        for _ in range(10000):
            value = fake.random_number(digits=3, fix_len=True)
            description = fake.english_text(max_nb_chars=180)
            due_date = fake.date_this_month(
                before_today=True, after_today=True)

            Transaction.objects.create(
                user_id=1,
                account_id=1,
                category_id=1,
                value=value,
                description=description,
                due_date=due_date,
            )
        print("TRANSAÇŌES CRIADAS COM SUCESSO")
