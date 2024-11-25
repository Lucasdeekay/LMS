from django.contrib import admin
from .models import CustomUser, Profile, Course, CourseMaterial, CoursePayment, CourseProgress, Comment


# Custom User Admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_student', 'is_lecturer', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_student', 'is_lecturer')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'bio')
    search_fields = ('user__username', 'phone_number', 'address')

admin.site.register(Profile, ProfileAdmin)

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lecturer', 'price', 'created_at')
    search_fields = ('title', 'lecturer__username')
    list_filter = ('lecturer',)
    ordering = ('created_at',)

admin.site.register(Course, CourseAdmin)

# Course Material Admin
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('course', 'material_type', 'uploaded_at')
    search_fields = ('course__title', 'material_type')
    list_filter = ('material_type',)

admin.site.register(CourseMaterial, CourseMaterialAdmin)

# Course Payment Admin
class CoursePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount_paid', 'payment_date', 'payment_status')
    search_fields = ('student__username', 'course__title', 'payment_status')
    list_filter = ('payment_status', 'payment_date')

admin.site.register(CoursePayment, CoursePaymentAdmin)

# Course Progress Admin
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress')
    search_fields = ('student__username', 'course__title')
    list_filter = ('course',)

admin.site.register(CourseProgress, CourseProgressAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'created_at')
    list_filter = ('created_at',)

admin.site.register(Comment, CommentAdmin)
