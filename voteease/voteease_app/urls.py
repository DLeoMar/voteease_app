from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_registration, name='login_registration'),
    path('votingsystemUi2/', views.votingsystem_ui2_view, name='votingsystemUi2'), 
    path('logout', views.logout_user, name='logout'),
    path('positions', views.positions, name='positions'),
    path('candidates', views.render_candidates, name='candidates'),
    path('candidates/add_candidate', views.open_create_candidate, name='add_candidate'),
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('delete-position/<int:position_id>/', views.delete_position, name='delete_position'),
    path('delete-candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('add_position/', views.add_position, name='add_position'),
    path('cast-vote', views.cast_vote, name='cast_vote'),
    path('filter_position', views.filter_position, name='filter_position'),
    
]