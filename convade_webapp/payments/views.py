import uuid, requests
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from courses.models import Course
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def initialize_payment(request):
    course_id = request.GET.get('course_id') or request.POST.get('course_id')
    amount = 5000  # Default amount
    course = None
    if course_id:
        try:
            course = Course.objects.get(pk=course_id)
            amount = float(course.price)
        except Course.DoesNotExist:
            pass
    tx_ref = str(uuid.uuid4())

    payment = Payment.objects.create(
        user=request.user,
        tx_ref=tx_ref,
        amount=amount,
        status="pending"
    )

    headers = {
        "Authorization": f"Bearer {getattr(settings, 'FLW_SECRET_KEY', '')}",
        "Content-Type": "application/json"
    }

    data = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": "NGN",
        "redirect_url": f"http://127.0.0.1:8000/payments/callback/?course_id={course.pk if course else ''}",
        "payment_options": "card,banktransfer",
        "customer": {
            "email": request.user.email,
            "name": request.user.username,
        },
        "customizations": {
            "title": course.title if course else "My Django Store",
            "description": f"Payment for {course.title}" if course else "Payment for course",
            "logo": "https://convade.org/static/images/ico.svg"
        }
    }

    response = requests.post(
        "https://api.flutterwave.com/v3/payments",
        headers=headers,
        json=data
    )

    res_data = response.json()

    if res_data.get("status") == "success":
        return redirect(res_data["data"]["link"])
    else:
        # Print/log the error for debugging
        print("Flutterwave error:", res_data)
        # Show the error to the user
        return JsonResponse({
            "error": res_data.get("message", "Payment initialization failed."),
            "details": res_data
        }, status=400)


@csrf_exempt
def payment_callback(request):
    tx_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")
    status = request.GET.get("status")
    course_id = request.GET.get("course_id")

    print("CALLBACK DATA:", request.GET)

    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}"
    }

    # If Flutterwave didn't send transaction_id, fetch it using tx_ref
    if not transaction_id:
        lookup_url = f"https://api.flutterwave.com/v3/transactions?tx_ref={tx_ref}"
        lookup_res = requests.get(lookup_url, headers=headers).json()
        print("LOOKUP RESPONSE:", lookup_res)
        if lookup_res.get("status") == "success" and lookup_res["data"]:
            transaction_id = lookup_res["data"][0]["id"]

    # Verify payment
    verify_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    response = requests.get(verify_url, headers=headers)
    res_data = response.json()
    print("VERIFY RESPONSE:", res_data)

    try:
        payment_status = res_data["data"]["status"]
    except KeyError:
        payment_status = None

    if payment_status == "successful":
        # Unlock course for user
        if course_id:
            try:
                from courses.models import Course, Enrollment
                course = Course.objects.get(pk=course_id)
                enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
                enrollment.is_active = True
                enrollment.save()
                # Optionally update Payment record
                Payment.objects.filter(tx_ref=tx_ref).update(status="successful")
                # Redirect to course content page
                return redirect('courses:content', pk=course.pk)
            except Exception as e:
                print("Error unlocking course:", e)
                return redirect('/')
        else:
            return redirect('/')
    else:
        # Payment failed, redirect to a generic error page or home
        return redirect('/')
