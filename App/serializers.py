from rest_framework import serializers
from .models import CustomUser, Profile, Course, CourseMaterial, CoursePayment, CourseProgress

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
class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ('id', 'course', 'material_type', 'content', 'text_content', 'uploaded_at')

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
