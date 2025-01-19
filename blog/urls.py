from django.urls import path
from blog import views

urlpatterns = [
    # cbw
    path('cbw/blogs/', views.BlogListCreateAPIView.as_view(), name='cbw-blogs-list-create'),
    path('cbw/myblogs/', views.MyBlogListAPIView.as_view(), name='my-blogs'),
    path('cbw/blogs/<int:pk>/', views.BlogRetriveUpdateDeleteAPIView.as_view(), name='cbw-blogs-retrive-update-delete'),
    path('cbw/register/', views.UserRegisterView.as_view(), name='user-register')

]
