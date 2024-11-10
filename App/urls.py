from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HomeView, ContactView, RegistrationView, LoginView, LogoutView, AboutView, ForgotPasswordView, \
    PasswordResetView, ChangePasswordView
from .viewsets import (
    CustomUserViewSet,
    ProfileViewSet,
    CourseViewSet,
    CourseMaterialViewSet,
    CoursePaymentViewSet,
    CourseProgressViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'course-materials', CourseMaterialViewSet)
router.register(r'course-payments', CoursePaymentViewSet)
router.register(r'course-progresses', CourseProgressViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/', include(router.urls)),
]
