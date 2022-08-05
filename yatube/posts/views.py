from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Group, User

from django.core.paginator import Paginator

from .forms import PostForm


num_posts = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10) 

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context) 


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.all()
    count_posts_author = posts_list.count()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'count_posts_author': count_posts_author,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_list = Post.objects.filter(author=post.author)
    count_posts_author = posts_list.count()
    context = {
        'post': post,
        'count_posts_author': count_posts_author,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'GET':
        title = 'Новый пост'
        is_edit = False
        form = PostForm()
        context = {
            'title': title,
            'is_edit': is_edit,
            'form': form
        }
        return render(request, 'posts/create_post.html', context)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:user', post.author)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        if request.user != post.author:
            return redirect('posts:post_detail', post_id=post.id)
        form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post.id)
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'post': post, 'is_edit': True}
    )