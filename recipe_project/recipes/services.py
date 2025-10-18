import requests
from django.conf import settings
from .models import Recipe, Category

class MealDBService:
    """Service class to interact with TheMealDB API"""
    
    BASE_URL = settings.MEALDB_API_BASE_URL if hasattr(settings, 'MEALDB_API_BASE_URL') else 'https://www.themealdb.com/api/json/v1/1'
    
    @classmethod
    def search_meals_by_name(cls, name):
        """Search meals by name"""
        try:
            response = requests.get(f'{cls.BASE_URL}/search.php', params={'s': name})
            response.raise_for_status()
            return response.json().get('meals', [])
        except requests.RequestException as e:
            print(f"Error fetching meals: {e}")
            return []
    
    @classmethod
    def get_meal_by_id(cls, meal_id):
        """Get a specific meal by ID"""
        try:
            response = requests.get(f'{cls.BASE_URL}/lookup.php', params={'i': meal_id})
            response.raise_for_status()
            meals = response.json().get('meals', [])
            return meals[0] if meals else None
        except requests.RequestException as e:
            print(f"Error fetching meal: {e}")
            return None
    
    # @classmethod
    # def get_random_meal(cls):
    #     """Get a random meal"""
    #     try:
    #         response = requests.get(f'{cls.BASE_URL}/randomselection.php')
    #         response.raise_for_status()
    #         meals = response.json().get('meals', [])
    #         return meals[0] if meals else None
    #     except requests.RequestException as e:
    #         print(f"Error fetching random meal: {e}")
    #         return None
    
    @classmethod
    def filter_by_category(cls, category):
        """Filter meals by category"""
        try:
            response = requests.get(f'{cls.BASE_URL}/filter.php', params={'c': category})
            response.raise_for_status()
            return response.json().get('meals', [])
        except requests.RequestException as e:
            print(f"Error filtering meals: {e}")
            return []
    
    @classmethod
    def get_all_categories(cls):
        """Get all available categories"""
        try:
            response = requests.get(f'{cls.BASE_URL}/categories.php')
            response.raise_for_status()
            return response.json().get('categories', [])
        except requests.RequestException as e:
            print(f"Error fetching categories: {e}")
            return []
    
    @classmethod
    def parse_meal_to_recipe_data(cls, meal, user):
        """Convert TheMealDB meal data to Recipe model format"""
        # Extract ingredients
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}', '').strip()
            measure = meal.get(f'strMeasure{i}', '').strip()
            if ingredient:
                ingredients.append(f"{measure} {ingredient}".strip())
        
        # Get or create category
        category_name = meal.get('strCategory', 'Uncategorized')
        category, _ = Category.objects.get_or_create(name=category_name)
        
        return {
            'title': meal.get('strMeal', 'Unknown'),
            'description': f"{meal.get('strMeal')} - A delicious {category_name} dish from {meal.get('strArea', 'International')} cuisine",
            'ingredients': ', '.join(ingredients),
            'steps': meal.get('strInstructions', 'No instructions provided'),
            'prep_time': 30,  # Default as TheMealDB doesn't provide this
            'category': category,
            'created_by': user,
            'mealdb_id': meal.get('idMeal'),
            'thumbnail_url': meal.get('strMealThumb'),
            'video_url': meal.get('strYoutube'),
            'source_url': meal.get('strSource'),
        }