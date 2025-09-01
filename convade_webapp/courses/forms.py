from django import forms
from .models import Course, CourseCategory

class CourseForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=CourseCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Course
        fields = ['title', 'description', 'difficulty', 'duration_hours', 'price', 'thumbnail', 'is_published', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe what students will learn in this course'
            }),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Course duration in hours'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01,
                'placeholder': 'Course price (0 for free)'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class CourseSearchForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    PRICE_CHOICES = [
        ('', 'Any Price'),
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]
    
    SORT_CHOICES = [
        ('newest', 'Newest'),
        ('popular', 'Most Popular'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search courses...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=CourseCategory.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    price = forms.ChoiceField(
        choices=PRICE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }


class EnrollmentForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], widget=forms.Select(attrs={'class': 'form-select'}))
    nationality = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    preferred_contact_method = forms.ChoiceField(choices=[('phone', 'Phone'), ('whatsapp', 'WhatsApp'), ('email', 'Email')], widget=forms.RadioSelect)

    highest_qualification = forms.ChoiceField(choices=[('secondary', 'Secondary School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('other', 'Other')], widget=forms.Select(attrs={'class': 'form-select'}))
    current_status = forms.ChoiceField(choices=[('student', 'Student'), ('graduate', 'Graduate'), ('professional', 'Working Professional'), ('entrepreneur', 'Entrepreneur')], widget=forms.Select(attrs={'class': 'form-select'}))
    field_of_study = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    course_of_interest = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    mode_of_learning = forms.ChoiceField(choices=[('online', 'Online Live Classes'), ('self_paced', 'Self-paced'), ('hybrid', 'Hybrid')], widget=forms.Select(attrs={'class': 'form-select'}))
    preferred_start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    motivation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    career_aspiration = forms.ChoiceField(choices=[('tech_career', 'Tech Career'), ('startup', 'Start-up'), ('freelancing', 'Freelancing'), ('job_readiness', 'Job Readiness')], widget=forms.Select(attrs={'class': 'form-select'}))

    sponsorship = forms.ChoiceField(choices=[('self', 'Self'), ('parent', 'Parent'), ('employer', 'Employer'), ('scholarship', 'Scholarship')], widget=forms.Select(attrs={'class': 'form-select'}))
    payment_plan = forms.ChoiceField(choices=[('full', 'Full'), ('installment', 'Installment'), ('subscription', 'Subscription')], widget=forms.Select(attrs={'class': 'form-select'}))

    has_laptop = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_internet = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    emergency_contact_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_contact_relationship = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_contact_phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    agree_terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    agree_attendance = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    agree_privacy = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    passport_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    id_card = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        course_title = kwargs.pop('course_title', None)
        super().__init__(*args, **kwargs)
        if course_title:
            self.fields['course_of_interest'].initial = course_title
        self.fields['course_of_interest'].widget.attrs['readonly'] = True
