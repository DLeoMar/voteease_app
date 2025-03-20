from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login_registration, name='login_registration'),
    # path('', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    path('votingsystemUi2/', views.votingsystem_ui2_view, name='votingsystemUi2'), 
    path('logout', views.logout_user, name='logout'),
    path('positions', views.positions, name='positions'),
    # path('positions', views.positions, name='positions'),
    path('candidates', views.render_candidates, name='candidates'),
    path('candidates/add_candidate', views.open_create_candidate, name='add_candidate'),
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('delete-position/<int:position_id>/', views.delete_position, name='delete_position'),
    path('delete-candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('add_position/', views.add_position, name='add_position'),
    path('cast-vote', views.cast_vote, name='cast_vote'),
    path('filter_position', views.filter_position, name='filter_position'),
    
    # #privacy policy
    # path('privacyPolicy', views.privacyPolicy, name='privacyPolicy'),

    # # Parent
    # path('home', views.parent_home, name='parent_home'),
    # path('preschooler/<str:pk>/', views.parent_preschooler, name='parent_preschooler'),
    # path('PG_password/<str:pk>/', views.change_pass, name='PG_pass'),

    

    # # Admin
    # path('ahome', views.admin_home, name='admin_home'),
    # path('apreschoolers', views.admin_preschoolers, name='admin_home2'),
    # path('apreschoolersbarangay/<str:brgy>/', views.admin_preschoolers_barangay, name='apreschoolersb'),
    # path('avalidation', views.bhw_validation, name='bhw_validation'),
    # path('validate_profile/<str:pk>/', views.unvalidated_profile, name='unvalidated_profile'),
    # path('delete_profile/<str:pk>/', views.delete_profile, name='delete_profile'),
    # path('abarangay', views.admin_barangay, name='admin_barangay'),
    # path('set_password/<str:pk>/', views.set_pass, name='set_pass'),
    # path('auseraccounts', views.admin_userAccounts, name='admin_userAccounts'),
    # path('aHistoryLogs', views.admin_historyLogs, name='admin_historyLogs'),



    # # Barangay Health Worker
    # path('bhwhome', views.bhw_home, name='bhw_home'),
    # path('preschooler_dashboard', views.preschooler_dashboard, name='preschooler_dashboard'),
    # path('preschooler_profile/<str:pk>/', views.preschooler_profile, name='preschooler_profile'),
    # path('update_preschooler', views.update_preschooler, name='update_preschooler'),
    # path('preschooler_profile/immunization/<str:pk>/', views.immunization_schedule, name='immunization_schedule'),
    # path('new_password/<str:pk>/', views.change_pass, name='new_pass'),
    
]