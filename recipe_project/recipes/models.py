from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="Enter ingredients separated by commas")
    steps = models.TextField(help_text="Enter cooking steps")
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_ingredients_list(self):
        return [ingredient.strip() for ingredient in self.ingredients.split(',')]