from django.http import Http404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response  
from rest_framework.decorators import api_view  


from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, CategoriesSerializer


#методы взаимодействия с объектами через сериализаторы
class LatestProductsList(APIView):
    def get(self, request, format=None):
        #отобрали 4 первых объекта из бдшки
        products = Product.objects.all()[0:4]
        #пихнули их в сериализатор
        serialazer = ProductSerializer(products, many=True)
        #ответ: данные сериализатора
        return Response(serialazer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serialazer = ProductSerializer(product)
        return Response(serialazer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug = category_slug)
        except:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serialazer = CategorySerializer(category)
        return Response(serialazer.data)

class AllCategory(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    #во фронте с помощью get запроса из url вытащили ключевое слово
    #по которому нужно производить поиск и поместили это слово в 'query'
    query = request.data.get('query','')
    #equals: select * from Product where name ILIKE "%query%" or description ILIKE "%query%"
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serialazer = ProductSerializer(products, many=True)
        return Response(serialazer.data)
    else: 
        return Response({"products": []})