from rest_framework import viewsets

from .models import CustomUser, Profile, Course, CoursePayment, CourseProgress, Comment, Lesson
from .serializers import (
    CustomUserSerializer,
    ProfileSerializer,
    CourseSerializer,
    CoursePaymentSerializer,
    CourseProgressSerializer, CommentSerializer, LessonSerializer,
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
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().select_related('course')
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Optionally filter lessons by course ID via query parameter (?course_id=).
        """
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return self.queryset.filter(course_id=course_id)
        return self.queryset


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
