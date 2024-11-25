from rest_framework import viewsets
from .models import CustomUser, Profile, Course, CourseMaterial, CoursePayment, CourseProgress, Comment
from .serializers import (
    CustomUserSerializer,
    ProfileSerializer,
    CourseSerializer,
    CourseMaterialSerializer,
    CoursePaymentSerializer,
    CourseProgressSerializer, CommentSerializer,
)

# User ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# Profile ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# Course ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Course Material ViewSet
class CourseMaterialViewSet(viewsets.ModelViewSet):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer

# Course Payment ViewSet
class CoursePaymentViewSet(viewsets.ModelViewSet):
    queryset = CoursePayment.objects.all()
    serializer_class = CoursePaymentSerializer

# Course Progress ViewSet
class CourseProgressViewSet(viewsets.ModelViewSet):
    queryset = CourseProgress.objects.all()
    serializer_class = CourseProgressSerializer

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
