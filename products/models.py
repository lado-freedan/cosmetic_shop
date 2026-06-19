from django.db import models


class Category(models.Model):
    name = models.CharField("Category Name", max_length=100)
    slug = models.SlugField("Category Slug", max_length=100,unique=True, allow_unicode=True)

    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name="Parent Category")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField("Brand Name", max_length=100)
    slug = models.SlugField("Brand Slug", max_length=100, unique=True, allow_unicode=True)
    description = models.TextField("Brand Description", blank=True, null=True)
    logo = models.ImageField("Brand Logo", upload_to="brands/", blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Category")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products", verbose_name="Brand")
    title = models.CharField("Product Name", max_length=200)
    slug = models.SlugField("Product Slug", max_length=200, unique=True, allow_unicode=True)
    description = models.TextField("Product Description", blank=True, null=True)
    price = models.DecimalField("Product Price", max_digits=10, decimal_places=2)
    discount_price = models.DecimalField("Discount Price", max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField("Stock Quantity", default=0)
    is_active = models.BooleanField("Is Active", default=True)
    main_image = models.ImageField("Main Image", upload_to="products/")
    created_at = models.DateTimeField("Created_at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated_at", auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name= "images", verbose_name="Product")
    image = models.ImageField("Image", upload_to="products/gallery/")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"