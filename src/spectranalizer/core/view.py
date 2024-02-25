import functools
from django.db import transaction
from django.shortcuts import redirect
from django.contrib import messages
import os

def base_view(func):
    @functools.wraps(func)
    def inner(request, *args, **kwards):
        try:
            with transaction.atomic():
                return func(request, *args, **kwards)
        except Exception as e:
            if 'file_spectrs' in request.FILES:
                uploaded_file = request.FILES['file_spectrs']
                file_path = os.path.join('uploads', uploaded_file.name)
                if os.path.exists(file_path):
                    os.remove(file_path)
            messages.error(request, str(e))
            return redirect('graph') 
    return inner

    
