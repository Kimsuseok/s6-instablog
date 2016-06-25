from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse

from .models import Post
from .forms import PostForm

from django.contrib.auth.decorators import login_required

# 페이징을 Paginator를 이용한 경우.
def list_posts(request):
    per_page = 5
    page = request.GET.get('page', 1)
    category_id = request.GET.get('category', 0)

    try:
        category_id = int(category_id)
        if category_id < 0:
            category_id = 0
    except ValueError:
        category_id = 0

    if category_id == 0:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(category=category_id)

    pg = Paginator(posts, per_page)
    try:
        # Paginator가 page값에 대한 예외처리를 알아서 하지는 않는다. 예외처리는 별도로 한다.
        contents = pg.page(page)
    except PageNotAnInteger:
        contents = pg.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        # template에 전달되는 객체는 page 객체이다. page 객체를 이용해 UI 필요한 여러 편리한 기능을 사용할 수 있다.
        'posts' : contents,
        'categories' : Category.objects.all(),
        'selected_category' : category_id,
    }

    return render(request, 'list.html', ctx)

def detail_post(request, pk):
    post = Post.objects.get(pk=pk)

    ctx = {
        'post' : post,
        'comments' : Comment.objects.filter(post=post)
    }

    return render(request, 'detail.html', ctx)

@login_required
def create_post(request):
    form = PostForm()
    categories = Category.objects.all()

    if request.method == 'POST':
        # Form으로 Validataion 체크하는 방법
        form = PostForm(data=request.POST)
        if form.is_valid() is True:
            new_post = form.save(commit=False)  # commit 인자를 False로 주면 save 호출시 DB에 반영하지는 않고 인스턴스 객체만 리턴한다.
            new_post.user = request.user        # 로그인한 정보를 기입
            new_post.save()                     # DB에 반영

            url = reverse('blog:detail', kwargs={'pk':new_post.pk})
            return redirect(url)

    ctx = {
        'form' : form,
        'categories' : categories,
    }

    return render(request, 'edit.html', ctx)

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # GET 일때는 수정을 위한 화면을 보여주고 POST일때는 글 수정을 한다.
    if request.method == 'GET':
        categories = Category.objects.all()

    else:
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.category = get_object_or_404(Category, pk=request.POST.get('category'))
        post.save()
        return redirect(reverse('blog:detail', kwargs={'pk' : post.pk}))

    ctx = {
        'categories' : categories,
        'post' : post,
    }

    return render(request, 'edit.html', ctx)

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:list')

    return render(request, 'delete.html', {'post' : post})

def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = request.POST.get('comment')

    if request.method == 'POST':
        new_comment = Comment()
        new_comment.post = post
        new_comment.content = comment
        new_comment.save()

    return redirect(reverse('blog:detail', kwargs={'pk' : post.pk}))

def delete_comment(request, pk):

    if request.method == 'POST':
        comment_pk = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()

    return redirect(reverse('blog:detail', kwargs={'pk': pk}))
"""
# 페이징을 직접 구현한 경우.
def list_posts(request):
    per_page = 2    # 한 페이지에 보여줄 게시물 갯수

    # 아래와 같이 하면 Query string에 반드시 page가 있어야 한다.
    # request.GET은 dict와 비슷한 key-value 방식의 QueryDict 객체인데 key가 없을 경우 에러가 발생한다.
    # page = request.GET['page']

    # 아래와 같이 하면 dict의 get()을 사용하기 때문에 Query String에 page가 없어도 상관없다.
    page = request.GET.get('page', 1)

    # Query String 으로 받는 page는 type이 string 이니 타입을 변경하여야 한다. 또한, 사용자에 의해 정수가 아닌 값이 들어올 수 있으니 체크를 해야 한다.
    try:
        page = int(page)
    except ValueError:
        page = 1
        # 만약 잘못된 query string에 대해 다른곳으로 이동하고 싶다면 redirect() 시킨다.
        # return redirect('blog:list')

    # page가 1보다 작은 값일 경우에 대한 처리.
    page = page if page >= 1 else 1

    posts = Post.objects.all()[(page-1)*per_page:page*per_page]

    # 참고로 posts 데이터가 없을때에 대한 예외처리는 view에서 할 수도 있고 template 에서 할 수도 있다.
    # view에서 할때는 redirect시키면 될 것이고, Template에서 할때는 템플릿 태그 {% empty %} 에서 처리하면 된다.

    # Template Context 로 Template에 전달할 인자를 dict로 전달한다.
    ctx = {
        'object_list' : posts,
    }

    # render 함수의 3번째 parameter는 Template Context를 dic으로 받는다.
    return render(request, 'list.html', ctx)
"""

"""
def create_post(request):
    form = PostNormalForm()
    categories = Category.objects.all()

    if request.method == 'POST':
        # Form으로 Validataion 체크하는 방법
        form = PostNormalForm(request.POST)
        if form.is_valid() is True:
            new_post = Post()
            new_post.title = form.cleaned_data['title']
            new_post.content = form.cleaned_data['content']
            new_post.category = get_object_or_404(Category, pk=request.POST.get('category'))
            new_post.save()
            url = reverse('blog:detail', kwargs={'pk':new_post.pk})
            return redirect(url)


        # Form을 사용하지 않는 경우
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = get_object_or_404(Category, pk=request.POST.get('category'))

        new_post = Post()
        new_post.title = title
        new_post.content = content
        new_post.category = category
        new_post.save()

        url = reverse('blog:detail', kwargs={'pk':new_post.pk})
        return redirect(url)

    else:
        post = get_object_or_404(Post, pk=2)
        form = PostNormalForm(initial=post.__dict__)

    ctx = {
        'form' : form,
        'categories' : categories,
    }

    return render(request, 'edit.html', ctx)
"""