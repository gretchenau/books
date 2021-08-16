from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def testok(self):
        book_1 = Book.objects.create(name='Book1', price=25,
                                     author_name='Author1')
        book_2 = Book.objects.create(name='Book2', price=55,
                                     author_name='Author2')
        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Book1',
                'price': '25.00',
                'author_name': 'Author1'
            },
            {
                'id': book_2.id,
                'name': 'Book2',
                'price': '55.00',
                'author_name': 'Author2'
            }
        ]
        print(data)
        self.assertEqual(expected_data, data)