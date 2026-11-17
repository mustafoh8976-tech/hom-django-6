from django.test import TestCase
from django.urls import reverse
from .models import Janore, Kino, Komentari


class KinoViewsTests(TestCase):
    def setUp(self):
        self.drama = Janore.objects.create(name='Драма')
        self.comedy = Janore.objects.create(name='Комедия')
        self.film = Kino.objects.create(
            name='Тихая история',
            description='Описание фильма',
            year=2024,
            country='Россия',
        )
        self.film.janore.add(self.drama)

    def test_home_searches_by_name_and_genre(self):
        response = self.client.get(reverse('home'), {'name': 'тихая', 'janore': self.drama.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тихая история')

        response = self.client.get(reverse('home'), {'janore': self.comedy.pk})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Тихая история')

    def test_film_page_saves_comment(self):
        response = self.client.post(
            reverse('kino_detail', args=[self.film.pk]),
            {'name': 'Аня', 'text': 'Очень понравился фильм!'},
        )
        self.assertRedirects(response, reverse('kino_detail', args=[self.film.pk]))
        self.assertTrue(Komentari.objects.filter(kino=self.film, name='Аня').exists())

    def test_empty_comment_is_rejected(self):
        response = self.client.post(
            reverse('kino_detail', args=[self.film.pk]),
            {'name': 'Аня', 'text': '   '},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заполни имя и текст комментария.')
        self.assertEqual(Komentari.objects.count(), 0)
