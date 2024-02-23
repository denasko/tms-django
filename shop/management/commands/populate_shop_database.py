import json

from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    help = 'Populate the shop database with initial data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False,
                            default='shop/management/commands/initial_data_shop.json')

    def handle(self, *args, **options):
        path = options.get('data_file_path', 'initial_data_shop.json')

        with open(path) as file:
            data = json.load(file)

        for item in data:
            product = Product(
                product_name=item['product_name'],
                description=item['description'],
                price=item['price'],
                category_id=item['category_id'],
                sale=item['sale'],
                is_published=item['is_published'],
                pub_date=item['pub_date']
            )
            product.save()

        self.stdout.write(self.style.SUCCESS('Data successfully populated in the shop database.'))
