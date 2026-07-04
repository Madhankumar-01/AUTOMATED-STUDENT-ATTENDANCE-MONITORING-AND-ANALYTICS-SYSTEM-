# AUTOMATED-STUDENT-ATTENDANCE-MONITORING-AND-ANALYTICS-SYSTEM-


Automated Student Attendance Monitoring and Analytic System

Automated Student Attendance Monitoring and Analytic System is a web-based platform developed to simplify attendance tracking, monitoring, and performance analysis within educational institutions. The platform provides separate dashboards for Students, Teachers, and Administrators, enabling automated attendance recording, real-time analytics, alerts, and centralized reporting for improved academic administration.

Features


Student Module


Secure Student Login
View Dashboard
View Attendance Records
View Attendance Analytics (percentage, trends, subject-wise breakdown)
Access Announcements
Check Academic Information
Submit Reports/Requests
Profile Management

 Teacher Module


Secure Teacher Login
Mark & Manage Student Attendance
Automated Low-Attendance Alerts
View Attendance Analytics per Class/Student
Post Announcements
View Student Information
Generate Attendance Reports
Profile Management

Admin Module


Secure Admin Login
Manage Students
Manage Teachers
Manage Announcements
View System-Wide Attendance Reports
Attendance Analytics Dashboard (charts, trends, at-risk students)
Automated Alerts & Notifications
Database Management


Technologies Used


Frontend



HTML5
CSS3
JavaScript
Chart.js (for attendance analytics & graphs)


Backend



Python
Flask
Database

MySQL


Development Tools


Visual Studio Code
XAMPP
Git & GitHub



Project Structure


AttendanceMonitoringSystem/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── admin/
│   ├── student/
│   ├── teacher/
│   ├── login.html
│   └── index.html
│
├── app.py
├── database.sql
├── requirements.txt
├── README.md
└── LICENSE


Installation


1. Clone the Repository
bash
git clone https://github.com/yourusername/AttendanceMonitoringSystem.git
2. Navigate to the Project Folder
bash
cd AttendanceMonitoringSystem
3. Create a Virtual Environment (Optional)
bash
python -m venv venv
4. Activate the Virtual Environment
Windows

bash
venv\Scripts\activate
Linux / macOS

bash
source venv/bin/activate
5. Install Dependencies
bash
pip install -r requirements.txt
6. Configure the Database
Create a MySQL database.
Import the database.sql file.
Update the database configuration in app.py.
7. Run the Application
bash
python app.py
8. Open the Browser
http://127.0.0.1:5000/



Project Objectives


Automate the student attendance recording process.
Reduce manual errors and paperwork in attendance management.
Provide real-time attendance analytics for students, teachers, and admins.
Automatically flag students with low attendance for early intervention.
Provide secure role-based access.
Centralize academic and attendance-related information.
Enhance efficiency and transparency in campus administration.


User Roles


Role	Access


Student	View attendance, attendance analytics, announcements, profile
Teacher	Mark attendance, view analytics, generate reports, alerts
Admin	Full system management, analytics dashboard, and reporting


Analytics Highlights


Attendance percentage calculation (overall & subject-wise)
Attendance trend graphs (daily/weekly/monthly)
Automated at-risk student identification (below threshold %)
Class-wise and student-wise comparison reports
Visual dashboards using charts for quick insights

Future Enhancements


Mobile Application
QR Code / Biometric Attendance
Push Notifications
AI-powered Attendance Prediction
Parent Notification System
Timetable Integration
Cloud Deployment
Email Notifications for Low Attendance