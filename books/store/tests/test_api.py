from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Book1', price=25)
        self.book_2 = Book.objects.create(name='Book2', price=25)

    def test_get(self):
        url = reverse('book-list')
        print(url)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BookSerializer([self.book_1, self.book_2], many=True).data, response.data)
        print(response.data)

    def test_get2(self):
        url = reverse('book-list')
        print(url)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BookSerializer([self.book_1, self.book_2], many=True).data, response.data)
        print(response.data)