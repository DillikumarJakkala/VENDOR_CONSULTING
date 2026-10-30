from django.contrib import admin
from .models import Requirement, SubVendorAssignment, Candidate

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_title', 'profiles_needed')

@admin.register(SubVendorAssignment)
class SubVendorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'sub_vendor')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'candidate_email', 'requirement', 'sub_vendor', 'status')
    list_filter = ('requirement', 'sub_vendor', 'status')
    search_fields = ('candidate_name', 'candidate_email')
    
admin.site.site_header = "SREENIDHI SOFTWARE SERVICES PRIVATE LIMITED"
admin.site.site_title = "Sreenidhi VMS Portal"
admin.site.index_title = "Welcome to Sreenidhi Management Portal"
    