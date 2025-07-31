from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.core.cache import cache
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related("products").all()

    def list(self, request, *args, **kwargs):
        cached_data = cache.get("category_list")
        if cached_data:
            return Response(cached_data)

        serializer = self.get_serializer(self.queryset, many=True)
        cache.set("category_list", serializer.data, timeout=60 * 60)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("category_list")

    def perform_update(self, serializer):
        serializer.save()
        cache.delete("category_list")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete("category_list")


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category").all()
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'stock', 'price']
    ordering_fields = ['price', 'stock']

    def list(self, request, *args, **kwargs):
        cached_data = cache.get(f"product_list_page_{request.query_params.get('page', 1)}")
        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set(f"product_list_page_{request.query_params.get('page', 1)}", self.get_paginated_response(serializer.data).data, timeout=60 * 60)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save()
        cache.clear()  

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()
