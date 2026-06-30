# Final Campus Management System Documentation

*(This is your living document. Copy-paste from here into your Word document.)*

---

## CHAPTER 1: INTRODUCTION

**1.1 Background**
Managing a college campus or hostel manually involves a massive amount of paperwork, from tracking student leaves on physical registers to managing daily food counts in the mess. These manual processes are often time-consuming, prone to human error, and make it difficult for administrators to quickly access student records or track complaints. With the rapid digitization of educational institutions, there is a strong need for a centralized platform to handle these daily operations efficiently. This project aims to digitize and automate the core processes of campus management, providing a seamless experience for students, staff, and administrators.

**1.2 Features of the System**
The system provides a comprehensive management platform with the following key features:
1. **User Authentication:** Secure login for Admins, Staff, and Students.
2. **Profile Management:** Detailed digital profiles for students (including emergency contacts and document uploads) and staff.
3. **Leave Management:** Students can apply for leave online, and staff/admins can approve or reject them digitally.
4. **Meal RSVP System:** Students can opt-in or out of daily meals (Breakfast, Lunch, Snacks, Dinner) to prevent food wastage.
5. **Complaint Tracking:** Students can raise issues, upload photos of problems, and track the resolution status.
6. **Marks Card Verification:** Students can upload semester marks cards for admin verification.
7. **Notification System:** Real-time alerts for holidays, meetings, and important campus announcements.

**1.3 Basic Overview**
This project replaces traditional paper-based campus management with a modern web application. It leverages Python and the Flask framework for robust backend logic, and HTML/CSS for a responsive, user-friendly interface. The system ensures that all data regarding students, leaves, and food requirements are stored securely in a relational database, allowing for quick retrieval and report generation by the administration.

**1.4 Objectives of the System**
The primary objectives of the system are:
1. To eliminate paper-based leave applications and manual tracking.
2. To optimize food preparation in the hostel mess by tracking daily student meal RSVPs.
3. To provide a secure, centralized database for student and staff records.
4. To create a transparent complaint resolution mechanism.
5. To improve communication across the campus via a digital notification board.

**1.5 Scope of the System**
The scope of this project is focused on the internal operations of a college campus or hostel. It covers student profiling, leave tracking, daily meal management, and grievance redressal. The system is designed to be used by enrolled students, assigned staff members, and the core administrative team. It does not currently handle external processes like new student admissions or online fee payments.

**1.6 Structure of the System**
The application is organized into three main modules:
1. **Admin Module:** Complete control over the system, ability to view reports, manage all users, and resolve complaints.
2. **Staff Module:** Focused on managing students assigned to them, specifically approving leave requests and viewing student profiles.
3. **Student Module:** The student-facing interface for applying for leaves, RSVPing for meals, raising complaints, and viewing notices.

**1.7 End Users**
*   **Students:** Interact with the system daily for meals and leaves.
*   **Staff Members:** Use the system to manage student requests.
*   **Administrators:** Use the system for overall oversight and reporting.

**1.8 Software/Hardware Used for Development**
*   **Programming Language:** Python 3.x
*   **Framework:** Flask
*   **Database:** SQLite / MySQL
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Hardware Minimum:** Intel Core i3 processor, 4GB RAM

---

## CHAPTER 2: LITERATURE SURVEY

**2.1 Introduction**
Before developing the Campus Management System, existing solutions for hostel and college automation were analyzed to understand current industry standards and identify areas for improvement.

**2.2 Literature Review**
*(ACTION REQUIRED: To avoid AI detection and plagiarism, you must write this section yourself. Go to Google Scholar, search for "Hostel Management System IEEE" or similar. Find 3 papers. For each paper, write the Author name, Year, and 3-4 sentences explaining what their system did. It is very easy and takes 10 minutes!)*

**2.3 Comparative Analysis**
*(ACTION REQUIRED: Once you find your 3 papers, you will create a small table here comparing them to your system. e.g., "Paper 1 had leave management but no food tracking. My system has both.")*

