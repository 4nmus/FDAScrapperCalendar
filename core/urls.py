from django.urls import path
from .views import ShowDataView

urlpatterns = [
    path('', ShowDataView.as_view() , name='main'),
]