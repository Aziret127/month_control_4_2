
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from CineBoard.forms import CustomUserForm
from django.shortcuts import get_object_or_404
from . import models, forms
from django.db.models import F
from .forms import CustomUserForm

# Create your views here.

class RegisterView(generic.CreateView):
    template_name = 'register.html'
    form_class = CustomUserForm
    def get_success_url(self):
        return reverse('login')
    
class AuthLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    def get_success_url(self):
        return reverse('home')
    
class AuthLogoutView(LogoutView):
    next_page = reverse_lazy('login')



class SearchView(generic.ListView):  
    template_name = 'movie_search.html' 
    context_object_name = 'movies'  
    model = models.Movie
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('s')
        if query:
            return self.model.objects.filter(title__icontains=query)
        return self.model.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = self.request.GET.get('s', '')
        return context

# UPDATE
class UpdateCineBoardView(generic.UpdateView):
    template_name = 'update_cineboard.html'
    form_class = forms.MovieForm  
    model = models.Movie
    
    def get_success_url(self):
        return reverse('movie_detail', kwargs={'id': self.object.id})
    
    def get_object(self, **kwargs):
        movie_id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=movie_id)
    
    def form_valid(self, form):
        print("Измененные поля:", form.changed_data)
        return super().form_valid(form)

# DELETE
class DeleteCineBoardView(generic.DeleteView):
    template_name = 'confirm_delete.html'
    model = models.Movie
    
    def get_success_url(self):
        return reverse('movie_list')
    
    def get_object(self, **kwargs):
        movie_id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=movie_id)

# CREATE
class CreateCineBoardView(generic.CreateView):
    template_name = 'create_cineboard.html'
    form_class = forms.MovieForm
    
    def get_success_url(self):
        return reverse('cineboard:movie_detail', kwargs={'id': self.object.id})
    def form_valid(self, form):
        print("Создан новый объект")
        return super().form_valid(form)

# DETAIL (ОБЪЕДИНЕННЫЙ КЛАСС)
class MovieDetailView(generic.DetailView):
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'id'
    model = models.Movie

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Подсчет просмотров
        request = self.request
        viewed_lang = request.session.get('viewed_lang', [])
        
        if obj.pk not in viewed_lang:
            models.Movie.objects.filter(pk=obj.pk).update(
                views=F("views") + 1
            )
            viewed_lang.append(obj.pk)
            request.session['viewed_lang'] = viewed_lang
            obj.refresh_from_db()
        
        return obj

# LIST
class MovieListView(generic.ListView):  # Переименовал для консистентности
    template_name = 'movie_list.html'  # Убедитесь, что имя шаблона правильное
    model = models.Movie
    context_object_name = 'movies'
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')