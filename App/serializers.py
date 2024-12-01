from rest_framework import serializers

from .models import CustomUser, Profile, Course, CoursePayment, CourseProgress, Comment, Lesson


# User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_student', 'is_lecturer')


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'profile_picture', 'phone_number', 'address')


# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'lecturer', 'created_at')


# Course Material Serializer
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'video', 'pdf', 'note', 'created_at']


# Course Payment Serializer
class CoursePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePayment
        fields = ('id', 'student', 'course', 'amount_paid', 'payment_date', 'payment_status')


# Course Progress Serializer
class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = ('id', 'student', 'course', 'progress')


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'website', 'message', 'created_at')
