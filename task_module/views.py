from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, DeleteView, CreateView
from .models import Task, Category
from django.urls import reverse_lazy


# Create your views here.


class PartialHeaderView(TemplateView):
    template_name = 'components/header_component.html'

    def get_context_data(self, **kwargs):
        kwargs['user'] = self.request.user
        kwargs['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            # User is logged in
            kwargs['is_logged_in'] = True
        kwargs['is_logged_in'] = False

        return super(PartialHeaderView, self).get_context_data(**kwargs)


class PartialImportantTasksView(TemplateView):
    template_name = 'components/most_important.html'

    def get_context_data(self, **kwargs):
        kwargs['tasks'] = Task.objects.order_by('-priority', 'due_date')[:6]
        return super(PartialImportantTasksView, self).get_context_data(**kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'task_module/index_page.html'


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_module/task_detail_page.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'priority', 'completed', 'due_date']
    template_name = 'task_module/task_update_page.html'

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_module/task_confirm_delete.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'priority', 'completed', 'due_date', 'category', ]
    template_name = 'task_module/task_create_page.html'

    def get_success_url(self):
        # Customize the success URL dynamically based on the created task
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})

    # auto save user as a foreignKey
    # https://stackoverflow.com/questions/70091149/fill-the-foreignkey-field-in-django-createview-automatically
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user if user else None
        return super(TaskCreateView, self).form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title']
    template_name = 'task_module/category_create.html'
    success_url = reverse_lazy('index_page')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user if user else None
        return super(CategoryCreateView, self).form_valid(form)


class TaskListTodayView(ListView):
    model = Task
    template_name = 'task_module/task_list.html'
    context_object_name = 'tasks'
    ordering = ['priority']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        today = date.today()
        queryset = Task.objects.filter(due_date=today).filter(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['1_priority'] = Task.objects.filter(user=self.request.user).filter(priority__exact=1)
        today = date.today()
        today_tasks = self.get_queryset().filter(due_date=today)
        context['today_tasks'] = today_tasks
        all_tasks = Task.objects.all().filter(user=self.request.user)
        context['all_tasks'] = all_tasks
        return context


class TaskListAPriorityView(ListView):
    model = Task
    template_name = 'task_module/task_list.html'
    context_object_name = 'tasks'
    ordering = ['priority']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(priority__lt=4).filter(user=user)
        return queryset


class TaskCategoriesView(View):
    def get(self, request, category):
        context = {
            'tasks': Task.objects.filter(user=self.request.user).filter(category__title=category),
            'category': category
        }
        return render(request, 'task_module/task_list.html', context)
