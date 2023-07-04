from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, )
    priority = models.IntegerField(default=1, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', )
    due_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    # todo : field category and category model
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-due_date', 'priority']
