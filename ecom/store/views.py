from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
import stripe

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


def index(request):
    product = Product.objects.all()
    return render(request, 'store/home.html', {'products': product})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_slug = self.kwargs['slug']
        product = Product.objects.get(slug=product_slug)
        description = product.description
        context['product'] = product
        context['description'] = description.split(',')
        return context


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item updated to your cart.")
            return redirect("order-summary")
        else:
            order.products.add(order_item)
            messages.info(request, "This item was added from your cart.")
            return redirect("order-summary")
    else:
        order = Order.objects.create(
            user=request.user)
        order.products.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product-detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product-detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product-detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product-detail", slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'store/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class CheckoutView(View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'store/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address1 = form.cleaned_data.get('address1')
                address2 = form.cleaned_data.get('address2')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user=self.request.user,
                    address1=address1,
                    address2=address2,
                    country=country,
                    zip_code=zip_code,
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == 'Card':
                    return redirect('payment', payment_option='card')
                else:
                    return redirect('payment', payment_option='cod')

        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect('order-summary')

        return redirect('checkout')


class PaymentView(View):

    def get(self, *args, **kwargs):
        form = PaymentForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }

        return render(self.request, 'store/payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = order.get_total()
        payment = Payment(
            user=self.request.user,
            amount=amount
        )
        payment.save()
        order_products = order.products.all()
        order_products.update(ordered=True)
        for product in order_products:
            product.save()

        order.ordered = True
        order.payment = payment
        order.save()
        messages.success(self.request, 'Your order has been placed successfully')
        return redirect('/')


def view_user_profile(request):

    orders = Order.objects.filter(user=request.user)
    for order in orders:
        for product in order.products.all():
            print(product.product.name)

    context = {
        'orders': orders
    }
    return render(request, 'store/user-profile.html', context)

