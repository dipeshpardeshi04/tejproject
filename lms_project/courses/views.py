from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from .models import Course, Enrollment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'courses/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'courses/login.html')

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'courses/dashboard.html', {'enrollments': enrollments})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def enrol(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.create(user=request.user, course=course)
    return redirect('course_detail', course_id=course.id)

def search(request):
    query = request.GET.get('q')
    courses = Course.objects.filter(title__icontains=query)
    return render(request, 'courses/search_results.html', {'courses': courses})
def home(request):
    return render(request, 'home.html')