from rest_framework import serializers
from .models import Category, Recipe
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    recipe_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'recipe_count', 'created_at')
    
    def get_recipe_count(self, obj):
        return obj.recipes.count()

class RecipeSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    ingredients_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'description', 'ingredients', 'ingredients_list',
            'steps', 'prep_time', 'category', 'category_name', 'created_by',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_by', 'created_at', 'updated_at')
    
    def get_ingredients_list(self, obj):
        return obj.get_ingredients_list()
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class RecipeDetailSerializer(RecipeSerializer):
    category = CategorySerializer(read_only=True)