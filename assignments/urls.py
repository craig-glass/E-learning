from django.urls import path
from . import views


urlpatterns = [
    path('assignment/<int:module_id>', views.AssignmentsContentView.as_view(),
         name='assignments_content_list'),
]