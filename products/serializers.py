from rest_framework import serializers

from .models import Product, Category, Brand, ProductImage


class ProductionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo"]


class ProductListSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), write_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)

    images = ProductionImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "brand_name", "brand","category_name", "category",  "price", "discount_price", "final_price", "stock", "main_image", "images", "description"]
        