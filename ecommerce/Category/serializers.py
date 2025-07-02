from rest_framework import serializers
from .models import Category , SubCategory

class CategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'