from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Comment
from datetime import datetime as dt
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from blog.forms import PostForm, CommentForm, ProfileForm
from django.http import Http404, HttpResponse

current_time = dt.now()
pag_pages: int = 10


class ProfileLoginView(LoginView):
    def get_success_url(self) -> HttpResponse:
        '''Получаем адрес.'''
        return reverse('blog:profile',
                       args=(self.request.user.get_username(),))


def edit_profile(request, name) -> HttpResponse:
    '''Редактирование профиля.'''
    templates = 'blog/user.html'
    instance = get_object_or_404(User, username=name)
    if instance.username != request.user.username:
        return redirect('login')
    form = ProfileForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, templates, context)


def info_profile(request, name) -> HttpResponse:
    '''Информация профиля.'''
    templates = 'blog/profile.html'
    user = get_object_or_404(User, username=name)
    profile_post = user.posts.all()
    paginator = Paginator(profile_post, pag_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user,
        'page_obj': page_obj,
    }
    return render(request, templates, context)


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    ).select_related('author')
    ordering = '-pub_date'
    paginate_by = 10


def category_posts(request, category_slug) -> HttpResponse:
    '''Отображение категории постов.'''
    templates = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    post_list = category.posts.filter(
        pub_date__lte=current_time,
        is_published=True,
    )
    paginator = Paginator(post_list, pag_pages)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, templates, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form) -> HttpResponse:
        '''Валидность формы.'''
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponse:
        '''Получаем адрес.'''
        if self.request.user.is_authenticated:
            return reverse('blog:profile',
                           args=(self.request.user.get_username(),))
        else:
            return reverse('login')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        '''Отправка условий.'''
        self.post_id = kwargs['pk']
        instance = get_object_or_404(Post, pk=self.post_id)
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=self.post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> HttpResponse:
        '''Получаем адрес.'''
        return reverse('blog:post_detail', args=[str(self.post_id)])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        '''Отправка условий.'''
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        '''Отправка условий.'''
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if not instance.is_published and instance.author != request.user:
            raise Http404("")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> HttpResponse:
        '''получем контекстные данные.'''
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context


@login_required
def add_comment(request, pk) -> HttpResponse:
    '''Добавление комментария.'''
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, comment_id, post_id) -> HttpResponse:
    '''Редактирование комментария.'''
    instance = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if instance.author != request.user:
        return redirect('login')
    form = CommentForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'comment': instance
    }
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, comment_id, post_id) -> HttpResponse:
    '''Удаление комментария.'''
    instance = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if instance.author != request.user:
        return redirect('login')
    context = {
        'comment': instance
    }
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)
