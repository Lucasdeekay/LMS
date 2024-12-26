from django.urls import path, include

from .views import HomeView, ContactView, AboutView,  BlogView, CommunityView, CourseListView, FaqsView, InstructorsView, \
    PricingView, TestimonialsView, ServicesView, CourseDetailsView, PaymentDetailsView


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
    path('course-list/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:course_id>/details/', CourseDetailsView.as_view(), name='course_details'),
    path('courses/<int:course_id>/payment/', PaymentDetailsView.as_view(), name='payment'),
]