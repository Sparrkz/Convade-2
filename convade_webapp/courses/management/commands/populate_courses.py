from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, CourseContent, CourseCategory, Enrollment
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with dummy courses for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing courses before creating new ones'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🧹 Clearing existing courses...')
            Course.objects.all().delete()
            CourseCategory.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS('🚀 Starting to populate courses...\n')
        )

        # Create instructors if they don't exist
        instructors = self.create_instructors()
        
        # Create categories
        categories = self.create_categories()
        
        # Create courses
        courses = self.create_courses(instructors, categories)
        
        # Add content to courses
        self.create_course_content(courses)
        
        # Create some enrollments
        self.create_enrollments(courses)
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {len(courses)} courses!')
        )

    def create_instructors(self):
        """Create instructor users"""
        instructors_data = [
            {
                'username': 'prof_smith',
                'email': 'smith@convade.edu',
                'first_name': 'John',
                'last_name': 'Smith',
                'bio': 'Professor of Computer Science with 15+ years of experience in web development and machine learning.'
            },
            {
                'username': 'dr_johnson',
                'email': 'johnson@convade.edu',
                'first_name': 'Emily',
                'last_name': 'Johnson',
                'bio': 'Data Science expert and author of several programming books.'
            },
            {
                'username': 'prof_chen',
                'email': 'chen@convade.edu',
                'first_name': 'David',
                'last_name': 'Chen',
                'bio': 'Software engineer turned educator, specializing in modern web technologies.'
            },
            {
                'username': 'dr_williams',
                'email': 'williams@convade.edu',
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'bio': 'UI/UX Design expert with extensive industry experience.'
            }
        ]

        instructors = []
        for data in instructors_data:
            instructor, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'teacher',
                    'bio': data['bio']
                }
            )
            instructors.append(instructor)
            if created:
                self.stdout.write(f'✓ Created instructor: {instructor.get_full_name()}')

        return instructors

    def create_categories(self):
        """Create course categories"""
        categories_data = [
            {'name': 'Web Development', 'description': 'Learn to build modern web applications'},
            {'name': 'Data Science', 'description': 'Analytics, machine learning, and data visualization'},
            {'name': 'Mobile Development', 'description': 'iOS and Android app development'},
            {'name': 'Design', 'description': 'UI/UX design and graphic design'},
            {'name': 'Programming', 'description': 'Programming languages and fundamentals'},
            {'name': 'DevOps', 'description': 'Deployment, automation, and infrastructure'},
        ]

        categories = []
        for data in categories_data:
            category, created = CourseCategory.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'✓ Created category: {category.name}')

        return categories

    def create_courses(self, instructors, categories):
        """Create dummy courses"""
        courses_data = [
            {
                'title': 'Complete Python Web Development with Django',
                'description': 'Master Django framework and build professional web applications. Learn models, views, templates, authentication, and deployment.',
                'difficulty': 'intermediate',
                'duration_hours': 40,
                'price': Decimal('99.99'),
                'categories': ['Web Development', 'Programming']
            },
            {
                'title': 'JavaScript Fundamentals for Beginners',
                'description': 'Learn JavaScript from scratch. Cover variables, functions, objects, DOM manipulation, and modern ES6+ features.',
                'difficulty': 'beginner',
                'duration_hours': 25,
                'price': Decimal('49.99'),
                'categories': ['Programming', 'Web Development']
            },
            {
                'title': 'Data Science with Python and Pandas',
                'description': 'Comprehensive guide to data analysis with Python. Learn pandas, matplotlib, seaborn, and basic machine learning.',
                'difficulty': 'intermediate',
                'duration_hours': 35,
                'price': Decimal('89.99'),
                'categories': ['Data Science', 'Programming']
            },
            {
                'title': 'React.js Complete Course',
                'description': 'Build modern web applications with React. Learn hooks, state management, routing, and best practices.',
                'difficulty': 'intermediate',
                'duration_hours': 30,
                'price': Decimal('79.99'),
                'categories': ['Web Development']
            },
            {
                'title': 'UI/UX Design Masterclass',
                'description': 'Learn user interface and user experience design principles. Create beautiful and functional designs.',
                'difficulty': 'beginner',
                'duration_hours': 20,
                'price': Decimal('69.99'),
                'categories': ['Design']
            },
            {
                'title': 'Machine Learning with Python',
                'description': 'Introduction to machine learning algorithms, scikit-learn, and practical applications.',
                'difficulty': 'advanced',
                'duration_hours': 45,
                'price': Decimal('129.99'),
                'categories': ['Data Science', 'Programming']
            },
            {
                'title': 'Mobile App Development with React Native',
                'description': 'Build cross-platform mobile apps using React Native. Deploy to both iOS and Android.',
                'difficulty': 'intermediate',
                'duration_hours': 38,
                'price': Decimal('109.99'),
                'categories': ['Mobile Development', 'Programming']
            },
            {
                'title': 'Docker and Kubernetes for Developers',
                'description': 'Learn containerization and orchestration. Master Docker, Kubernetes, and deployment strategies.',
                'difficulty': 'advanced',
                'duration_hours': 32,
                'price': Decimal('119.99'),
                'categories': ['DevOps']
            },
            {
                'title': 'HTML & CSS for Beginners',
                'description': 'Start your web development journey. Learn HTML5, CSS3, responsive design, and modern layout techniques.',
                'difficulty': 'beginner',
                'duration_hours': 18,
                'price': Decimal('29.99'),
                'categories': ['Web Development']
            },
            {
                'title': 'Advanced JavaScript and Node.js',
                'description': 'Deep dive into JavaScript concepts and server-side development with Node.js and Express.',
                'difficulty': 'advanced',
                'duration_hours': 42,
                'price': Decimal('99.99'),
                'categories': ['Programming', 'Web Development']
            }
        ]

        courses = []
        for i, data in enumerate(courses_data):
            course = Course.objects.create(
                title=data['title'],
                description=data['description'],
                instructor=instructors[i % len(instructors)],
                difficulty=data['difficulty'],
                duration_hours=data['duration_hours'],
                price=data['price'],
                is_published=True
            )
            
            # Add categories
            course_categories = [cat for cat in categories if cat.name in data['categories']]
            for category in course_categories:
                category.courses.add(course)
            
            courses.append(course)
            self.stdout.write(f'✓ Created course: {course.title} by {course.instructor.get_full_name()}')

        return courses

    def create_course_content(self, courses):
        """Create course content for each course"""
        content_templates = [
            {
                'title': 'Course Introduction',
                'content_type': 'video',
                'content': 'Welcome to the course! In this introduction video, we\'ll cover what you\'ll learn.',
                'is_free': True,
                'order': 1
            },
            {
                'title': 'Getting Started',
                'content_type': 'text',
                'content': 'In this lesson, we\'ll set up your development environment and install necessary tools.',
                'is_free': True,
                'order': 2
            },
            {
                'title': 'Basic Concepts',
                'content_type': 'video',
                'content': 'Understanding the fundamental concepts you need to know.',
                'is_free': False,
                'order': 3
            },
            {
                'title': 'Hands-on Practice',
                'content_type': 'assignment',
                'content': 'Complete these practice exercises to reinforce your learning.',
                'is_free': False,
                'order': 4
            },
            {
                'title': 'Knowledge Check',
                'content_type': 'quiz',
                'content': 'Test your understanding with this comprehensive quiz.',
                'is_free': False,
                'order': 5
            }
        ]

        for course in courses:
            for content_data in content_templates:
                CourseContent.objects.create(
                    course=course,
                    title=content_data['title'],
                    content_type=content_data['content_type'],
                    content=content_data['content'],
                    is_free=content_data['is_free'],
                    order=content_data['order']
                )
            
            self.stdout.write(f'✓ Added content to: {course.title}')

    def create_enrollments(self, courses):
        """Create some sample enrollments"""
        # Create some student users if they don't exist
        students_data = [
            {'username': 'student1', 'email': 'student1@convade.edu', 'first_name': 'Alice', 'last_name': 'Brown'},
            {'username': 'student2', 'email': 'student2@convade.edu', 'first_name': 'Bob', 'last_name': 'Davis'},
            {'username': 'student3', 'email': 'student3@convade.edu', 'first_name': 'Carol', 'last_name': 'Wilson'},
        ]

        students = []
        for data in students_data:
            student, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'student'
                }
            )
            students.append(student)

        # Create random enrollments
        enrollment_count = 0
        for student in students:
            # Each student enrolls in 2-4 random courses
            student_courses = random.sample(courses, random.randint(2, 4))
            for course in student_courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'progress': random.randint(0, 100),
                        'is_active': True
                    }
                )
                if created:
                    enrollment_count += 1

        self.stdout.write(f'✓ Created {enrollment_count} enrollments') 