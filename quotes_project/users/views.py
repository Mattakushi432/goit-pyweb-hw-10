from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import RegisterForm


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            # Автоматический вход после регистрации
            user = authenticate(username=username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect(to='quotes_app:root')
        return render(request, self.template_name, {'form': form})
