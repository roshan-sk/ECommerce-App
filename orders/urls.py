from django.urls import path
from .views import *

urlpatterns = [
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='cart-add'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='cart-update'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('order/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
    path('order/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='order-status-update'),
    path('orders/all/', AllOrdersView.as_view(), name='all-orders'),
    path('orders/history/all/', UserOrderHistoryView.as_view(), name='user-order-history'),
    path('orders/history/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]
