from django.urls import path
from . import views


urlpatterns = [
    path('assignment/<int:module_id>', views.AssignmentsListView.as_view(),
         name='assignments_list'),
    path('assignment/<int:module_id>/content/<model_name>/create/',
         views.AssignmentCreateUpdateView.as_view(),
         name='assignment_content_create'),
]