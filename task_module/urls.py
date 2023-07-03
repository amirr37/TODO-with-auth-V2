from django.urls import path
from task_module import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/update/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
]
