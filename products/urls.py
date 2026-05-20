from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="list"),
    path("products/<slug:slug>/", views.product_detail, name="detail"),
    path("search/suggestions/", views.search_suggestions, name="search_suggestions"),
]
