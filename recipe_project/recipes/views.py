from rest_framework import viewsets, permissions, status # type: ignore
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Recipe
from .serializers import CategorySerializer, RecipeSerializer, RecipeDetailSerializer
from .filters import RecipeFilter

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('category', 'created_by').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RecipeFilter
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'prep_time', 'title']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_recipes(self, request):
        recipes = self.queryset.filter(created_by=request.user)
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_name = request.query_params.get('name')
        if not category_name:
            return Response(
                {'error': 'Category name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipes = self.queryset.filter(category__name__iexact=category_name)
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)