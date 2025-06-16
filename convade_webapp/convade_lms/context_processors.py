from django.urls import resolve

def navigation_context(request):
    """
    Context processor to determine active navigation item
    """
    try:
        # Get the current URL name and namespace
        current_url = resolve(request.path_info)
        url_name = current_url.url_name
        namespace = current_url.namespace
        
        # Initialize all nav items as inactive
        nav_context = {
            'nav_home_active': False,
            'nav_courses_active': False,
            'nav_my_courses_active': False,
            'nav_badges_active': False,
            'nav_certificates_active': False,
            'nav_dashboard_active': False,
            'nav_profile_active': False,
            'nav_create_course_active': False,
            'nav_create_test_active': False,
            'nav_analytics_active': False,
            'nav_admin_active': False,
            'nav_login_active': False,
            'nav_signup_active': False,
        }
        
        # Determine active navigation based on URL
        if url_name == 'home':
            nav_context['nav_home_active'] = True
        elif namespace == 'courses':
            if url_name in ['list', 'detail']:
                nav_context['nav_courses_active'] = True
            elif url_name == 'my_courses':
                nav_context['nav_my_courses_active'] = True
            elif url_name == 'create':
                nav_context['nav_create_course_active'] = True
        elif namespace == 'badges' and url_name == 'my_badges':
            nav_context['nav_badges_active'] = True
        elif namespace == 'certifications' and url_name == 'my_certificates':
            nav_context['nav_certificates_active'] = True
        elif namespace == 'accounts':
            if url_name == 'dashboard':
                nav_context['nav_dashboard_active'] = True
            elif url_name == 'profile':
                nav_context['nav_profile_active'] = True
        elif namespace == 'tests' and url_name == 'create':
            nav_context['nav_create_test_active'] = True
        elif namespace == 'analytics' and url_name == 'dashboard':
            nav_context['nav_analytics_active'] = True
        elif url_name == 'account_login':
            nav_context['nav_login_active'] = True
        elif url_name == 'account_signup':
            nav_context['nav_signup_active'] = True
        elif request.path_info.startswith('/admin/'):
            nav_context['nav_admin_active'] = True
            
        return nav_context
        
    except Exception:
        # If there's any error resolving URL, return all inactive
        return {
            'nav_home_active': False,
            'nav_courses_active': False,
            'nav_my_courses_active': False,
            'nav_badges_active': False,
            'nav_certificates_active': False,
            'nav_dashboard_active': False,
            'nav_profile_active': False,
            'nav_create_course_active': False,
            'nav_create_test_active': False,
            'nav_analytics_active': False,
            'nav_admin_active': False,
            'nav_login_active': False,
            'nav_signup_active': False,
        } 