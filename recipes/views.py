from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, \
    HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, \
    CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Recipe, Category, TagPost, UploadFiles
from .utils import DataMixin


class RecipeHome(DataMixin, ListView):
    template_name = 'recipe/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Recipe.published.all().select_related('cat')


def about(request):
    contact_list = Recipe.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recipe/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'recipe/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(
            Recipe.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'recipe/addpage.html'
    title_page = 'Добавление рецепта'

    def form_valid(self, form):
        r = form.save(commit=False)
        r.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Recipe
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'recipe/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование рецепта'


def login(request):
    return HttpResponse("Авторизация")


class RecipeCategory(DataMixin, ListView):
    template_name = 'recipe/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Recipe.published.filter(
            cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'recipe/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Recipe.published.filter(
            tags__slug=self.kwargs['tag_slug']).select_related('cat')

