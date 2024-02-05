from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from shop.models import Product, Category, Order, OrderEntry, Profile


@cache_page(3)
def index(request: HttpResponse):
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)


def show_product(request: HttpResponse, product_id: int) -> str:
    product = get_object_or_404(Product, pk=product_id)
    new_price = 0
    if product.sale != 0:
        new_price: float = product.price / 100 * (100 - product.sale)
    data = {'product': product,
            'new_price': round(new_price, 2),
            'sale': product.sale}
    return render(request, 'shop/product.html', context=data)


def show_category(request: HttpResponse, category_name: str) -> str:
    category = get_object_or_404(Category, category_name=category_name)
    products = Product.objects.filter(category_id=category.pk)
    data = {'products': products,
            'category': category}
    return render(request, 'shop/category.html', context=data)


@login_required
def add_to_cart(request: HttpResponse, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = Profile.objects.get(user=request.user)
    if not profile.shopping_cart:
        order = Order.objects.create(profile=profile)
        profile.shopping_cart = order
        profile.save()
    else:
        order = profile.shopping_cart
    order_entry, created = OrderEntry.objects.get_or_create(order=order, product=product)
    if not created:
        order_entry.count += 1
        order_entry.save()

    return redirect('shop:product', product_id=product_id)


@login_required
def my_cart(request: HttpResponse):
    categories = Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.filter(profile=profile, status=Order.Status.INITIAL).first()
    if not order:
        order = Order.objects.create(profile=profile, status=Order.Status.INITIAL)
    entries = order.order_entries.all().order_by('product_id')
    total_amount = sum(entry.count * entry.product.price for entry in order.order_entries.all())
    print(entries)
    return render(request, 'shop/my_cart.html',
                  {'order': order, 'total_amount': total_amount, 'categories': categories, 'entries': entries})


def about(request: HttpResponse):
    return render(request, 'shop/about.html')


def add_product(request):
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)


def feedback(request):
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)


def login(request):
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)
