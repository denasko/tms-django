from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from shop.forms import RegistrationForm, UserUpdateForm

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
def add_to_cart(request: HttpResponse, product_id: Product.pk) -> str:
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
    messages.success(request, f'Product added:  {product.product_name}')
    return redirect('shop:product', product_id=product_id)


@login_required
def my_cart(request: HttpResponse) -> str:
    categories = Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    order: Order = Order.objects.filter(profile=profile, status=Order.Status.INITIAL).first()

    if not order:
        order: Order = Order.objects.create(profile=profile, status=Order.Status.INITIAL)
    order_entry = OrderEntry.objects.filter(order=profile.shopping_cart).order_by('product')
    total_amount = sum(entry.count * entry.product.price for entry in order_entry)
    print(total_amount)
    data = {
        'order': order,
        'total_amount': total_amount,
        'categories': categories,
        'entries': order_entry
    }
    return render(request, 'shop/my_cart.html', context=data)


@login_required
def update_quantity(request: HttpResponse) -> str:
    """
        Обновляет количество продукта в корзине пользователя.
    """
    entry_id = request.POST.get('entry_id')
    quantity = request.POST.get('quantity')
    entry = OrderEntry.objects.get(id=entry_id)
    entry.count = quantity
    entry.save()
    return redirect('shop:my_cart')


@login_required
def remove_entry(request: HttpResponse) -> str:
    """
        Удаляет запись о продукте из корзины пользователя.
    """
    entry_id = request.POST.get('entry_id')
    entry = OrderEntry.objects.get(id=entry_id)
    entry.delete()
    return redirect('shop:my_cart')


@login_required
def clear_cart(request: HttpResponse) -> str:
    """
        Очищает все продукты из корзины пользователя.
    """
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.filter(profile=profile, status=Order.Status.INITIAL).first()
    if order:
        OrderEntry.objects.filter(order=profile.shopping_cart).delete()
    return redirect('shop:my_cart')


@login_required
def process_order(request: HttpResponse) -> str:
    """
    Обрабатывает заказ пользователя, создавая новый заказ с продуктами из корзины покупок.
    """
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.create(profile=profile, status=Order.Status.COMPLETED)
        if profile.shopping_cart.order_entries.exists():
            entries = profile.shopping_cart.order_entries.all()
            for entry in entries:
                order.order_entries.create(product=entry.product, count=entry.count)
            profile.shopping_cart.order_entries.all().delete()
            data = {
                'order': order
            }
            return render(request, 'shop/order_success.html', context=data)

    return redirect('shop:my_cart')


@login_required
def user_profile(request):
    """
        Отображает информацию о профиле пользователя и последние заказы.
    """
    categories = Category.objects.all()
    user = request.user
    orders = Order.objects.filter(profile=user.profile).order_by('-id')[:5]
    for order in orders:
        entries = order.order_entries.all()
        total_quantity = sum(entry.count for entry in entries)
        order.total_quantity = total_quantity

        total_amount = sum(entry.product.price * entry.count for entry in entries)
        order.total_amount = total_amount
        order.save()
    data = {
        'user': user,
        'orders': orders,
        'categories': categories
    }
    return render(request, 'shop/user_profile.html', context=data)


@login_required
def order_history(request):
    """
        Отображает историю заказов пользователя с пагинацией.
    """
    categories = Category.objects.all()
    orders = Order.objects.filter(profile=request.user.profile).order_by('-id')
    paginator = Paginator(orders.all(), 7)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    for order in orders:
        entries = order.order_entries.all()
        order.total_quantity = sum(entry.count for entry in entries)
        order.total_amount = sum(entry.product.price * entry.count for entry in entries)
        order.product_links = [reverse('shop:product', args=[entry.product.id]) for entry in entries]
    data = {
        'orders': orders,
        'categories': categories
    }
    return render(request, 'shop/order_history.html', context=data)


@login_required
def update_profile(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('shop:user_profile')

    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'shop/update_user_profile.html',
                  {'user_form': user_form, 'categories': categories})


@login_required
def repeat_order(request, order_id):
    """
        Обрабатывает заказ пользователя, создавая новый заказ с продуктами из корзины покупок.
    """
    order = get_object_or_404(Order, id=order_id, profile=request.user.profile)
    OrderEntry.objects.filter(order=request.user.profile.shopping_cart).delete()
    for entry in order.order_entries.all():
        OrderEntry.objects.create(order=request.user.profile.shopping_cart, product=entry.product, count=entry.count)

    return redirect('shop:my_cart')


def about(request: HttpResponse) -> str:
    return render(request, 'shop/about.html')


def add_product(request) -> str:
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)


def feedback(request) -> str:
    products = Product.objects.all().order_by('category')
    category = Category.objects.all()
    data = {'title': 'main page',
            'products': products,
            'category': category
            }
    return render(request, 'shop/index.html', context=data)
