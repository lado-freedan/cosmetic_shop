from django.contrib import admin

from .models import Category, Brand, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "brand", "category", "price", "stock", "is_active"]
    list_filter = ["is_active", "brand", "category"]
    list_editable = ["price", "stock", "is_active"]

    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]