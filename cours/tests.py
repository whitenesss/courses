
from rest_framework import status

from rest_framework.test import APITestCase

from cours.models import Lesson
from users.models import User


# from users.models import User
# from django.contrib.auth import get_user_model


class LessonTestCase(APITestCase):
    pass

    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password1')
        # self.user2 = User.objects.create_user(email='user2@example.com', password='password2')
        # self.course = Well.objects.create(title='Test Course')
        # self.lesson1 = Lesson.objects.create(title='Lesson 1', description='This is a test lesson',
        #                                      link_to_video='https://www.youtube.com/')
        # self.lesson2 = Lesson.objects.create(title='Lesson 2', course=self.well, owner=self.user1)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user1)
        url = 'http://127.0.0.1:8000/well/lesson/create/'
        url1 = 'http://127.0.0.1:8000/well/lesson'
        url2 = 'http://127.0.0.1:8000/well/lesson/retrieve/1/'
        url3 = 'http://127.0.0.1:8000/well/lesson/update/1/'
        url4 = 'http://127.0.0.1:8000/well/lesson/destroy/1/'
        data = {
            'title': 'Test Lesson',
            'description': 'This is a test lesson',
            'link_to_video': 'https://www.youtube.com/',

        }

        resource = self.client.post(
            url,
            data=data, format='json'
        )
        print(resource.json())
        self.assertEqual(resource.status_code, status.HTTP_201_CREATED)

        resource = self.client.get(
            url1, format='json'
        )
        print(resource.json())
        self.assertEqual(resource.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resource.data), 4)

        resource = self.client.get(
            url2, format='json'
        )

        print(resource.json())
        self.assertEqual(resource.status_code, status.HTTP_200_OK)
        self.assertEqual(resource.data['title'], 'Test Lesson')

        data = {
            'title': 'Updated Lesson 1',
            'link_to_video': 'https://www.youtube.com/'
        }
        response = self.client.patch(url3, data, format='json')
        print(resource.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson 1')

        response = self.client.delete(url4)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_create_well(self):
        self.client.force_authenticate(user=self.user1)
        url = 'http://127.0.0.1:8000/well/'
        url2 = 'http://127.0.0.1:8000/well/subscription/create/'
        data = {
            'title': 'test curs',
            'content': 'test content',

        }
        resource = self.client.post(url, data=data, format='json')
        self.assertEqual(resource.status_code, status.HTTP_201_CREATED)

        data1 = {
            "well_id": 1
            }
        resource = self.client.post(url2, data=data1, format='json')
        self.assertEqual(resource.status_code, status.HTTP_200_OK)
        # self.assertEqual(resource.data1['is_subscribed'], True)
