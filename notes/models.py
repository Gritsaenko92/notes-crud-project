from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    text = models.TextField(verbose_name="Текст нотатки")
    reminder_at = models.DateTimeField(null=True, blank=True, verbose_name="Час нагадування")
    category = models.CharField(max_length=100, blank=True, verbose_name="Категорія")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title