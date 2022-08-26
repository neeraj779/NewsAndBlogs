from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('v2/blogs', views.BlogViewSet, basename="BlogViewSet")

urlpatterns = [
    path('', views.Home.as_view(), name="Home"),
    path('register/', views.Register.as_view(), name="Register"),
    path('contact/', views.Contact.as_view(), name="Contact"),
    path('blogs/', views.Blogs.as_view(), name="Blogs"),
    path('blogs/<int:id>/', views.BlogDetails.as_view(), name="BlogDetails"),
    path('addblog/', views.AddBlog.as_view(), name="AddBlog"),
    path('updateblog/<int:id>/', views.UpdateBlog.as_view(), name="UpdateBlog"),
    path('deleteblog/<int:id>/', views.DeleteBlog.as_view(), name="DeleteBlog"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include(router.urls))
]
