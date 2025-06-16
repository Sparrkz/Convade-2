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