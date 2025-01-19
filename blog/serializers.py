from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Blog


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ["id", "username", "full_name"]


class BlogSerializer(serializers.ModelSerializer):  # CRUD
    characters = serializers.SerializerMethodField()
    words = serializers.SerializerMethodField()
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author = UserSerializer(read_only=True)

    # author_info = serializers.SerializerMethodField()  # read_only=True

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'created', 'updated', 'characters', "words", "author"]

    def get_characters(self, obj):
        return len(obj.description)

    def get_words(self, obj):
        return len(obj.description.split())

    # def get_author_info(self, obj):
    #     detail = {
    #         "id": obj.author.id,
    #         "username": obj.author.username,
    #         "full_name": obj.author.first_name + " " + obj.author.last_name
    #     }
    #     return detail
