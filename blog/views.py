from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer


# View Yozish usuli
# 1. Function Based View
# 2. Class Based View

# Views Built-in Types
# View: APIView
# Generic
# ViewSet

class BlogListCreateAPIView(APIView):
    def get(self, request):
        # default
        blogs = Blog.objects.all()
        # serach
        title = request.query_params.get("title", None)
        desc = request.query_params.get("description", None)

        if title:
            blogs = blogs.filter(title__icontains=title)

        if desc:
            blogs = blogs.filter(description__icontains=desc)

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogRetriveUpdateDeleteAPIView(APIView):
    def get(self, requset, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        blog.delete()
        return Response({"success": "Blog deleted"}, status=status.HTTP_204_NO_CONTENT)

