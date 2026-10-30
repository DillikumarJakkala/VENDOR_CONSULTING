from django.db import models
from django.contrib.auth.models import User

# 1. Company/Client Requirement Model
class Requirement(models.Model):
    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    skills_required = models.TextField()
    experience_required = models.CharField(max_length=50)
    profiles_needed = models.IntegerField(default=5)  # <-- Added this field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title} (Target: {self.profiles_needed})"

# 2. Assignment Model (Assigns specific JDs to Sub-vendors safely)
class SubVendorAssignment(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    sub_vendor = models.ForeignKey(User, on_delete=models.CASCADE)  # Must match 'sub_vendor'
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sub_vendor.username} -> {self.requirement.job_title}"

# 3. Candidate Tracking & Feedback Model
class Candidate(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]

    ROUND_CHOICES = [
        ('Screening', 'Screening'),
        ('L1 Technical', 'L1 Technical'),
        ('L2 Technical', 'L2 Technical'),
        ('Managerial', 'Managerial'),
        ('HR Round', 'HR Round'),
    ]

    requirement = models.ForeignKey('Requirement', on_delete=models.CASCADE)
    sub_vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=200)
    candidate_email = models.EmailField()
    experience = models.CharField(max_length=50)
    resume = models.FileField(upload_to='resumes/')
    
    # Fields managed EXCLUSIVELY by Company/Admin:
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted')
    current_round = models.CharField(max_length=50, choices=ROUND_CHOICES, default='Screening')
    interview_date = models.DateTimeField(null=True, blank=True)  # Company sets interview date/time
    feedback_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.candidate_name} ({self.status})"