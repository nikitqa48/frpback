from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.db.models import Prefetch


class BranchView(ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerialize


class DetailBranchView(RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Branch.objects.all()
    serializer_class = BranchSerialize


class CompanyView(APIView):
    def get(self,request, slug):
        results = Company.objects.filter(branch__slug=slug)
        """Находим полный список компаний в конкретной отрасли"""
        list_company = list()
        for company in results:
            """Прокручиваем каждую компанию"""
            if isinstance(company, Company):
                my_list = list()
                ser = CompanySerialize(company, context={'request':request})
                """Сериализуем каждую компанию"""
                product = Product.objects.filter(organisation=company.id)[0:4]
                """Находим список продуктов каждой компании,  Максимум 4 продукта"""
                if product.exists():
                    """Если список не пустой"""
                    for item in product:
                        """Прокручиваем каждый продукт и вытаскиваем по одному фото"""
                        image = ProductPhoto.objects.filter(product=item)[0:1]
                        serialize_image = PhotoSerialize(image, many=True, context={'request': request})
                        serialize_product = ProductSerializeNoCompany(item)
                        """Сериализуем фото и продукт"""
                        my_list.append({'product':serialize_product.data, 'image':serialize_image.data})
                    list_company.append({'company': ser.data, 'product':my_list})
                    """Добавляем все в массив"""
        return Response(list_company)



class DetailCompanyView(RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Company.objects.all()
    serializer_class = CompanySerialize


class ProductCompanyView(APIView):
    def get(self, request, company):
        products = Product.objects.filter(organisation__slug=company)
        organisation_object = Company.objects.get(slug=company)
        organisation = CompanySerialize(organisation_object, context={'request':request})
        data = list()
        organisation_list = list()
        organisation_list.append({'organisation':organisation.data})
        for product in products:
            photo_list = list()
            photo = ProductPhoto.objects.filter(product=product)[0:4]
            serialize_product = ProductSerializeNoCompany(product, context={'request':request})
            for image in photo:
                serialize_photo = PhotoSerialize(image, context={'request':request})
                photo_list.append({'photo':serialize_photo.data})
            data.append({'product':serialize_product.data, 'image':photo_list})
        
        return Response({'data':data, 'organisation':organisation_list})

class ProductDetailView(APIView):
    def get(self, request, name):
        product = Product.objects.get(slug=name)
        photo = ProductPhoto.objects.filter(product=product)
        photo_serialize = PhotoSerialize(photo, many=True, context={'request':request})
        product_serialize = ProductSerialize(product, context={'request':request})
        return Response({'product':product_serialize.data, 'image':photo_serialize.data})