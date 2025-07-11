from django.contrib import admin
from .models import Category, SubCategory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_by', 'created_at', 'updated_by', 'updated_at')
    list_filter = ('created_by', 'updated_by')
    search_fields = ('name', 'description')
    ordering = ('created_at',)
    list_per_page = 20

admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    ordering = ['id']
    list_per_page = 20

admin.site.register(SubCategory, SubCategoryAdmin)