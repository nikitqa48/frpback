from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Branch)
class AdminBranch(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    class Meta:
        model = Branch

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    class Meta:
        model = Product
        fields = '__all__'

@admin.register(ProductPhoto)
class AdminProductPhoto(admin.ModelAdmin):
    class Meta:
        model = ProductPhoto

@admin.register(Company)
class AdminCompany(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    class Meta:
        model = Company
    