from django.urls import path
from .views import CustomLoginView, LogoutInterfaceView
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),  # Redirect root URL to /home/
    path('home/', views.home, name='home'),  # Remove the leading slash
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutInterfaceView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('add_run/', views.add_run, name='add_run'),
    path('edit_run/<int:run_id>/', views.edit_run, name='edit_run'),
    path('delete_run/<int:run_id>/', views.delete_run, name='delete_run'),
    path('add_swim/', views.add_swim, name='add_swim'),
    path('edit_swim/<int:swim_id>/', views.edit_swim, name='edit_swim'),
    path('delete_swim/<int:swim_id>/', views.delete_swim, name='delete_swim'),
    path('add_bike/', views.add_bike, name='add_bike'),
    path('edit_bike/<int:bike_id>/', views.edit_bike, name='edit_bike'),
    path('delete_bike/<int:bike_id>/', views.delete_bike, name='delete_bike'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('progress/add/', views.add_progress, name='add_progress'),
    path('progress/view/', views.view_progress_reports, name='view_progress')
    # Additional paths if needed
]

