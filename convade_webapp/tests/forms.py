from django import forms
from django.forms import inlineformset_factory
from .models import Test, Question, AnswerChoice
from courses.models import Course

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            'title', 'description', 'course', 'test_type', 
            'duration_minutes', 'max_attempts', 'passing_score',
            'start_time', 'end_time', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter test title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what this test covers...'
            }),
            'course': forms.Select(attrs={
                'class': 'form-select'
            }),
            'test_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '300'
            }),
            'max_attempts': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            'passing_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_teacher:
            # Filter courses to only show courses taught by this teacher
            self.fields['course'].queryset = Course.objects.filter(
                instructor=user,
                is_published=True
            )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'points', 'explanation']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your question...'
            }),
            'question_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'value': '1'
            }),
            'explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional: Explain the correct answer...'
            })
        }

class AnswerChoiceForm(forms.ModelForm):
    class Meta:
        model = AnswerChoice
        fields = ['choice_text', 'is_correct']
        widgets = {
            'choice_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter answer choice...'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

# Formsets for handling multiple questions and answers
QuestionFormSet = inlineformset_factory(
    Test, 
    Question, 
    form=QuestionForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

AnswerChoiceFormSet = inlineformset_factory(
    Question,
    AnswerChoice,
    form=AnswerChoiceForm,
    extra=2,
    can_delete=True,
    min_num=2,
    validate_min=True
) 