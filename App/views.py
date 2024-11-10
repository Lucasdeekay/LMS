from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from App.models import CustomUser


# Home Page View
class HomeView(View):
    def get(self, request):
        return render(request, 'app/home.html')


# About Page View
class AboutView(View):
    def get(self, request):
        return render(request, 'app/about.html')


# Contact Page View
class ContactView(View):
    def get(self, request):
        return render(request, 'app/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Add a simple validation check
        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
            return render(request, 'app/contact.html')

        # Implement any additional processing for contact form (e.g., save to DB, send email)
        # For demonstration, we can display a success message
        messages.success(request, 'Thank you for contacting us. We will get back to you soon.')
        return render(request, 'app/contact.html')

# Custom Registration View
class RegistrationView(View):
    def get(self, request):
        return render(request, 'app/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'app/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'app/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'app/register.html')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. You can log in now.')
        return redirect('login')


# Custom Login View
class LoginView(View):
    def get(self, request):
        return render(request, 'app/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')  # Redirect to a dashboard or home page
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'app/login.html')


# Custom Logout View
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')


# Forgot Password View
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'app/forgot_password.html')

    def post(self, request):
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse_lazy('reset_password', kwargs={'uidb64': uid, 'token': token})
            reset_url = request.build_absolute_uri(link)

            # Send email with reset link
            subject = 'Password Reset Request'
            message = render_to_string('app/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, 'from@example.com', [email])  # Update sender email
            messages.success(request, 'Password reset link has been sent to your email.')
        else:
            messages.error(request, 'Email not registered.')
        return render(request, 'app/forgot_password.html')


# Password Reset View
class PasswordResetView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'app/reset_password.html', {'valid': True, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'Invalid link.')
            return render(request, 'app/reset_password.html', {'valid': False})

    def post(self, request, uidb64, token):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'app/reset_password.html', {'valid': True, 'uidb64': uidb64, 'token': token})

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset. You can log in now.')
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')


# Change Password View
class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'app/change_password.html')

    def post(self, request):
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'app/change_password.html')

        if request.user.check_password(old_password):
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Password changed successfully.')
            return redirect('dashboard')  # Redirect to a dashboard or home page
        else:
            messages.error(request, 'Old password is incorrect.')
            return render(request, 'app/change_password.html')
