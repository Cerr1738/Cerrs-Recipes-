from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Category
from recipes.services import MealDBService

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with recipes from TheMealDB API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of recipes to import'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Get or create a system user for imported recipes
        user, created = User.objects.get_or_create(
            username='mealdb_importer',
            defaults={
                'email': 'mealdb@example.com',
                'is_active': True
            }
        )
        
        if created:
            user.set_password('changeme123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created mealdb_importer user'))
        
        # Import categories first
        self.stdout.write('Importing categories from TheMealDB...')
        categories = MealDBService.get_all_categories()
        for cat in categories:
            Category.objects.get_or_create(name=cat['strCategory'])
        self.stdout.write(self.style.SUCCESS(f'Imported {len(categories)} categories'))
        
        # Import recipes
        self.stdout.write(f'Importing {count} recipes from TheMealDB...')
        imported = 0
        skipped = 0
        
        for _ in range(count):
            meal = MealDBService.get_random_meal()
            if not meal:
                continue
            
            meal_id = meal.get('idMeal')
            
            # Check if already exists
            if Recipe.objects.filter(mealdb_id=meal_id).exists():
                skipped += 1
                continue
            
            # Create recipe
            try:
                recipe_data = MealDBService.parse_meal_to_recipe_data(meal, user)
                Recipe.objects.create(**recipe_data)
                imported += 1
                self.stdout.write(f'Imported: {meal.get("strMeal")}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing {meal.get("strMeal")}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding completed!\n'
            f'Imported: {imported}\n'
            f'Skipped: {skipped}\n'
            f'Total recipes in database: {Recipe.objects.count()}'
        ))