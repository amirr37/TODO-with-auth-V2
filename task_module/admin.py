from django.contrib import admin

# Register your models here.
from task_module.models import Task, Category


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
