from decimal import Decimal

from django.db.models import Q

from products.models import CashbackOffer, Category, Product


class StorefrontSearchService:
    """Answers basic ecommerce questions from the live storefront database."""

    PRODUCT_TERMS = {
        "product",
        "products",
        "item",
        "items",
        "catalog",
        "shop",
        "shopping",
        "available",
        "stock",
    }
    CATEGORY_TERMS = {"category", "categories", "department", "departments"}
    OFFER_TERMS = {"offer", "offers", "deal", "deals", "discount", "cashback", "sale"}

    def answer(self, question: str) -> dict | None:
        normalized = question.casefold()
        words = set(normalized.replace("/", " ").replace("-", " ").split())

        product_matches = self._matching_products(normalized)
        if product_matches:
            return self._product_answer(product_matches, "matching products")

        if words & self.CATEGORY_TERMS:
            categories = Category.objects.order_by("name")[:10]
            return self._category_answer(categories)

        if words & self.OFFER_TERMS:
            return self._offer_answer()

        if words & self.PRODUCT_TERMS:
            products = Product.objects.select_related("category").order_by("-created_at")[:6]
            return self._product_answer(products, "latest products")

        category_matches = self._matching_categories(normalized)
        if category_matches:
            return self._category_answer(category_matches)

        return None

    @staticmethod
    def _matching_products(query: str):
        if len(query) < 2:
            return Product.objects.none()

        return (
            Product.objects.select_related("category")
            .filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(brand__icontains=query)
                | Q(tags__icontains=query)
                | Q(category__name__icontains=query)
            )
            .order_by("-rating", "-created_at")[:6]
        )

    @staticmethod
    def _matching_categories(query: str):
        if len(query) < 2:
            return Category.objects.none()

        return Category.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by("name")[:6]

    def _product_answer(self, products, label: str) -> dict | None:
        products = list(products)
        if not products:
            return None

        lines = [f"I found these {label}:"]
        matches = []
        for product in products:
            stock = "in stock" if product.in_stock else "out of stock"
            category = product.category.name if product.category_id else "General"
            lines.append(
                f"- {product.name}: Rs. {self._money(product.discount_price)} "
                f"({category}, {stock}, rating {product.rating}/5)"
            )
            matches.append(
                {
                    "id": f"product-{product.id}",
                    "content": product.description,
                    "metadata": {
                        "title": product.name,
                        "source_type": "product",
                        "source_url": product.get_absolute_url(),
                    },
                    "score": 1.0,
                }
            )

        lines.append("Open Products from the navbar to filter, sort, or add items to cart.")
        return {"answer": "\n".join(lines), "matches": matches}

    @staticmethod
    def _category_answer(categories) -> dict | None:
        categories = list(categories)
        if not categories:
            return None

        lines = ["Available categories:"]
        matches = []
        for category in categories:
            description = f" - {category.description}" if category.description else ""
            lines.append(f"- {category.name}{description}")
            matches.append(
                {
                    "id": f"category-{category.id}",
                    "content": category.description or category.name,
                    "metadata": {
                        "title": category.name,
                        "source_type": "category",
                        "source_url": f"/products/?category={category.slug}",
                    },
                    "score": 1.0,
                }
            )
        return {"answer": "\n".join(lines), "matches": matches}

    @staticmethod
    def _offer_answer() -> dict | None:
        offers = list(CashbackOffer.objects.filter(is_active=True).order_by("-valid_until")[:5])
        if not offers:
            discounted = Product.objects.filter(discount_percentage__gt=0).order_by(
                "-discount_percentage"
            )[:5]
            if not discounted:
                return {"answer": "There are no active offers right now.", "matches": []}

            lines = ["Current product discounts:"]
            for product in discounted:
                lines.append(f"- {product.name}: {product.discount_percentage}% off")
            return {"answer": "\n".join(lines), "matches": []}

        lines = ["Current offers:"]
        matches = []
        for offer in offers:
            lines.append(
                f"- {offer.title}: {offer.percentage}% cashback above "
                f"Rs. {StorefrontSearchService._money(offer.minimum_order_value)}"
            )
            matches.append(
                {
                    "id": f"offer-{offer.id}",
                    "content": offer.description,
                    "metadata": {"title": offer.title, "source_type": "offer"},
                    "score": 1.0,
                }
            )
        return {"answer": "\n".join(lines), "matches": matches}

    @staticmethod
    def _money(value: Decimal) -> str:
        return f"{value:.2f}"


def get_storefront_search_service() -> StorefrontSearchService:
    return StorefrontSearchService()
