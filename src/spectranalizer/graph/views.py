from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound, JsonResponse
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .models import *
from parser.parser import parser
from .form import *

# class GraphHome(ListView):
#     template_name = 'graph/main_graph.html'

def index(request):
    return render(request, 'graph/main_graph.html')



def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def graph_spectr(request):
    user_id = request.user.id
    if request.method == 'POST':
        file_name = request.FILES['file_upload'].name
        handle_uploaded_file(request.FILES['file_upload'])
        value_x, value_y, type = parser(f"uploads/{file_name}")
        values_data = Values.objects.create(type_spectr=type,values_x=value_x, values_y=value_y)
        spectr_data = Spectr.objects.create(file_name=file_name, values=values_data)
        UsersSpectrs.objects.create(spectr=spectr_data, user=user_id)
    
        
        # if request.is_ajax():
        #     info_id = request.POST.get('info_id')
        #     try:
        #         info_object = Values.objects.get(pk=info_id)
        #         info_object.is_used = True
        #         info_object.save()
        #         return JsonResponse({'status': 'success', 'message': 'Information marked as used'})
        #     except Values.DoesNotExist:
        #         return JsonResponse({'status': 'error', 'message': 'Information not found'})
    
    context = {
        # 'list' : spectr_list
    }
    return render(request, 'graph/spectr_graph.html', context)

def pageNotFound(request, exception):
    return HttpResponseNotFound("Страница не найдена")

def spectr_not_found(request):
    return redirect('home', parament=False)
    
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
    # form_class = AuthenticationForm
    template_name = 'graph/login.html'

    def get_success_url(self):
        return reverse_lazy('graph')


def logout_user(request):
    logout(request)
    return redirect('home')

    