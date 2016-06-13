from django.contrib import admin

from .models import Post
from .models import Comment
from .models import Tag
from .models import Category

class CommentInlineAdmin(admin.StackedInline):
    # 같이 추가할 모델
    model = Comment
    # 같이 추가할 갯수
    extra = 2

class PostAdmin(admin.ModelAdmin):
    # admin 에서 보여줄 컬럼
    list_display = ['id', 'title', 'created_at']
    # admin 에서 링크를 걸어줄 컬럼
    list_display_links = ['id', 'title', 'created_at']
    # admin 에서 보여줄 정렬방식
    ordering = ['id', 'created_at'] # 역순은 '-id'
    # 글을 쓸때 댓글까지 같이 쓸수 있는 기능
    inlines = [CommentInlineAdmin, ]
    # 검색
    search_fields = ['title', 'content']
    # 날짜별로 그룹핑해주는 기능이다. 그냥 사용하면 pytz가 설치되어 있지 않다고 하면서 에러가 난다. 에러가 나는 이유는 '시간' 에 대한 그룹핑 기능 때문이다.
    # 시간에 대한 연산을 위해 pytz가 설치되어 있어야 한다. (pip install pytz)
    date_hierarchy = 'created_at'
    # 필터
    list_filter = ['status', 'category']
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)

