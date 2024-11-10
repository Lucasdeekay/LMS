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
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_lecturer': True})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Course Material model
class CourseMaterial(models.Model):
    MATERIAL_TYPES = [
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('text', 'Text'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    content = models.FileField(upload_to='course_materials/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.material_type}"

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
