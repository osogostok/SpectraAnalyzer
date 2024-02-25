from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import View
from core.view import base_view
from django.utils.decorators import method_decorator
import os


from .models import *
from parser.parser import parser
from .form import *


def index(request):
    return render(request, 'graph/main_graph.html')


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class GraphSpectrs(LoginRequiredMixin, View):
    template_name = 'graph/spectr_graph.html'

    def get(self, request, *args, **kwargs):
        queryset = UsersSpectrs.objects.filter(
            user=request.user, is_publish=True)
        return render(request, self.template_name, {'spectrs': queryset})

    @method_decorator(base_view)
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file_spectrs')
        if uploaded_file:
            file_name = uploaded_file.name
            if not Spectr.objects.filter(file_name=file_name).exists():
                handle_uploaded_file(uploaded_file)
                type, value_y, value_x = parser(f"uploads/{file_name}")
                values_data = Values.objects.create(
                    type_spectr=type, values_x=value_x, values_y=value_y)
                spectr_data = Spectr.objects.create(
                    file_name=file_name, values=values_data)
                UsersSpectrs.objects.create(
                    spectr=spectr_data, user=request.user)
                os.remove(f"uploads/{file_name}")
            else:
                spectr_data = get_object_or_404(Spectr, file_name=file_name)
                UsersSpectrs.objects.create(
                    spectr=spectr_data, user=request.user)

            return redirect(request.path)
        else:
            raise ValueError("Unknown Error")


class UpdateSpectrView(View):
    @method_decorator(base_view)
    def post(self, request, *args, **kwargs):
        info_id = request.POST.get('infoId')
        is_publish_str = request.POST.get('isPublish')
        is_publish = (is_publish_str == 'true')
        UsersSpectrs.objects.filter(
            user=request.user, spectr=info_id).update(is_publish=is_publish)
        return JsonResponse({'status': 'success'})


def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'graph/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('graph')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'graph/login.html'

    def get_success_url(self):
        return reverse_lazy('graph')


def logout_user(request):
    logout(request)
    return redirect('home')