**2.4 Conclusion of Literature Review**
Based on the review of existing systems, it was observed that many solutions focus heavily on either academics or hostel booking, but lack daily operational tools like detailed meal RSVPs and digital outpasses. The proposed system bridges this gap by integrating daily living management (food, leave, complaints) into a single, cohesive platform.

---

## CHAPTER 3: METHODOLOGY

**3.1 Research Design**
The project adopts a modular design and development methodology. The system was broken down into distinct functional areas (Authentication, Admin operations, Student tasks, Staff tasks) which were developed and tested iteratively. This approach ensures that each module works independently before being integrated into the final web application.

**3.2 Data Collection**
Data is collected dynamically through user interaction with the web forms. For example, student details are collected during profile completion, while daily operational data (leaves, RSVPs) is generated continuously as students use the system. Document uploads (like Aadhaar cards or marks cards) are securely stored on the server file system with their paths referenced in the database.

**3.3 Tools and Technologies**
*   **Flask (Python):** Chosen as the backend framework for its lightweight nature and flexibility in building web applications rapidly.
*   **SQLAlchemy:** Used as the Object Relational Mapper (ORM) to securely interact with the database using Python objects instead of raw SQL queries.
*   **HTML/CSS:** Used to design clean, responsive user interfaces that are accessible on both desktop and mobile browsers.

---

## CHAPTER 4: SYSTEM REQUIREMENTS

**4.1 Hardware Requirements**
*   **Processor:** Intel Core i3 / i5, 2.4 GHz (Minimum)
*   **RAM:** 4 GB (8 GB Recommended)
*   **Hard Disk:** 50 GB available space
*   **Network:** Active Internet/Intranet connection

**4.2 Software Requirements**
*   **Operating System:** Windows 10/11 or Linux
*   **Programming Language:** Python 3.x
*   **Development Tools:** Visual Studio Code
*   **Web Browser:** Google Chrome, Microsoft Edge, or Mozilla Firefox
*   **Server:** Built-in Flask development server (or Waitress/Gunicorn for production)

---

## CHAPTER 5: SYSTEM DESIGN (Functional Design)

**5.1 Introduction**
System design is the process of defining the architecture, components, and interfaces required to satisfy the project's requirements. For this Campus Management System, the design focuses on ensuring smooth data flow between the student's browser and the college's server, maintaining strict role-based access control.

