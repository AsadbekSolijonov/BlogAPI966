from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Blog


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ["id", "username", "full_name"]


class BlogSerializer(serializers.ModelSerializer):  # CRUD
    characters = serializers.SerializerMethodField()
    words = serializers.SerializerMethodField()
    author = UserSerializer()

    # author = serializers.SerializerMethodField()  # read_only=True

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'created', 'updated', 'characters', "words", "author"]

    def get_characters(self, obj):
        return len(obj.description)

    def get_words(self, obj):
        return len(obj.description.split())

    # def get_author(self, obj):
    #     return obj.author.username
