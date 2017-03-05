from django.shortcuts import render
import numpy as np

from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
import json
from .netcdf_loader import get_computed_dataset

dataset = get_computed_dataset()


def index(request):
    return render(request, 'asthmap/index.html', {})


def get_index(value, variable):
    return np.argmin(abs(variable - value))


@requires_csrf_token
def query_computed_dataset(request):

    if request.method == 'POST':

        danger_index = dataset['computed_values'][0,
            get_index(dataset['latitudes'], float(request.POST.get('latitude'))),
            get_index(dataset['longitudes'], float(request.POST.get('longitude')))
        ]

        return HttpResponse(
            json.dumps({
                'risk': int(danger_index)
            }),
            content_type="application/json"
        )
