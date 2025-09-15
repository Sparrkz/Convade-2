from django import forms
from .models import Course, CourseCategory, EnrollmentApplication

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


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = EnrollmentApplication
        exclude = ['student', 'course', 'status', 'created_at']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'preferred_contact_method': forms.RadioSelect,
            'highest_qualification': forms.Select(attrs={'class': 'form-select'}),
            'current_status': forms.Select(attrs={'class': 'form-select'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_of_learning': forms.Select(attrs={'class': 'form-select'}),
            'preferred_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'career_aspiration': forms.Select(attrs={'class': 'form-select'}),
            'sponsorship': forms.Select(attrs={'class': 'form-select'}),
            'payment_plan': forms.Select(attrs={'class': 'form-select'}),
            'has_laptop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_internet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'agree_terms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'agree_attendance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'agree_privacy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'id_card': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.pop('course_title', None)  # No longer needed
        super().__init__(*args, **kwargs)
        self.fields['agree_terms'].required = True
        self.fields['agree_attendance'].required = True
        self.fields['agree_privacy'].required = True
