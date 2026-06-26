from django.urls import path
from .views import NoteListView, NoteCreateView, NoteDetailUpdateView, NoteDeleteView

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('new/', NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/', NoteDetailUpdateView.as_view(), name='note_detail'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]