from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer

# сериализатор экземпляра товара в заказе
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        # модель, которую мы берем за основу
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",  
        )


# сериализатор экземпляра товара в заказе
class MyOrderItemSerializer(serializers.ModelSerializer):
    # для воизбежания ошибок
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",  
        )

class MyOrderSerializer(serializers.ModelSerializer):
    #формируется вложенный список - rest сам отберет связанные элементы по вторичному ключу(один-ко-многим)
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "place",
            "phone",
            "items",
            "stripe_token",
            "paid_amount"
        )
# сериализатор заказа
class OrderSerializer(serializers.ModelSerializer):
    #формируется вложенный список - rest сам отберет связанные элементы по вторичному ключу(один-ко-многим)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "place",
            "phone",
            "items",
            "stripe_token"
        )
    
    def create(self, validated_data):
        # помещаем validated_data без items в items_data 
        items_data = validated_data.pop('items')
        # создаем новый Order Ппомещая в него validated_data
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            # создаем OrderItem, вторичный ключ = order, данные = items_data 
            OrderItem.objects.create(order=order, **item_data)

        return order