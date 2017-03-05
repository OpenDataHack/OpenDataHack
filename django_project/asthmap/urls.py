from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^query_computed_dataset', views.query_computed_dataset)
]
