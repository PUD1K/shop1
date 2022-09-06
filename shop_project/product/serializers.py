from dataclasses import field
from rest_framework import serializers

from .models import Category, Product   

#просто JSON представление
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )

class CategorySerializer(serializers.ModelSerializer):
    #формируется вложенный список - rest сам отберет связанные элементы с Category по id(один-ко-многим)
    products = ProductSerializer(many = True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            "get_absolute_url",
            'products',
        )

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            "get_absolute_url",
            'products',
        )