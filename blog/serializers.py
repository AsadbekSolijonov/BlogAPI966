from rest_framework import serializers
from blog.models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'description']


class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['id']


class BlogCreateSerizlier(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
