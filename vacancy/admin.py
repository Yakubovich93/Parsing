from django.contrib import admin

from .forms import ProductForm
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'company', 'link')
    list_filter = ('date',)
    search_fields = ('company',)
    ordering = ('date',)
    form = ProductForm