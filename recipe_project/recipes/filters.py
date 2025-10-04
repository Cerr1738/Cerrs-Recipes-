from django_filters import rest_framework as filters
from .models import Recipe

class RecipeFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    ingredient = filters.CharFilter(method='filter_by_ingredient')
    title = filters.CharFilter(lookup_expr='icontains')
    min_prep_time = filters.NumberFilter(field_name='prep_time', lookup_expr='gte')
    max_prep_time = filters.NumberFilter(field_name='prep_time', lookup_expr='lte')
    
    class Meta:
        model = Recipe
        fields = ['category', 'ingredient', 'title']
    
    def filter_by_ingredient(self, queryset, name, value):
        return queryset.filter(ingredients__icontains=value)