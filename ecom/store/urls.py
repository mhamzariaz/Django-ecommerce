from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('product/<slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('user-profile/', views.view_user_profile, name='user-profile')
]
