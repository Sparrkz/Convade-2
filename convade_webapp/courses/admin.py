from django.contrib import admin
from .models import Course, CourseContent, Enrollment, CourseCategory

class CourseContentInline(admin.TabularInline):
    model = CourseContent
    extra = 0
    fields = ['title', 'content_type', 'order', 'is_free']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'difficulty', 'price', 'is_published', 'created_at']
    list_filter = ['difficulty', 'is_published', 'created_at', 'instructor']
    search_fields = ['title', 'description', 'instructor__username']
    ordering = ['-created_at']
    inlines = [CourseContentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor', 'thumbnail')
        }),
        ('Course Details', {
            'fields': ('difficulty', 'duration_hours', 'price', 'is_published')
        }),
    )

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'order', 'is_free']
    list_filter = ['content_type', 'is_free', 'course']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'progress', 'is_active']
    list_filter = ['is_active', 'enrolled_at', 'course']
    search_fields = ['student__username', 'course__title']
    ordering = ['-enrolled_at']

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    filter_horizontal = ['courses']
