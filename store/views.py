from django.shortcuts import render, HttpResponse
from .models import *
import json
from django.http import JsonResponse
import datetime
from .utils import cookiesCart, cartData


def store(request):
    data = cartData(request)
    cartItem = data['cartItem']

    products = Product.objects.all()
    context = {'products': products, 'cartItem': cartItem}
    return render(request, 'store/store.html', context)


def view(request, pk_test):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cookieData = cookiesCart(request)
        cartItem = cookieData['cartItem']
        order = cookieData['order']
        items = cookieData['items']

    products = Product.objects.get(id=pk_test)
    context = {'products': products,
               'items': items,
               'cartItem': cartItem,
               'order': order,
               }
    return render(request, 'store/view.html', context)


def checkout(request):

    data = cartData(request)
    cartItem = data['cartItem']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'store/checkout.html', context)


def cart(request):
    data = cartData(request)
    cartItem = data['cartItem']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'store/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("action", action)
    print("productId", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
