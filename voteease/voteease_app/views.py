from itertools import count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime, timedelta
from json import dumps
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F

def login_registration(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        # print("POST Data:", request.POST)
        if 'register_btn' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Your account is successfully created.')
                form.save()
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        # Add each error message individually to the Django messages
                        messages.warning(request, f"{error}")
                return redirect('login_registration')

        else:
            user_email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=user_email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully!')
                return redirect('votingsystemUi2')
            else:
                messages.error(request, 'Login Failed. Please check your credentials and try again.')
                return redirect('login_registration')


    candidates = Candidate.objects.all().select_related('position').order_by('-vote_count')
    
    all_position = Position.objects.all()
    context = {'candidates': candidates,
                'all_position': all_position,
                'is_login_page': True
                }
    return render(request, 'votingsystemUi.html', context)

@login_required
def add_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('positions')  
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{field}' has error: {error}")

            error_string = ''.join([''.join(x for x in l) for l in list(form.errors.values())])
            
            CRITICAL = 50
            error_string = ''.join([''.join(x for x in l)
                                    for l in list(form.errors.values())])
            messages.add_message(request, CRITICAL, str(error_string))
    else:
        form = PositionForm()

    all_position = Position.objects.all()
    context = {'all_position': all_position,
                }

    return render(request, 'votingsystemUi3.html', context)

@login_required
def votingsystem_ui2_view(request):
    all_candidates = Candidate.objects.all().prefetch_related(
        'educations', 
        'leadership_experiences',
        'awards'
    )
    all_position = Position.objects.all()
    context = {'all_candidates': all_candidates,
                'all_position': all_position,
                }
    return render(request, 'votingsystemUi2.html', context)


def logout_user(request):
    user= request.user
    current_date =  datetime.now()
    format_date =  current_date.strftime("%Y/%m/%d, %H:%M:%S")
    logout(request)
    return redirect('login_registration')
    
@login_required
def positions(request):
    all_position = Position.objects.all()
    voted_positions = {}
    if request.user.is_authenticated and request.user.user_type == 'student':
        # For each position, check if the user has voted
        for position in all_position:
            has_voted = Vote.objects.filter(user=request.user, position=position).exists()
            voted_positions[position.id] = has_voted

    context = {
        'all_position': all_position,
        'voted_positions': voted_positions,
    }
    return render(request, 'votingsystemUi3.html', context)

    # context = {'all_position': all_position,
    #             }
    # return render(request, 'votingsystemUi3.html', context)

@login_required
def render_candidates(request):
    all_candidates = Candidate.objects.all()
    all_position = Position.objects.all()
    context = {'all_candidates': all_candidates,
                'all_position': all_position,
                }
    return render(request, 'votingsystemUi4.html', context)

@login_required
def candidates(request):
    all_position = Position.objects.all()
    context = {'all_position': all_position,}
    return render(request, 'votingsystemUi4.html', context)

@login_required
def open_create_candidate(request):
    all_position = Position.objects.all()
    context = {
                'all_position': all_position,
                }
    return render(request, 'votingsystemUi5.html', context)

@login_required
def delete_position(request, position_id):
    if request.method == 'POST':
        position = get_object_or_404(Position, id=position_id)
        position.delete()
    return redirect('positions')

@login_required
def delete_candidate(request, candidate_id):
    if request.method == 'POST':
        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate.delete()
    return redirect('candidates')

@login_required
def create_candidate(request):
    if request.method == 'POST':
        submitted_data = request.POST
        candidate_form = CandidateForm(request.POST, request.FILES)
        test = request.FILES.get('ps_image')
        print(test)
        
        education_entries = []
        education_indices = set()
        for key in request.POST:
            if key.startswith('education['):
                index = key.split('[')[1].split(']')[0]
                if index.isdigit():
                    education_indices.add(index)

        for index in education_indices:
            institution_name = request.POST.get(f'education[{index}][institution_name]')
            start_year = request.POST.get(f'education[{index}][start_year]')
            end_year = request.POST.get(f'education[{index}][end_year]')
            description = request.POST.get(f'education[{index}][description]')

            education_entries.append({
                'institution_name': institution_name,
                'start_year': start_year,
                'end_year': end_year,
                'description': description,
            })

        leadership_entries = []
        leadership_indices = set()
        for key in request.POST:
            if key.startswith('leadership['):
                index = key.split('[')[1].split(']')[0]
                if index.isdigit():
                    leadership_indices.add(index)

        for index in leadership_indices:
            position = request.POST.get(f'leadership[{index}][position]')
            organization = request.POST.get(f'leadership[{index}][organization]')
            start_year = request.POST.get(f'leadership[{index}][start_year]')
            description = request.POST.get(f'leadership[{index}][description]')

            leadership_entries.append({
                'position': position,
                'organization': organization,
                'start_year': start_year,
                'description': description,
            })

        award_entries = []
        award_indices = set()
        for key in request.POST:
            if key.startswith('award['):
                index = key.split('[')[1].split(']')[0]
                if index.isdigit():
                    award_indices.add(index)

        for index in award_indices:
            award_name = request.POST.get(f'award[{index}][award_name]')
            year = request.POST.get(f'award[{index}][year]')
            description = request.POST.get(f'award[{index}][description]')

            award_entries.append({
                'award_name': award_name,
                'year': year,
                'description': description,
            })


        if candidate_form.is_valid():
            
            candidate = candidate_form.save()

            for entry in education_entries:
                Education.objects.create(
                    candidate=candidate,
                    institution_name=entry['institution_name'],
                    start_year=entry['start_year'],
                    end_year=entry['end_year'],
                    description=entry['description'])

            for entry in leadership_entries:
                LeadershipExperience.objects.create(
                    candidate=candidate,
                    position=entry['position'],
                    organization=entry['organization'],
                    start_year=entry['start_year'],
                    description=entry['description'])

            for entry in award_entries:
                Award.objects.create(
                    candidate=candidate,
                    award_name=entry['award_name'],
                    year=entry['year'],
                    description=entry['description'])

            return redirect('candidates')  

        else:
            return render(request, 'votingsystemUi5.html', {
                'all_position': Position.objects.all(),
                'submitted_data': submitted_data,
            })
            

    all_position = Position.objects.all()

    return render(request, 'votingsystemUi5.html', {
        'candidate_form': candidate_form,
        'all_position': all_position
    })

@login_required
def cast_vote(request, candidate_id):
    if request.method == 'POST':
        if not request.user.is_authenticated or request.user.user_type != 'student':
            return redirect('login_registration')
        
        candidate = get_object_or_404(Candidate, id=candidate_id)
        position = candidate.position
        
        if Vote.objects.filter(user=request.user, position=position).exists():
            messages.warning(request, f"You've already voted for the position: {position.position_name}!")
            return redirect('votingsystemUi2')
        
        # Create vote record
        Vote.objects.create(
            user=request.user,
            candidate=candidate,
            position=position
        )
        
        # Update vote count atomically
        Candidate.objects.filter(id=candidate_id).update(vote_count=F('vote_count') + 1)
        candidate.refresh_from_db() 
        
        messages.success(request, "Vote cast successfully!")
        return redirect('votingsystemUi2')
    
    return redirect('votingsystemUi2')


def filter_position(request):
    positions = Position.objects.all()
    
    # Handle POST request to filter candidates by selected position
    if request.method == 'POST':
        selected_position_id = request.POST.get('position_id')
        if selected_position_id == 'all':
            candidates = Candidate.objects.all()  # Return all candidates if 'all' is selected
        else:
            candidates = Candidate.objects.filter(position_id=selected_position_id)
    else:
        candidates = Candidate.objects.all()  # Show all candidates by default

    return render(request, 'votingsystemUi.html', {
        'candidates': candidates,
        'positions': positions,
        'is_login_page': False
    })

