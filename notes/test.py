from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Note

# ==========================================
# ЧАСТИНА 1: UNIT-ТЕСТИ (Робота з БД)
# ==========================================
class NoteModelAndCRUDTestCase(TestCase):
    
    def setUp(self):
        # Готуємо початкові дані для тестів
        self.note = Note.objects.create(
            title="Тестова нотатка",
            text="Опис тестової нотатки",
            category="Навчання"
        )

    def test_note_creation(self):
        """Unit-тест: Перевірка коректності створення та збереження нотатки в БД"""
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, "Тестова нотатка")
        self.assertEqual(note.text, "Опис тестової нотатки")
        self.assertEqual(note.category, "Навчання")
        self.assertNil = note.reminder_at  # за замовчуванням нагадування немає (None)

    def test_note_update(self):
        """Unit-тест: Перевірка зміни (оновлення) деталей нотатки"""
        note = Note.objects.get(id=self.note.id)
        
        # Змінюємо поля
        note.title = "Оновлена назва"
        note.text = "Новий текст"
        note.category = "Робота"
        note.save()

        # Отримуємо з бази знову і перевіряємо зміни
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, "Оновлена назва")
        self.assertEqual(updated_note.text, "Новий текст")
        self.assertEqual(updated_note.category, "Робота")

    def test_note_deletion(self):
        """Unit-тест: Перевірка видалення нотатки з БД"""
        note_id = self.note.id
        self.note.delete()
        
        # Перевіряємо, чи нотатка дійсно зникла з бази
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)


# ==========================================
# ЧАСТИНА 2: ІНТЕГРАЦІЙНІ ТЕСТИ (Тестовий клієнт / "API" Views)
# ==========================================
class NoteIntegrationTestCase(TestCase):

    def setUp(self):
        # Ініціалізуємо тестовий клієнт Django
        self.client = Client()
        # Створюємо базову нотатку для тестів відображення/редагування
        self.note = Note.objects.create(
            title="Інтеграційна нотатка",
            text="Текст для перевірки клієнтом",
            category="Тести"
        )

    def test_note_list_view(self):
        """Інтеграційний тест: Перевірка доступності головної сторінки та пошуку"""
        # Робимо GET-запит до головної сторінки
        response = self.client.get(reverse('note_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Інтеграційна нотатка")

        # Перевіряємо extra-функціонал: пошук через GET-параметр
        response_search = self.client.get(reverse('note_list'), {'search': 'Інтеграційна'})
        self.assertContains(response_search, "Інтеграційна нотатка")
        
        # Перевіряємо, що за пустим пошуком нічого не знайдено
        response_empty = self.client.get(reverse('note_list'), {'search': 'НеіснуючаНотатка'})
        self.assertNotContains(response_empty, "Інтеграційна нотатка")

    def test_note_create_via_client(self):
        """Інтеграційний тест: Створення нотатки через відправку форми (POST-запит)"""
        data = {
            'title': 'Нова нотатка від клієнта',
            'text': 'Створено через інтеграційний тест',
            'category': 'Покупки',
            'reminder_at': ''  # залишаємо порожнім
        }
        # Відправляємо POST-запит на створення
        response = self.client.post(reverse('note_create'), data=data)
        
        # Після успішного створення має бути редірект (код 302) на головну сторінку
        self.assertEqual(response.status_code, 302)
        # Перевіряємо, чи з'явилася нотатка в базі даних
        self.assertTrue(Note.objects.filter(title='Нова нотатка від клієнта').exists())

    def test_note_update_via_client(self):
        """Інтеграційний тест: Редагування деталей нотатки через POST-запит"""
        data = {
            'title': 'Повністю змінена назва',
            'text': 'Змінений текст через Клієнт',
            'category': 'Важливо',
            'reminder_at': ''
        }
        # Відправляємо POST-запит на URL деталей/редагування нотатки
        response = self.client.post(reverse('note_detail', kwargs={'pk': self.note.pk}), data=data)
        
        # Після редагування у нас налаштований редірект на цю ж сторінку деталей (код 302)
        self.assertEqual(response.status_code, 302)
        
        # Перевіряємо, чи оновилися дані в БД
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Повністю змінена назва')
        self.assertEqual(self.note.category, 'Важливо')

    def test_note_delete_via_client(self):
        """Інтеграційний тест: Видалення нотатки через POST-запит підтвердження"""
        # Відправляємо POST-запит на URL видалення
        response = self.client.post(reverse('note_delete', kwargs={'pk': self.note.pk}))
        
        # Має бути редірект на головну (302)
        self.assertEqual(response.status_code, 302)
        # Перевіряємо, що в БД нотатки з таким ID більше немає
        self.assertFalse(Note.objects.filter(id=self.note.pk).exists())