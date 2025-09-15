# Convade (LMS)

Welcome to Convade - a comprehensive learning management system built with Django that supports different user roles and provides a complete educational platform.

## 🚀 Project Overview

Convade is a full-featured learning management system that allows students to enroll in courses, take tests, earn badges and certificates, while providing teachers and administrators with powerful tools to manage content and track progress.

## 🏗️ Architecture

The application is built with Django and follows a modular architecture with separate apps for different functionalities:

- **accounts**: User management with role-based access (Student, Teacher, Admin)
- **courses**: Course creation, management, and enrollment
- **tests**: Quiz and exam system with various question types
- **badges**: Gamification with badge rewards and rules
- **certifications**: Certificate generation and verification
- **analytics**: Performance tracking and reporting
- **helpcenter**: Support system with FAQ and tickets

## 📋 Features by Role

### 👨‍🎓 Students
- **Account Management**: Signup/login with social authentication (Google, Facebook)
- **Course Enrollment**: Browse and enroll in courses
- **Learning Progress**: Track course completion and progress
- **Assessments**: Take quizzes and exams with timer functionality
- **Achievements**: Earn and view badges
- **Certifications**: Download verified certificates
- **Support**: Access help center and submit support tickets

### 👩‍🏫 Teachers
- **Course Management**: Create and manage courses with multimedia content
- **Content Creation**: Add videos, text, quizzes, and assignments
- **Assessment Tools**: Create tests with multiple question types
- **Student Tracking**: View student progress and performance
- **Badge System**: Create and manage badge reward rules
- **Analytics**: Access detailed reports on course performance

### 🛠️ Admins
- **User Management**: Create, edit, and manage user accounts and roles
- **System Analytics**: View comprehensive system reports
- **Content Moderation**: Manage all courses and content
- **Support Management**: Handle support tickets and help content
- **System Settings**: Configure site-wide features and settings

## 🛠️ Technology Stack

- **Backend**: Django 5.2.3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development) - easily configurable for PostgreSQL/MySQL
- **Authentication**: Django Allauth with social login support
- **UI Components**: Django Crispy Forms, Widget Tweaks
- **API**: Django REST Framework
- **File Handling**: Pillow for image processing

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd convade_webapp
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  
   if On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📊 Database Models

### Core Models

#### User (Custom User Model)
- Role-based system (Student, Teacher, Admin)
- Profile information and preferences
- Social authentication support

#### Course System
- **Course**: Main course entity with instructor, difficulty, price
- **CourseContent**: Modular content (videos, text, quizzes)
- **Enrollment**: Student-course relationships with progress tracking
- **CourseCategory**: Course organization and filtering

#### Assessment System
- **Test**: Quizzes and exams with timing and attempt limits
- **Question**: Multiple choice, true/false, text, and essay questions
- **TestSubmission**: Student test attempts with scoring
- **StudentAnswer**: Individual question responses

#### Gamification
- **Badge**: Achievement system with various badge types
- **BadgeRule**: Automated badge awarding rules
- **EarnedBadge**: User badge achievements

#### Certification
- **Certificate**: Course completion certificates
- **CertificateTemplate**: Customizable certificate designs
- **CertificateVerification**: Certificate authenticity verification

#### Analytics & Support
- **UserActivity**: Comprehensive activity tracking
- **SystemAnalytics**: Daily system metrics
- **SupportTicket**: Help desk functionality
- **HelpArticle**: Knowledge base content

## 🎨 Frontend Features

- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **Modern UI**: Clean, professional design with smooth animations
- **Interactive Elements**: AJAX-powered features for better UX
- **Accessibility**: Screen reader friendly and keyboard navigable
- **Progress Tracking**: Visual progress bars and completion indicators

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

<!-- client_max_body_size 50M; -->


### Social Authentication Setup
To enable Google and Facebook login:

1. **Google OAuth2:**
   - Go to Google Cloud Console
   - Create OAuth2 credentials
   - Add credentials to Django admin under Social Applications

2. **Facebook Login:**
   - Create a Facebook App
   - Add Facebook credentials to Django admin

## 📈 Analytics Features

- **User Engagement**: Track logins, course views, test attempts
- **Course Performance**: Enrollment rates, completion rates, average scores
- **System Metrics**: Daily active users, new registrations, revenue
- **Export Capabilities**: Download reports in various formats

## 🔒 Security Features

- **Role-based Access Control**: Granular permissions system
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM protection
- **Secure Authentication**: Password hashing and session management
- **File Upload Security**: Secure file handling with validation

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📱 API Endpoints

The application includes REST API endpoints for:
- Course management
- User authentication
- Progress tracking
- Analytics data

API documentation available at `/api/docs/` when running in development mode.

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up static file serving (WhiteNoise or CDN)
- [ ] Configure email backend for notifications
- [ ] Set up SSL certificates
- [ ] Configure domain and ALLOWED_HOSTS
- [ ] Create Superuser with `python manage.py createsuperuser --settings=convade_lms.settings_production`
- [ ] After using git pull on the vps - restart the server with 'sudo systemctl restart gunicorn'

### Recommended Deployment Platforms
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: App Platform or Droplets
- **AWS**: Elastic Beanstalk or EC2
- **Google Cloud**: App Engine or Compute Engine

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: support@convade.org
- Create an issue in the repository
- Check the help center within the application

## 🔄 Version History

### v1.0.0 (Current)
- Initial release with core LMS functionality
- User role management
- Course and test creation
- Badge and certificate system
- Analytics dashboard
- Help center and support system

---

**Built with ❤️ by the Convade Team** 