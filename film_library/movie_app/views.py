import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string

from . import models
from . import forms


@csrf_exempt
def vote_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            movie_id = data.get('movie_id')
            vote_value = int(data.get('vote'))

            if vote_value not in [-1, 1]:
                return JsonResponse({'error': 'Invalid vote'}, status=400)

            movie = models.Movie.objects.get(pk=movie_id)

            vote, created = models.MovieVote.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'vote': vote_value}
            )

            likes = movie.votes.filter(vote=1).count()
            dislikes = movie.votes.filter(vote=-1).count()

            return JsonResponse({'likes': likes, 'dislikes': dislikes})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Unauthorized'}, status=403)


@require_POST
@csrf_exempt
def delete_comment_view(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    comment = get_object_or_404(models.CommentMovie, pk=pk)

    if comment.author != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    comment.delete()
    return JsonResponse({'success': True})


class Cats(ListView):
    model = models.Category
    template_name = 'movie_app/cat_list.html'
    context_object_name = 'categories'


class MovieCat(ListView):
    model = models.Movie
    template_name = 'movie_app/movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return models.Movie.objects.filter(category__slug=self.kwargs['cat_slug'])


class ShowMovie(FormMixin, DetailView):
    form_class = forms.CommentsForm
    model = models.Movie
    template_name = 'movie_app/movie_detail.html'
    slug_url_kwarg = 'movie_slug'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        context['comments'] = models.CommentMovie.objects.filter(post=movie)
        context['form'] = self.get_form()
        context['like_count'] = movie.votes.filter(vote=1).count()
        context['dislike_count'] = movie.votes.filter(vote=-1).count()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=403)

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = self.request.user
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('movie_app/additionally/comment.html', {
                    'comm': comment,
                    'user': request.user
                })
                return JsonResponse({'comment_html': html})

            return redirect(self.get_success_url())
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form'}, status=400)
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie', kwargs={
            'movie_slug': self.kwargs['movie_slug'],
            'cat_slug': self.kwargs['cat_slug'],
        })


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'movie_app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('cat_list')


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'movie_app/login.html'

    def get_success_url(self):
        return reverse_lazy('cat_list')


class UserAccount(DetailView):
    model = User
    template_name = 'movie_app/personal_account.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_pk'


def logout_user(request):
    logout(request)
    return redirect('login')