from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField
from rest_framework import serializers
from .models import *

class BranchSerialize(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class CompanySerialize(ModelSerializer):
    # branch = BranchSerialize()
    class Meta:
        model = Company
        lookup_field = 'slug'
        fields = '__all__' 
    
class ProductSerialize(ModelSerializer):
    organisation = CompanySerialize()
    class Meta:
        model = Product
        fields = '__all__'

class ProductSerializeNoCompany(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PhotoSerialize(ModelSerializer):
    # product = ProductSerialize()
    class Meta:
        model = ProductPhoto
        fields = ('image',)

class ProductPhotoSerialize(ModelSerializer):
    product = ProductSerialize()
    class Meta:
        model = ProductPhoto
        fields = '__all__'

