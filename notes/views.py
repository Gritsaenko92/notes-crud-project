from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Note
from .forms import NoteForm

# Головна сторінка: список, пошук за назвою, фільтрація за категорією або часом нагадування
class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        
        # Отримуємо параметри з GET-запиту (з форми фільтрації)
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        reminder_filter = self.request.GET.get('has_reminder', '')

        # Extra: Пошук за title
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        # Extra: Фільтрація за категорією
        if category_filter:
            queryset = queryset.filter(category__iexact=category_filter)
            
        # Extra: Фільтрація за наявністю часу нагадування
        if reminder_filter == 'yes':
            queryset = queryset.filter(reminder_at__isnull=False)
        elif reminder_filter == 'no':
            queryset = queryset.filter(reminder_at__isnull=True)

        return queryset

# Створення нової нотатки
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

# Вікно деталей та редагування (в одному вікні, як у завданні)
class NoteDetailUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_detail_update.html'
    
    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})

# Видалення нотатки
class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')