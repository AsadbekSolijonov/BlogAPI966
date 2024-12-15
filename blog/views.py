from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer
from rest_framework.decorators import api_view


# View Yozish usuli
# 1. Function Based View
# 2. Class Based View

# Views Built-in Types
# View: APIView
# Generic
# ViewSet

class BlogListCreateAPIView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
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


@api_view(['GET'])
def search_blogs(request):
    # /api/v1/blogs/search/?title={}&desc={}
    title = request.query_params.get('title')
    desc = request.query_params.get('desc')

    if title and desc:
        blogs = Blog.objects.filter(Q(title__icontains=title), Q(description__icontains=desc))
    elif title:
        blogs = Blog.objects.filter(title__icontains=title)
    elif desc:
        blogs = Blog.objects.filter(description__icontains=desc)
    else:
        blogs = Blog.objects.all()

    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)
