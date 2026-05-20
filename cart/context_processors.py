from .models import Cart, Wishlist


def cart_summary(request):
    if not request.user.is_authenticated:
        return {"cart_count": 0, "wishlist_count": 0}
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return {
        "cart_count": cart.total_items,
        "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
    }
