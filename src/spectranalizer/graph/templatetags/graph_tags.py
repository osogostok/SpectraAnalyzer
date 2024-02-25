from django import template
from graph.models import *
import numpy as np

register = template.Library()


@register.inclusion_tag('graph/part_spectr.html')
def show_spectrs(request):
    user_spectrs = UsersSpectrs.objects.filter(
        user=request.user, is_publish=True)
    data = []
    for user_spectr in user_spectrs:
        values_y = np.fromstring(
            user_spectr.spectr.values.values_x, dtype=float,  sep=' ')
        values_x = np.fromstring(
            user_spectr.spectr.values.values_y, dtype=float,  sep=' ')
        coordinates = np.column_stack((values_y, values_x))
        coordinates_list = coordinates.tolist()
        temp = {
            'name': user_spectr.spectr.file_name,
            'data': coordinates_list
        }
        data.append(temp)
    return {"spectrs": data}


@register.simple_tag
def get_list_unused(user_id):
    return UsersSpectrs.objects.filter(user_id=user_id)
