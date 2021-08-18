import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Book1', price=25,
                                          author_name='Author1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Book2', price=55,
                                          author_name='Author1')
        self.book_3 = Book.objects.create(name='Book3', price=55,
                                          author_name='Author2')

    def test_get(self):
        url = reverse('book-list')
        print(url)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data, response.data)
        print(response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        print(url)
        response = self.client.get(url, data={'price': 55})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BookSerializer([self.book_2, self.book_3], many=True).data, response.data)
        print(response.data)

    def test_get_search(self):
        url = reverse('book-list')
        print(url)
        response = self.client.get(url, data={'search': 'Author1'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BookSerializer([self.book_1, self.book_2], many=True).data, response.data)
        print(response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Python3",
            "price": 150,
            "author_name": "Mark Summerfield"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book_1 = Book.objects.create(name='Book1', price=25,
                                          author_name='Author1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Book2', price=55,
                                          author_name='Author1')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #self.book_1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "rate": 3
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #self.book_1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(relation.rate, 3)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "rate": 6
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        #self.book_1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(relation.rate, 3)