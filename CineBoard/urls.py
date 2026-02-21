
from django.urls import path
from . import views

app_name = 'cineboard' 
urlpatterns = [
    path('movies', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create/', views.CreateCineBoardView.as_view(), name='movie_create'),
    path('movie/<int:id>/update/', views.UpdateCineBoardView.as_view(), name='movie_update'),
    path('movie/<int:id>/delete/', views.DeleteCineBoardView.as_view(), name='movie_delete'),
    
    path('search/', views.SearchView.as_view(), name='movie_search'),
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.AuthLoginView.as_view()),
    
    path('logout/', views.AuthLogoutView.as_view(), name='logout'),
]