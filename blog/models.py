from django.db import models
from django.conf import settings

class Post(models.Model):
    _status = (
        ('opn', 'Opened', ),
        ('clsd', 'Closed', ),
        ('prvt', 'Privated', ),
        ('scheduled', '예약', ),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    status = models.CharField(max_length=20, choices=_status,)
    image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category')

    def __str__(self):
        #return '{}: {}'.format(self.pk, self.title)
        return self.title

    def get_absolute_url(self):
        # get_absolute_url() 메서드를 지정해두면 나중에 redirect(Post) 를 호출했을때 여기 정의한 URL로 이동한다.
        # 메서드 이름 자체는 Django에서 사용하는 일종의 규칙이다.
        return '/blog/posts/{}/'.format(self.pk)

    class Meta:
        ordering = ['-created_at', '-pk']


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.content)


class Tag(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.name