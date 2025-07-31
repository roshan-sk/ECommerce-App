from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from utils.email_utils import send_order_email
from .permissions import IsAdminUser
from products.models import Product
from .models import *
from .serializers import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return Response({"message": "Product added to cart."}, status=200)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, product_id):
        quantity = request.data.get("quantity")
        if quantity is None:
            return Response({"error": "Quantity is required."}, status=400)

        try:
            quantity = int(quantity)
            if quantity < 0:
                return Response({"error": "Quantity cannot be negative."}, status=400)
        except ValueError:
            return Response({"error": "Quantity must be an integer."}, status=400)

        # Get cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=404)

        # Get product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        # Check if product is in cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            return Response({"error": "Product is not in your cart."}, status=404)

        if quantity == 0:
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=200)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            "message": "Cart item updated.",
            "product": product.name,
            "new_quantity": quantity
        }, status=200)



class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            cart = user.cart
        except Cart.DoesNotExist:
            return Response({"message": "Cart is empty"}, status=200)

        items = cart.items.all().order_by('-id')  # Descending
        paginator = StandardResultsSetPagination()
        paginated_items = paginator.paginate_queryset(items, request)

        item_list = []
        total_price = 0
        total_products = 0

        for item in paginated_items:
            product = item.product
            quantity = item.quantity
            price = product.price * quantity
            item_list.append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": quantity,
                "price_per_unit": float(product.price),
                "total_price": float(price)
            })
            total_price += price
            total_products += quantity

        return paginator.get_paginated_response({
            "user": user.username,
            "total_products": total_products,
            "total_price": float(total_price),
            "items": item_list
        })



class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            cart = user.cart
            if not cart.items.exists():
                return Response({"error": "Cart is empty"}, status=400)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

        total = 0
        order = Order.objects.create(user=user, total_price=0)  # temp 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_order=item.product.price
            )
            total += item.product.price * item.quantity
            # Update stock
            item.product.stock -= item.quantity
            item.product.save()

        order.total_price = total
        order.save()

        items = order.items.all()
        context = {"user": request.user, "order": order, "items": items}
        send_order_email(
            user_email=request.user.email,
            subject="Order Confirmation",
            template="emails/order_confirmation.html",
            context=context
        )

        cart.items.all().delete()  # clear cart

        return Response({"message": "Order placed successfully."}, status=201)
    
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, order_id):
        status = request.data.get("status")
        if status not in ['pending', 'shipped', 'delivered']:
            return Response({"error": "Invalid status"}, status=400)

        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            context = {"user": order.user, "order": order}
            send_order_email(
                user_email=order.user.email,
                subject=f"Order #{order.id} Status Updated",
                template="emails/order_status_update.html",
                context=context
            )

            return Response({
                "message": f"Order status updated to {status}",
                "order_id": order.id,
                "status": order.status,
                "updated_at": order.updated_at
            }, status=200)

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        

# List all orders (admin only)
class AllOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        status_filter = request.query_params.get('status')
        orders = Order.objects.all().order_by('-created_at')

        if status_filter in ['pending', 'shipped', 'delivered']:
            orders = orders.filter(status=status_filter)

        paginator = StandardResultsSetPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)


# User's own order history
class UserOrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status', '').lower()
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        if status_filter in ['pending', 'shipped', 'delivered']:
            orders = orders.filter(status=status_filter)

        paginator = StandardResultsSetPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)


# Get single order
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            if order.user != request.user and not request.user.is_admin:
                return Response({"error": "Unauthorized"}, status=403)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)