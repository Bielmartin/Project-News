from django.db.models import fields
from rest_framework import serializers
from .models import Category, News, Comment

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = '__all__'
        
class NewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = News
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Comment
        fields = '__all__'