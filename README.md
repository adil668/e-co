# NovaMart - Professional Django Ecommerce Web Application

NovaMart is a full-featured ecommerce web application built for a final-year college project, portfolio showcase and GitHub submission. It uses Django, Bootstrap 5, custom CSS, JavaScript and SQLite to deliver an Amazon/Flipkart-inspired shopping experience.

## Features

- Modern responsive ecommerce homepage with sticky navbar, hero carousel, categories, featured products, trending products, cashback offers, newsletter and footer
- User authentication with login, register, logout, remember me, password visibility toggles and profile management
- Product catalog with categories, product gallery support, discounts, cashback, ratings, stock, brands, tags and specifications
- Product listing with search, category filters, price filters, sorting and live search suggestions
- Premium product detail page with image gallery, zoom effect, stock status, delivery info, reviews and related products
- Cart system with AJAX add-to-cart, quantity updates, dynamic totals and toast notifications
- Wishlist system with AJAX toggle support
- Checkout flow with shipping form, demo payment method UI, order summary and success page
- Cashback badges, offer modal and JavaScript countdown timer
- Professional Django admin configuration with image previews and organized model management
- Professional demo catalog with remote ecommerce product photos, gallery images and uploaded media fallback
- SQLite database, reusable templates, static/media settings and modular apps

## Tech Stack

- Python
- Django 6
- HTML5, CSS3, JavaScript
- Bootstrap 5 and Bootstrap Icons
- SQLite

## Project Structure

```text
ecommerce_project/
├── cart/
├── orders/
├── products/
├── users/
├── templates/
├── static/
│   ├── css/
│   └── js/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

The `seed_demo` command creates realistic demo categories such as smartphones, laptops, headphones, smart watches, shoes, fashion, gaming accessories and cameras. Products include Unsplash demo image URLs, multiple gallery images, discounts, ratings and cashback values. You can replace these with uploaded media from the Django admin panel.

Open the project at:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## Screenshots

Add screenshots after running the project:

- Homepage
- Product listing
- Product detail
- Cart
- Checkout
- Admin dashboard

## Notes

This project intentionally uses a demo payment UI only. It does not integrate real payment gateways and is intended for college evaluation, portfolio presentation and learning.
