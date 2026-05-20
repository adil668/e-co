from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart

from .forms import CheckoutForm
from .models import OrderItem


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:detail")

    initial = {
        "full_name": request.user.get_full_name() or request.user.username,
        "email": request.user.email,
        "phone": request.user.profile.phone,
        "address": request.user.profile.address,
        "city": request.user.profile.city,
        "state": request.user.profile.state,
        "postal_code": request.user.profile.postal_code,
    }
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.subtotal = cart.subtotal
            order.cashback_earned = cart.cashback_total
            order.save()
            for item in cart.items.select_related("product"):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discount_price,
                    cashback=item.cashback_total,
                )
            cart.items.all().delete()
            messages.success(request, "Order placed successfully.")
            return redirect("orders:success", order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)
    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(request.user.orders.prefetch_related("items__product"), id=order_id)
    return render(request, "orders/order_success.html", {"order": order})
