# stripe api
import stripe 

# отсюда получаем секретный ключ stripe
from django.conf import settings
# отсюда получаем данные нашего юзера
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import MyOrderSerializer, OrderSerializer

# вообще эти декораторы, если мы пользуемся представлениями на основе функций
# мы хотим использовать именно post запрос 
@api_view(['POST'])

# схемы аутентификации
# мы хотим использовать аутентификацию
@authentication_classes([authentication.TokenAuthentication])
# проверяем, аутентифириировался ли юзер
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    # помещаем в сериалайзер данные с запроса
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        # интегрируем апишку
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # сумма к оплате =  количество товара  * цена товара                    для всех товаров внутри сериализатора
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            # оплата
            charge = stripe.Charge.create(
                amount = int(paid_amount * 100), 
                currency='USD',
                description = "Charge from ThingsShop",
                # источник = stipe token, который приходит с фронта
                source = serializer.validated_data['stripe_token']
            )
            # если нет ошибок, значит все отлично, идем дальше
            # метод save вызывает метод create у serializer
            serializer.save(user=request.user, paid_amount=paid_amount)
            # респонсим на сервак что все успешно и возвращаем данные сериализатора
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderList(APIView):
    # классы аутентификации
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):    
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)