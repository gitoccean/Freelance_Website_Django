# pip install djangorestframework
# go to settings and put named 'rest_framework' as put app name in installed app


from rest_framework import serializers
from .models import Jobs, Book


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
