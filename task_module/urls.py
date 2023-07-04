from django.urls import path
from task_module import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_page'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/update/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/delete/<int:pk>', views.TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('category/create', views.CategoryCreateView.as_view(), name='category-create'),
    path('tasks/today', views.TaskListTodayView.as_view(), name='today-task'),
    path('tasks/important', views.TaskListAPriorityView.as_view(), name='important-task'),
    path('category/<str:category>', views.TaskCategoriesView.as_view(), name='category')

]
