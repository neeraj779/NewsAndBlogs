from rest_framework import serializers
from .models import *

# Create your serializers here.
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        
        