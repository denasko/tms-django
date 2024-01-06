from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from shop.models import Product, Category


def index(request):
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)


def show_product(request: HttpResponse, product_id: int) -> str:
    product = get_object_or_404(Product, pk=product_id)
    sale = 0
    if product.sale != 0:
        sale = product.price/100*(100-product.sale)
    data = {'product': product,
            'sale': sale}
    return render(request, 'shop/product.html', context=data)


def show_category(request: HttpResponse, category_name: str) -> str:
    category = get_object_or_404(Category,category_name=category_name)
    print(category)
    products = Product.objects.filter(category_id=category.pk)
    data = {'products': products}
    return render(request, 'shop/category.html', context=data)


def about(request):
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)


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
