from django.contrib import admin
from .models import Category, Recipe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'prep_time', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'ingredients', 'description')
    readonly_fields = ('created_at', 'updated_at')
