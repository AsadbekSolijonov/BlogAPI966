from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from blog.models import Blog
from blog.serializers import BlogListSerializer, BlogDetailSerializer, BlogSearchSerializer, BlogCreateSerizlier, \
    BlogUpdateSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])  # LIST
def list_blogs(request):
    # /api/v1/blogs/
    blogs = Blog.objects.all()
    serializer = BlogListSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(['GET'])  # RETRIEVE
def detail_blog(request, pk):
    # /api/v1/blog/<int:pk>/detail
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        data = {"detail": f"Blog {pk} is not found!"}
        return Response(data)

    serializer = BlogDetailSerializer(blog)
    return Response(serializer.data)


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

    serializer = BlogSearchSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def blogs_create(request):
    try:
        serializer = BlogCreateSerizlier(data=request.data)
        if serializer.is_valid():
            blog = serializer.save()
            response_serializer = BlogCreateSerizlier(blog)
            return Response({"success": "Created OK", "detail": response_serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({"errors": str(e)}, status=500)


@api_view(['PUT'])
def blogs_update(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    serializer = BlogUpdateSerializer(blog, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Hammasi muvoffaqiyatli yaratildi."}, status=status.HTTP_200_OK)
    return Response({"error": "Ma'lumot xato."}, status=status.HTTP_400_BAD_REQUEST)

