from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView
from account_module.forms import SignupForm, LoginForm
from account_module.models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class SignupView(View):
    def get(self, request):
        context = {'signup_form': SignupForm}
        return render(request, 'account_module/signup.html', context)

    def post(self, request):
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']

            # Check if a user with the same username already exists
            if CustomUser.objects.filter(username=username).exists():
                signup_form.add_error('username', 'Username already exists')
                context = {'signup_form': signup_form}
                return render(request, 'account_module/signup.html', context)

            # Create a new user object
            new_user = CustomUser(username=username, email=email)

            # Set the password for the new user
            new_user.set_password(password)

            # Save the new user to the database
            new_user.save()

            # Redirect the user to a success page or login page
            return redirect('login')

        # If the form is not valid, re-render the signup page with the form and error messages
        context = {'signup_form': signup_form}
        return render(request, 'account_module/signup.html', context)


class LoginView(View):
    def get(self, request):

        context = {'login_form': LoginForm}
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_username = login_form.cleaned_data.get('username')
            user: CustomUser = CustomUser.objects.filter(username=user_username).first()
            if user:

                user_password = login_form.cleaned_data.get('password')
                is_password_correct = user.check_password(user_password)
                if is_password_correct:
                    login(request, user)
                    return redirect(reverse('index_page'))
                else:
                    login_form.add_error('username', 'wrong username or password')
            else:
                login_form.add_error('username', 'wrong username or password')

        context = {'login_form': LoginForm}
        return render(request, 'account_module/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account_module/profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        # return self.model.objects.get(username=self.request.user.username)
        return self.request.user


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'account_module/delete_account.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'account_module/edit_profile.html'
    fields = ['first_name', 'last_name', 'age', ]
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
