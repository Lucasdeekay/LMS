from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HomeView, ContactView, RegistrationView, LoginView, LogoutView, AboutView, ForgotPasswordView, \
    PasswordResetView, ChangePasswordView, BlogView, CommunityView, CourseListView, FaqsView, InstructorsView, \
    PricingView, TestimonialsView, ServicesView, CourseDetailsView
from .viewsets import (
    CustomUserViewSet,
    ProfileViewSet,
    CourseViewSet,
    CoursePaymentViewSet,
    CourseProgressViewSet, CommentViewSet, LessonViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'course-payments', CoursePaymentViewSet)
router.register(r'course-progresses', CourseProgressViewSet)
router.register(r'comments', CommentViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('community/', CommunityView.as_view(), name='community'),
    path('faqs/', FaqsView.as_view(), name='faqs'),
    path('instructors/', InstructorsView.as_view(), name='instructors'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('testimonials/', TestimonialsView.as_view(), name='testimonials'),
    path('services/', ServicesView.as_view(), name='services'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('course-list/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:course_id>/lessons/', CourseDetailsView.as_view(), name='course_lessons'),
    path('api/', include(router.urls)),
]
