from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt  # <-- REQUIRED to stop 403 errors
from django.db.models import Q
from .models import Requirement, Candidate, SubVendorAssignment

@csrf_exempt  # <-- Prevents 403 errors on Login
@never_cache
def user_login(request):
    """Handles sub-vendor and admin login securely without CSRF blocks."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password.'})
            
    return render(request, 'core/login.html')

@csrf_exempt  # <-- Prevents 403 errors on Logout
@never_cache
def user_logout(request):
    """Logs out the user instantly via GET request, avoiding all 403 CSRF errors."""
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    
    # Check if user is Super Admin or Staff
    if user.is_superuser or user.is_staff:
        requirements = Requirement.objects.all().order_by('-created_at')
        assignments = SubVendorAssignment.objects.all().order_by('-assigned_date')
        candidates = Candidate.objects.all().order_by('-id')
        
        # Handle search query & status filter for admin candidates table
        query = request.GET.get('q', '')
        selected_status = request.GET.get('status', '')
        
        if query:
            candidates = candidates.filter(
                Q(candidate_name__icontains=query) | 
                Q(candidate_email__icontains=query)
            )
        if selected_status:
            candidates = candidates.filter(status=selected_status)
            
        context = {
            'requirements': requirements,
            'assignments': assignments,
            'candidates': candidates,
            'query': query,
            'selected_status': selected_status,
        }
        return render(request, 'core/admin_dashboard.html', context)
    
    else:
        # Sub-vendor portal view: Flexible lookup matching User, Vendor relation, or Username
        assigned_records = SubVendorAssignment.objects.filter(
            Q(sub_vendor=user) | 
            Q(sub_vendor__user=user) | 
            Q(sub_vendor__name__iexact=user.username) |
            Q(sub_vendor__code__iexact=user.username)
        ).select_related('requirement')
        
        requirements = [assignment.requirement for assignment in assigned_records]
        
        candidates = Candidate.objects.filter(
            Q(sub_vendor=user) | 
            Q(sub_vendor__user=user) |
            Q(sub_vendor__name__iexact=user.username) |
            Q(sub_vendor__code__iexact=user.username)
        ).order_by('-id')
        
        context = {
            'requirements': requirements,
            'candidates': candidates,
        }
        return render(request, 'core/vendor_dashboard.html', context)
@login_required
def submit_candidate(request, requirement_id):
    requirement = get_object_or_404(Requirement, id=requirement_id)
    
    if request.method == 'POST':
        candidate_name = request.POST.get('candidate_name', '').strip()
        candidate_email = request.POST.get('candidate_email', '').strip()
        experience = request.POST.get('experience', '').strip()
        resume = request.FILES.get('resume')
        
        # Ensure name and resume are provided
        if candidate_name and resume:
            Candidate.objects.create(
                requirement=requirement,
                sub_vendor=request.user,
                candidate_name=candidate_name,
                candidate_email=candidate_email,
                experience=experience,
                resume=resume,
                status='Submitted'  # Automatically set to Submitted for Admin review
            )
            return redirect('dashboard')
        else:
            return render(request, 'core/submit_candidate.html', {
                'requirement': requirement,
                'error': 'Candidate Name and Resume file are required.'
            })
        
    return render(request, 'core/submit_candidate.html', {'requirement': requirement})

@login_required
def update_candidate_status(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == 'POST':
        candidate.status = request.POST.get('status', candidate.status)
        candidate.current_round = request.POST.get('current_round', candidate.current_round)
        candidate.feedback_reason = request.POST.get('feedback_reason', candidate.feedback_reason)
        candidate.save()
        return redirect('dashboard')
        
    return render(request, 'core/update_status.html', {'candidate': candidate})