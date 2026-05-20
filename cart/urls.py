from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add"),
    path("update/<int:item_id>/", views.update_cart_item, name="update"),
    path("remove/<int:item_id>/", views.remove_cart_item, name="remove"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
]
