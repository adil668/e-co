from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from products.models import CashbackOffer, Category, Product, ProductImage


class Command(BaseCommand):
    help = "Create professional demo categories, products, galleries and cashback offers."

    def handle(self, *args, **options):
        categories = [
            ("Smartphones", "Flagship and mid-range mobile phones", "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=80"),
            ("Laptops", "Performance laptops for work, study and gaming", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"),
            ("Headphones", "Wireless audio, earbuds and studio headphones", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80"),
            ("Smart Watches", "Fitness and lifestyle smart wearables", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80"),
            ("Shoes", "Sneakers and sport shoes for everyday style", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80"),
            ("Fashion", "Premium clothing and lifestyle fashion", "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=900&q=80"),
            ("Gaming Accessories", "Keyboards, controllers, headsets and RGB gear", "https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&w=900&q=80"),
            ("Cameras", "Mirrorless cameras, lenses and creator gear", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80"),
        ]
        category_map = {}
        for name, description, image_url in categories:
            category, _ = Category.objects.update_or_create(
                name=name,
                defaults={"description": description, "image_url": image_url, "is_featured": True},
            )
            category_map[name] = category

        products = [
            {
                "name": "Galaxy Nova S24 Ultra 5G",
                "brand": "Samsung",
                "category": "Smartphones",
                "description": "A premium 5G smartphone with pro-grade camera, vivid AMOLED display and all-day battery life.",
                "price": "129999",
                "discount": 18,
                "cashback": 6,
                "stock": 24,
                "rating": "4.8",
                "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "6.8-inch AMOLED display\n200MP pro camera system\n12GB RAM and 256GB storage\n5000mAh battery with fast charging",
                "featured": True,
                "trending": True,
            },
            {
                "name": "iPhone 16 Pro Max",
                "brand": "Apple",
                "category": "Smartphones",
                "description": "A flagship iPhone experience with titanium design, advanced camera controls and smooth performance.",
                "price": "144900",
                "discount": 10,
                "cashback": 4,
                "stock": 16,
                "rating": "4.9",
                "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Super Retina XDR display\nA-series pro chipset\n48MP fusion camera\nMagSafe and USB-C support",
                "featured": True,
                "trending": True,
            },
            {
                "name": "MacBook Air M3 13-inch",
                "brand": "Apple",
                "category": "Laptops",
                "description": "Ultra-thin laptop for students and professionals with silent performance and exceptional battery life.",
                "price": "114900",
                "discount": 12,
                "cashback": 5,
                "stock": 12,
                "rating": "4.8",
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Apple M3 chip\n13.6-inch Liquid Retina display\n8GB unified memory\n256GB SSD storage",
                "featured": True,
                "trending": True,
            },
            {
                "name": "ROG Strix G16 Gaming Laptop",
                "brand": "ASUS",
                "category": "Laptops",
                "description": "High-refresh gaming laptop with powerful graphics, advanced cooling and RGB keyboard.",
                "price": "159990",
                "discount": 20,
                "cashback": 7,
                "stock": 9,
                "rating": "4.7",
                "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Intel Core i9 processor\nNVIDIA RTX graphics\n165Hz display\n16GB RAM and 1TB SSD",
                "featured": False,
                "trending": True,
            },
            {
                "name": "Sony WH-1000XM5 Headphones",
                "brand": "Sony",
                "category": "Headphones",
                "description": "Industry-leading noise cancellation with premium comfort and rich wireless audio.",
                "price": "34990",
                "discount": 22,
                "cashback": 8,
                "stock": 30,
                "rating": "4.7",
                "image_url": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Active noise cancellation\n30-hour battery life\nMultipoint Bluetooth\nPremium soft-fit earcups",
                "featured": True,
                "trending": True,
            },
            {
                "name": "AirPods Pro 2 Wireless Earbuds",
                "brand": "Apple",
                "category": "Headphones",
                "description": "Compact earbuds with adaptive audio, transparency mode and a pocket-ready charging case.",
                "price": "24900",
                "discount": 14,
                "cashback": 5,
                "stock": 44,
                "rating": "4.6",
                "image_url": "https://images.unsplash.com/photo-1606741965429-8d76ff50bb2f?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1603351154351-5e2d0600bb77?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Adaptive noise cancellation\nSpatial audio\nUSB-C charging case\nSweat and water resistant",
                "featured": False,
                "trending": True,
            },
            {
                "name": "Apple Watch Series 10",
                "brand": "Apple",
                "category": "Smart Watches",
                "description": "Elegant smartwatch with health insights, fitness tracking and a bright always-on display.",
                "price": "46900",
                "discount": 9,
                "cashback": 4,
                "stock": 25,
                "rating": "4.8",
                "image_url": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Always-on Retina display\nHeart and sleep tracking\nFast charging\nWater resistant design",
                "featured": True,
                "trending": False,
            },
            {
                "name": "Nike Air Max Pulse Sneakers",
                "brand": "Nike",
                "category": "Shoes",
                "description": "Street-ready sneakers with cushioned comfort, bold silhouette and premium materials.",
                "price": "13995",
                "discount": 25,
                "cashback": 6,
                "stock": 36,
                "rating": "4.5",
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Air cushioning\nRubber traction outsole\nBreathable mesh upper\nEveryday sport fit",
                "featured": True,
                "trending": True,
            },
            {
                "name": "Premium Denim Jacket",
                "brand": "Myntra Select",
                "category": "Fashion",
                "description": "A structured denim jacket with clean stitching, versatile styling and premium wash.",
                "price": "3999",
                "discount": 35,
                "cashback": 5,
                "stock": 52,
                "rating": "4.4",
                "image_url": "https://images.unsplash.com/photo-1523398002811-999ca8dec234?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Premium cotton denim\nRegular fit\nButton closure\nMachine washable",
                "featured": False,
                "trending": True,
            },
            {
                "name": "Logitech G Pro RGB Keyboard",
                "brand": "Logitech G",
                "category": "Gaming Accessories",
                "description": "Tournament-grade mechanical keyboard with responsive switches and customizable RGB lighting.",
                "price": "12995",
                "discount": 28,
                "cashback": 7,
                "stock": 18,
                "rating": "4.7",
                "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1595044426077-d36d9236d44a?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Mechanical switches\nProgrammable RGB\nDetachable cable\nCompact tournament layout",
                "featured": True,
                "trending": True,
            },
            {
                "name": "DualSense Wireless Controller",
                "brand": "PlayStation",
                "category": "Gaming Accessories",
                "description": "Immersive controller with adaptive triggers, haptic feedback and modern ergonomic design.",
                "price": "6990",
                "discount": 16,
                "cashback": 5,
                "stock": 40,
                "rating": "4.6",
                "image_url": "https://images.unsplash.com/photo-1607853202273-797f1c22a38e?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "Haptic feedback\nAdaptive triggers\nBuilt-in microphone\nUSB-C charging",
                "featured": False,
                "trending": False,
            },
            {
                "name": "Canon EOS R50 Creator Kit",
                "brand": "Canon",
                "category": "Cameras",
                "description": "Compact mirrorless camera kit for creators, travel photography and high-quality video.",
                "price": "75995",
                "discount": 15,
                "cashback": 6,
                "stock": 11,
                "rating": "4.7",
                "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=85",
                "gallery": [
                    "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=900&q=85",
                    "https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?auto=format&fit=crop&w=900&q=85",
                ],
                "specs": "24.2MP APS-C sensor\n4K video recording\nVari-angle touchscreen\nCreator kit lens included",
                "featured": True,
                "trending": False,
            },
        ]

        for data in products:
            product, _ = Product.objects.update_or_create(
                name=data["name"],
                defaults={
                    "brand": data["brand"],
                    "category": category_map[data["category"]],
                    "description": data["description"],
                    "price": Decimal(data["price"]),
                    "discount_percentage": data["discount"],
                    "cashback_percentage": data["cashback"],
                    "stock_quantity": data["stock"],
                    "rating": Decimal(data["rating"]),
                    "image_url": data["image_url"],
                    "specifications": data["specs"],
                    "tags": f"{data['brand']}, {data['category']}, premium, sale, deal",
                    "is_featured": data["featured"],
                    "is_trending": data["trending"],
                },
            )
            product.gallery.all().delete()
            for index, image_url in enumerate(data["gallery"], start=1):
                ProductImage.objects.create(
                    product=product,
                    image_url=image_url,
                    alt_text=f"{product.name} gallery image {index}",
                )

        offers = [
            ("Flash Sale Cashback", "Extra cashback on trending electronics, gaming gear and smart wearables.", 12, "1499.00", 3),
            ("Fashion Weekend Bonus", "Save more on shoes, jackets and campus-ready fashion picks.", 10, "999.00", 5),
            ("Creator Gear Deal", "Special rewards on cameras, laptops and accessories for creators.", 8, "4999.00", 7),
        ]
        for title, description, percentage, minimum, days in offers:
            CashbackOffer.objects.update_or_create(
                title=title,
                defaults={
                    "description": description,
                    "percentage": percentage,
                    "minimum_order_value": Decimal(minimum),
                    "valid_until": timezone.now() + timedelta(days=days),
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Professional demo ecommerce data created successfully."))
