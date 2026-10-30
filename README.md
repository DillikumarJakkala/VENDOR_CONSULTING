# B2B Recruitment Vendor Management System (VMS)

A role-based B2B Recruitment VMS built with Python and Django to manage job requirements, sub-vendor candidate submissions, resume downloads, and interview stage tracking.

## Tech Stack & Dependencies
- **Backend**: Python 3.12, Django 6.1.2
- **Image/File Handling**: Pillow (for resume & media processing)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3

## Core Features
1. **Admin Dashboard**:
   - Metric summary cards (Total Jobs, Total Candidates).
   - Manage job requirements and target `Profiles Needed`.
   - Sub-vendor assignment management.
   - Search & Filter candidate profiles by name or recruitment status.
   - Resume downloads and interview stage updates (`Submitted`, `Shortlisted`, `Interviewing`, `Offered`, `Rejected`).
2. **Sub-Vendor Portal**:
   - View assigned client requirements & target profile counts.
   - Upload candidate details along with resume files.
   - Track candidate interview progress and feedback in real time.

## How to Run Locally
1. Navigate to the project directory:
   ```bash
   cd vms_project