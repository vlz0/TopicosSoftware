from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from django.contrib import messages
from tienda.models import Product
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse
import stripe
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


def add_to_cart(request):
    cart_product = {}
    qty = int(request.GET['qty'])
    price = float(request.GET['price'])

    total_price = qty * price

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'total_price': total_price,
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            try:
                # Intenta convertir el precio a float
                price = float(item['price'])
                qty = int(item['qty'])
                # Suma el costo total del producto al total del carrito
                cart_total_amount += qty * price
            except ValueError:
                # Maneja el caso en que el precio no sea un número válido
                pass

        context = {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'cart.html', context)
    else:
        messages.success(request, "El carrito está vacío")
        return redirect('home')


def cart_delete(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            try:
                # Intenta convertir el precio a float
                price = float(item['price'])
                qty = int(item['qty'])
                # Suma el costo total del producto al total del carrito
                cart_total_amount += qty * price
            except ValueError:
                # Maneja el caso en que el precio no sea un número válido
                pass

    context = render_to_string("cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(
        request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, })
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        if product_id and action:
            if 'cart_data_obj' in request.session:
                cart_data = request.session['cart_data_obj']
                if product_id in cart_data:
                    if action == 'add':
                        cart_data[product_id]['qty'] = str(
                            int(cart_data[product_id]['qty']) + 1)
                        cart_data[product_id]['total_price'] = str(
                            float(cart_data[product_id]['qty']) * float(cart_data[product_id]['price']))
                    elif action == 'subtract':
                        # Restar la cantidad y verificar si es cero
                        cart_data[product_id]['qty'] = str(
                            int(cart_data[product_id]['qty']) - 1)
                        if int(cart_data[product_id]['qty']) == 0:
                            # Eliminar el producto del carrito si la cantidad es cero
                            del cart_data[product_id]
                        else:
                            # Actualizar el precio total del producto si la cantidad no es cero
                            cart_data[product_id]['total_price'] = str(
                                float(cart_data[product_id]['qty']) * float(cart_data[product_id]['price']))
                    request.session['cart_data_obj'] = cart_data
    return redirect('cart_view')


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        # Crear una lista de productos para la sesión de pago de Stripe
        cart = request.session.get('cart_data_obj', {})

        if not cart:  # Verificar si el carrito está vacío
            messages.error(request, "Tu carrito está vacío.")
            return JsonResponse({'error': 'Tu carrito está vacío.'}, status=400)

        # Dominio de la aplicación o localhost si no hay un dominio configurado
        # domain = 'https://' + settings.ALLOWED_HOSTS[0]
        # if settings.DEBUG:
        #     domain = 'http://127.0.0.1:8080'

        domain = 'http://' + request.get_host()

        line_items = []  # Crear una lista de productos para la sesión de pago de Stripe
        #product_ids = []  # Crear una lista de IDs de productos para la metadata de Stripe
        purchased_items = []
        for product_id, item in cart.items():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['title'],
                    },
                    # Stripe espera el monto en centavos
                    'unit_amount': int(float(item['price']) * 100),
                },
                'quantity': item['qty'],
            })
            # Agregar el ID del producto a la lista
            # product_ids.append(product_id)
            purchased_items.append({  # Agregar detalles del producto a la lista
                'title': item['title'],
                'qty': item['qty'],
                'price': item['price']
            })
        try:
            # Crear la sesión de pago de Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=domain + reverse('success'),
                cancel_url=domain + reverse('home'),
                metadata={
                    "stripe_product_ids": ",".join(cart.keys())},
            )
            request.session['purchased_items'] = purchased_items
            # Devolver la ID de la sesión de pago de Stripe
            return JsonResponse({"id": session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class SuccessView(TemplateView):
    template_name = 'payment/success.html'

    def get(self, request, *args, **kwargs):
        if 'cart_data_obj' in request.session:
            # Limpiar el carrito despues de una compra exitosa
            del request.session['cart_data_obj']
            request.session.save()
        messages.success(request, "Pago exitoso!")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchased_items = self.request.session.pop('purchased_items', [])
        if purchased_items:
            context['purchased_items'] = purchased_items
            self.request.session.save()  
        else:
            pass
            messages.error(self.request, "No se encontraron detalles de productos comprados.")
        return context


@csrf_exempt
def stripe_webhook(request, *args, **kwargst):

    CHECKOUT_SESSION_COMPLETED = 'checkout.session.completed'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    # print(event)
    # Handle the event checkout.session.completed
    if event['type'] == CHECKOUT_SESSION_COMPLETED:
        # print(event)
        # Accedemos a los productos pagados
        session_product_ids = event['data']['object']['metadata']['stripe_product_ids']
        product_ids = session_product_ids.split(',')
        print(product_ids)

        # Fulfill the purchase...
        # Logica para manejar la compra -> asignar a un cliente o realizar el envio . . .
        pass

    return HttpResponse(status=200)
