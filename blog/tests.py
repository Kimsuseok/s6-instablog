from django.test import TestCase, Client
from .models import Post, Category
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class PostTest(TestCase):
    # 테스트 시작 전 호출되는 메서드
    def setUp(self):
        self.u1 = User.objects.create_user(username='hello', password='asdf')
        category = Category(name='ccc')
        category.save()
        self.category = category

    def test_create_post(self):
        u1 = User.objects.first()

        new_post = Post()
        new_post.user = u1
        new_post.title = 'hello'
        new_post.content = 'ahahahahah'
        new_post.category = self.category
        new_post.save()

        # 방법은 여러개..
        # 1.
        # self.assertIsNotNone(new_post.pk)
        # 2.
        self.assertTrue(Post.objects.filter(pk=new_post.pk).exists())

    def test_failed_create_post(self):
        new_post = Post()
        new_post.title = 'hello'
        new_post.content = 'ahahahahah'
        new_post.category = self.category

        with transaction.atomic():
            # new_post.save()를 호출했을때 반드시 IntegrityError 가 발생한다는 테스트
            with self.assertRaises(IntegrityError):
                new_post.save()

    # 가상의 Client를 이용한 테스트
    def test_client_detail_post(self):
        c = Client()

        p = Post()
        p.user = self.u1
        p.title = 'title'
        p.content = 'content'
        p.category = self.category
        p.save()

        # res는 Django View 함수가 리턴해주는 HttpResponse
        res = c.get(reverse('blog:detail', kwargs={'pk':p.pk}))

        self.assertEqual(res.status_code, 200)
