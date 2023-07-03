from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
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
