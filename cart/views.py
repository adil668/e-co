from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .models import Cart, CartItem, Wishlist


def _cart_for(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = _cart_for(request.user)
    return render(request, "cart/cart.html", {"cart": cart})


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _cart_for(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "message": f"{product.name} added to cart",
                "cart_count": cart.total_items,
                "cart_total": f"{cart.subtotal:.2f}",
            }
        )
    messages.success(request, f"{product.name} added to cart.")
    if request.POST.get("next") == "checkout":
        return redirect("orders:checkout")
    return redirect(request.META.get("HTTP_REFERER", "cart:detail"))


@login_required
@require_POST
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    item.quantity = min(quantity, item.product.stock_quantity or quantity)
    item.save()
    cart = item.cart
    return JsonResponse(
        {
            "ok": True,
            "item_total": f"{item.line_total:.2f}",
            "cart_total": f"{cart.subtotal:.2f}",
            "cashback_total": f"{cart.cashback_total:.2f}",
            "cart_count": cart.total_items,
        }
    )


@login_required
@require_POST
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart:detail")


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
    count = Wishlist.objects.filter(user=request.user).count()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "added": created,
                "wishlist_count": count,
                "message": "Added to wishlist" if created else "Removed from wishlist",
            }
        )
    return redirect(request.META.get("HTTP_REFERER", "products:home"))


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product", "product__category")
    return render(request, "cart/wishlist.html", {"items": items})