**5.3 System Architecture**
The system follows a standard Client-Server architecture utilizing the Model-View-Controller (MVC) pattern (implemented via Flask's routing and templates). 
*   **Client (View):** The HTML/CSS templates rendered in the user's browser.
*   **Server (Controller):** The Flask routes that handle requests, process logic, and return responses.
*   **Database (Model):** The SQLAlchemy models defining the data structure.

**5.4 Description of Programs (Data Flow Diagrams - DFD)**
*(ACTION REQUIRED: You will need to draw these diagrams in a tool like draw.io or Microsoft Word. Here is exactly what to draw:)*

*   **Context Diagram (Level 0 DFD):** 
    *   Draw one big circle in the middle called "Campus Management System".
    *   Draw 3 squares around it: "Student", "Admin", "Staff".
    *   Draw an arrow from Student to the System labeled "Leave Request, Meal RSVP, Complaints".
    *   Draw an arrow from System to Admin labeled "Reports, Profiles".
    *   Draw an arrow from System to Staff labeled "Leave Approvals".

*   **Level 1 DFD:**
    *   Break the system down into multiple circles: "1.0 Manage Users", "2.0 Manage Leaves", "3.0 Manage Food Menu", "4.0 Manage Complaints".
    *   Show how data from the Student square flows into these specific circles, and how the circles save data to a "Database" data store (drawn as an open rectangle).

---

## CHAPTER 6: DATABASE DESIGN

### 6.5 Table Definition

**i. Structure of Table “users”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique identifier for each user |
| email | varchar | 255 | UNIQUE, NOT NULL | User's email address |
| password_hash | varchar | 255 | NOT NULL | Encrypted password |
| role | enum | - | NOT NULL | Role of user (admin, student, staff) |
| created_at | datetime | - | - | Timestamp of account creation |

**ii. Structure of Table “student_profile”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique profile ID |
| user_id | int | 11 | FOREIGN KEY, UNIQUE | Link to users table |
| full_name | varchar | 120 | NOT NULL | Student's full name |
| dob | date | - | NOT NULL | Date of birth |
| mobile | varchar | 20 | NOT NULL | Student's contact number |
| guardian_name | varchar | 120 | - | Name of local guardian |
| emergency_contact| varchar | 20 | - | Emergency phone number |
| course | varchar | 120 | - | Enrolled course name |
| diet | enum | - | DEFAULT 'veg' | Food preference |
| status | varchar | 20 | DEFAULT 'Pending' | Profile verification status |

**iii. Structure of Table “leave_requests”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique leave request ID |
| user_id | int | 11 | FOREIGN KEY, NOT NULL | Link to student requesting leave |
| leave_type | varchar | 50 | NOT NULL | Type (casual, outpass, etc.) |
| reason | text | - | NOT NULL | Reason provided for leave |
| from_date | date | - | NOT NULL | Start date of leave |
| to_date | date | - | NOT NULL | End date of leave |
| status | varchar | 20 | DEFAULT 'Pending' | Current approval status |
| is_returned | boolean | - | DEFAULT False | Check if student has returned |
| attachment_path| varchar | 255 | - | Path to uploaded proof document |
| ocr_text | text | - | - | Text extracted from attachment |

**iv. Structure of Table “staff_profiles”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique profile ID |
| user_id | int | 11 | FOREIGN KEY, UNIQUE | Link to users table |
| full_name | varchar | 120 | NOT NULL | Staff's full name |
| specialty | varchar | 120 | NOT NULL | Role or department |
| phone | varchar | 20 | - | Contact number |
| email | varchar | 120 | - | Email address |
| status | varchar | 20 | DEFAULT 'On Duty'| Current availability status |

**v. Structure of Table “complaints”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique complaint ID |
| user_id | int | 11 | FOREIGN KEY, NOT NULL | Link to user making complaint |
| category | varchar | 50 | NOT NULL | Type of complaint |
| description | text | - | NOT NULL | Detailed issue description |
| image_path | varchar | 255 | - | Path to uploaded photo |
| status | varchar | 20 | DEFAULT 'Pending'| Issue resolution status |
| admin_notes | text | - | - | Updates from admin |

**vi. Structure of Table “food_menu”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique menu ID |
| day | varchar | 20 | UNIQUE, NOT NULL | Day of the week |
| breakfast | varchar | 200 | - | Breakfast items |
| lunch | varchar | 200 | - | Lunch items |
| snacks | varchar | 200 | - | Snack items |
| dinner | varchar | 200 | - | Dinner items |

**vii. Structure of Table “meal_rsvps”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique RSVP ID |
| user_id | int | 11 | FOREIGN KEY, NOT NULL | Link to student |
| date | date | - | NOT NULL | Date of RSVP |
| eating_breakfast| boolean | - | DEFAULT True | Attending breakfast |
| eating_lunch | boolean | - | DEFAULT True | Attending lunch |
| eating_dinner | boolean | - | DEFAULT True | Attending dinner |

**viii. Structure of Table “marks_cards”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique marks card ID |
| user_id | int | 11 | FOREIGN KEY, NOT NULL | Link to student |
| semester | int | 11 | NOT NULL | Academic semester |
| file_path | varchar | 255 | NOT NULL | Path to uploaded marks card |
| status | varchar | 20 | DEFAULT 'Pending'| Verification status |
| extracted_cgpa | varchar | 10 | - | CGPA read from document |

**ix. Structure of Table “rooms”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique room ID |
| number | varchar | 50 | UNIQUE, NOT NULL | Room identifier |

**x. Structure of Table “notifications”:**
| Field Name | Field Type | Size | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| id | int | 11 | PRIMARY KEY | Unique notification ID |
| title | varchar | 150 | NOT NULL | Alert title |
| description | text | - | NOT NULL | Alert message details |
| category | varchar | 50 | NOT NULL | Alert type (Holiday, etc.) |
| priority | varchar | 20 | DEFAULT 'Normal' | Alert importance level |
| target_role | varchar | 20 | - | Specific group to notify |

---

## CHAPTER 7: DETAILED DESIGN

**7.1 Introduction**
Detailed design specifies the internal logic and structure of individual modules and their interactions. It acts as a detailed blueprint for the system, bridging the gap between high-level requirements and actual coding.

**7.2 Structure of the Software Package (Structure Chart)**
The system is divided into three main functional modules based on user roles.
*(ACTION REQUIRED: Draw a hierarchical chart. Put "Campus Management System" at the top. Draw three boxes below it: "Admin Module", "Staff Module", and "Student Module".)*

**7.3 Modular Decomposition Components**

**7.3.1 Admin Module:** 
This module gives full control to the system administrators. They can manage global system settings, oversee all users (staff and students), view comprehensive reports on leaves and meals, and handle escalated complaints.

**7.3.2 Staff Module:** 
This module acts as an intermediary. Staff members are primarily responsible for reviewing and approving/rejecting leave requests from the students assigned to them, and viewing basic student profiles.

**7.3.3 Student Module:** 
The primary user interface where students manage their daily activities. Students can update their profile, apply for leaves, RSVP for upcoming meals, and raise complaints regarding hostel facilities.

**7.4 Interaction Between Modules**
The modules interact heavily through the central database. For instance, a student (Student Module) submits a leave request, which changes a status in the database. The staff member (Staff Module) sees this updated status and approves it. The Admin (Admin Module) can then view the entire history of this transaction.

**7.5 System Models**
*(ACTION REQUIRED: You need to draw the following diagrams. You can draw them on paper and take photos, or use a tool like draw.io.)*

**7.5.1 Use Case Diagram**
*   **Actors (Draw as stick figures on the left):** Student, Staff, Admin.
*   **Use Cases (Draw as ovals in the middle):** Login, Manage Profile, Request Leave, Approve Leave, Submit Meal RSVP, Raise Complaint, View Reports.
*   **Connections (Draw lines connecting them):**
    *   Student connects to: Login, Manage Profile, Request Leave, Submit Meal RSVP, Raise Complaint.
    *   Staff connects to: Login, Approve Leave.
    *   Admin connects to: Login, View Reports, Manage Users.

**7.5.2 Class Diagram**
*   Draw boxes representing the main database tables we defined in Chapter 6 (User, StudentProfile, LeaveRequest, FoodMenu, Complaint).
*   Inside each box, list 3 or 4 of the main attributes (e.g., in the LeaveRequest box, write `id`, `leave_type`, `status`).

**7.5.3 Sequence Diagram (Example: Leave Request Process)**
*   **Lifelines (Boxes at the top with dashed lines going down):** Student, Web Browser, Server, Database.
*   **Sequence of arrows going back and forth:**
    1. Student -> Browser: Clicks "Request Leave"
    2. Browser -> Server: Sends Leave Details (POST)
    3. Server -> Database: Insert Leave Record
    4. Database -> Server: Confirm Success
    5. Server -> Browser: Render Success Page
    6. Browser -> Student: Display "Leave Requested Successfully"

---

## CHAPTER 8: IMPLEMENTATION (CODING)

**8.1 Introduction**
This chapter provides an overview of the core source code files developed for the Campus Management System. The project is built using Python with the Flask framework, ensuring modularity and maintainability.

**8.2 Key Source Code Files**
*(ACTION REQUIRED: You can simply copy-paste a few small snippets of your code into your final Word document under this section, or just list these files to show the examiner how the project is structured.)*

*   `run.py`: The main entry point of the application that starts the server.
*   `config.py`: Contains system configurations, such as the database connection string.
*   `app/models/`: Contains the database schemas (`user.py`, `student_profile.py`, `leave_request.py`, etc.) mapped using SQLAlchemy.
*   `app/auth/routes.py`: Handles secure user login, registration, and password hashing.
*   `app/admin/routes.py`: Contains the logic for the administrator dashboard, report generation, and user management.
*   `app/student/routes.py`: Manages student-facing logic such as applying for leaves and submitting meal RSVPs.
*   `app/staff/routes.py`: Handles staff-facing logic like approving or rejecting assigned student leaves.

---

## CHAPTER 9: SYSTEM INTERFACES (USER INTERFACE)

**9.1 Introduction**
The User Interface (UI) is the front-end interaction layer of the Campus Management System. It was designed using HTML5, CSS3, and Bootstrap to ensure a responsive and intuitive experience across both desktop and mobile devices.

**9.2 Screen Layouts**
*(ACTION REQUIRED: Take screenshots of your running website and paste them below each heading in your Word document.)*

*   **9.2.1 Login Screen:** Screenshot of the login page showing email and password fields.
*   **9.2.2 Admin Dashboard:** Screenshot showing the high-level admin statistics and navigation menu.
*   **9.2.3 Student Profile Form:** Screenshot showing where a student enters their emergency contact and uploads documents.
*   **9.2.4 Leave Request Page:** Screenshot of the form where students select "Outpass" or "Casual" leave.
*   **9.2.5 Staff Leave Approval:** Screenshot showing the table where staff members can click "Approve" or "Reject".
*   **9.2.6 Meal RSVP Menu:** Screenshot showing the daily food menu and the checkboxes to attend meals.

---

## CHAPTER 10: SOFTWARE TESTING

**10.1 Introduction**
Testing is a critical phase of software development aimed at finding and resolving defects to ensure the system functions exactly as required. The Campus Management System underwent various levels of testing, primarily focusing on functional and validation testing.

**10.2 Types of Testing Executed**
*   **Unit Testing:** Individual forms (like the login form) were tested to ensure they validate empty fields correctly.
*   **Integration Testing:** The flow between modules was tested (e.g., ensuring a leave request submitted by a student correctly appears in the staff dashboard).
*   **System Testing:** The entire application was run from end-to-end to verify that all requirements were met.

**10.3 Test Cases**
*(Below are standard test cases based on your project. You can copy these directly into your report.)*

| Test Case ID | Test Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-01 | User attempts to login with incorrect password | System displays "Invalid credentials" error message | Displayed error message | Pass |
| TC-02 | Student submits leave request without selecting a date | Form prevents submission and highlights date field | Submission blocked | Pass |
| TC-03 | Staff member clicks "Approve" on a pending leave | Leave status updates to "Approved" in the database | Status updated | Pass |
| TC-04 | Admin attempts to access a student-only page | System redirects admin to dashboard with "Unauthorized" error | Redirected correctly | Pass |
| TC-05 | Student RSVPs for "Lunch" | Database records a boolean True for that specific date | Recorded successfully | Pass |

---

## CHAPTER 11: CONCLUSION & FUTURE ENHANCEMENTS

**11.1 Conclusion**
The development of the Campus Management System has successfully demonstrated how manual, paper-based hostel and campus operations can be digitized. By providing dedicated modules for Admins, Staff, and Students, the system has streamlined leave processing, optimized daily food tracking, and established a secure, centralized database for student records. The use of the Flask framework proved effective in creating a robust and scalable web application.

**11.2 Future Enhancements**
While the current system fulfills the primary objectives, future updates could include:
1.  **Payment Gateway Integration:** To allow students to pay hostel and mess fees directly through the portal.
2.  **Mobile Application:** Developing a dedicated Android/iOS app for push notifications regarding leaves and complaints.
3.  **Advanced Analytics:** Implementing AI-driven reports to predict food consumption trends and reduce mess wastage further.
4.  **Facial Recognition Attendance:** Integrating computer vision to automate daily student attendance in the hostel.
