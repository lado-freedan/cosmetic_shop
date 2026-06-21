from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)
    
    @action(detail=False, methods=["post"], url_path="add-item")
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer = CartItemSerializer(data=self.request.data)

        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data.get("quantity", 1)
            product = Product.objects.get(id=product_id)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["delete"], url_path="remove_item/(?P<item_id>[0-9]+)")
    def remove_item(self, request, item_id=None):
        cart, _ =Cart.objects.get_or_create(user=self.request.user)
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order = Order.objects.create(
                user=self.request.user,
                total_price=cart.total_price() if callable(cart.total_price) else cart.total_price,
                status="pending"
            )

            for item in cart_items:
                product = item.product

                if product.stock < item.quantity:
                    return Response(
                        {"error": f"Not enough stock for {product.title}."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                product.stock -= item.quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item.quantity
                )
            
            cart_items.delete()
        
        return Response(
            {"message": "order is set.", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )