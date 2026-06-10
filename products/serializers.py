from rest_framework import serializers

from .models import Product, Category, Brand


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo"]


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name")
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "brand", "category", "price", "discount_price", "final_price", "stock", "main_image"]
        