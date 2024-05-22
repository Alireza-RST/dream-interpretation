from django.urls import path

from .views import InterpretationView


urlpatterns = [
    path('interpret/', InterpretationView.as_view(), name='interpret')
]
