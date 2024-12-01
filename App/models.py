from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User model
class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Profile model for additional user profile information
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Profile"


# Course model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for the course
    image = models.ImageField(upload_to='course-images/', verbose_name='Course Image')
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_lecturer': True},
                                 related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    pdf = models.FileField(upload_to='lessons/pdfs/', blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"


# Course Payment model
class CoursePayment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Completed')  # Can be extended for multiple statuses

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.amount_paid}"


# Student Course Progress model
class CourseProgress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # Progress percentage

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.progress}%"


# Comment model
class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
