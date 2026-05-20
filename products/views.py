from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import CashbackOffer, Category, Product


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    trending_products = Product.objects.filter(is_trending=True)[:8]
    flash_sale_products = Product.objects.filter(discount_percentage__gte=15).order_by("-discount_percentage")[:8]
    categories = Category.objects.filter(is_featured=True)[:8]
    category_sections = (
        Category.objects.prefetch_related("products")
        .filter(products__isnull=False)
        .distinct()
        .order_by("name")
    )
    offers = CashbackOffer.objects.filter(is_active=True, valid_until__gt=timezone.now())[:3]
    return render(
        request,
        "products/home.html",
        {
            "featured_products": featured_products,
            "trending_products": trending_products,
            "flash_sale_products": flash_sale_products,
            "categories": categories,
            "category_sections": category_sections,
            "offers": offers,
            "popular_brands": ["Apple", "Samsung", "Sony", "Nike", "ASUS", "Canon", "Logitech G", "PlayStation"],
        },
    )


def product_list(request):
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort", "latest")

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(brand__icontains=query)
            | Q(tags__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_map = {
        "price_low": "price",
        "price_high": "-price",
        "rating": "-rating",
        "discount": "-discount_percentage",
        "latest": "-created_at",
    }
    products = products.order_by(sort_map.get(sort, "-created_at"))

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "category_sections": categories.prefetch_related("products"),
            "query": query,
            "selected_category": category_slug,
            "sort": sort,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(id=product.id)
        .order_by("-rating")[:4]
    )
    return render(
        request,
        "products/product_detail.html",
        {"product": product, "related_products": related_products},
    )


def search_suggestions(request):
    query = request.GET.get("q", "").strip()
    results = []
    if len(query) >= 2:
        results = list(
            Product.objects.filter(name__icontains=query)
            .values("name", "slug")[:8]
        )
    return JsonResponse({"results": results})
