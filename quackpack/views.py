from django.shortcuts import render, redirect
from quackpack import models
from .models import CustomUser, students, wardens, req
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request,'home.html')

def loginUser(request):
    if request.method=='POST':
        return render(request, 'login_page.html')
    else:
        return render(request, 'login_page.html')
    
def doLogin(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not (email and password):
            messages.error(request, "Please provide all the details!!")
            return render(request, 'login_page.html')

        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                # Password is correct, proceed with login or other logic
                print("login")
            else:
                # Password is incorrect
                print("no")
        except CustomUser.DoesNotExist:
            #user does not exist
            pass

        
        if user is not None:
            # Password is correct, log the user in and redirect to the home page
            login(request, user)
            if user.user_type == CustomUser.STUDENT:
                print("Student user logged in")
                return redirect('student_main')
            elif user.user_type == CustomUser.WARDEN:
                print("Warden user logged in")
                return redirect('warden_main')
            else:
                print("Unknown user type")
                return redirect('home')
            
        else:
            print('test')
            messages.error(request, 'Invalid Login Credentials!!')
            return render(request, 'login_page.html')

    else:
        return render(request, 'login_page.html')

def registration(request):
    return render(request,'registration.html')

def doRegistration(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['confirm_password'] 

        if not (email and password and pass2):
            messages.error(request, 'Please provide all the details!')
            return render(request, 'registration.html')
        
        if password != pass2:
            messages.error(request, 'Both passwords should match!')
            return render(request, 'registration.html')
        
        is_user_exists = CustomUser.objects.filter(email=email).exists()
        if is_user_exists:
            messages.error(request, 'User with this email already exists. Please proceed to login!')
            return render(request, 'registration.html')
        
        user_type = get_user_type_from_email(email)  # Determine user type based on email
        
        if user_type is None:
            messages.error(request, "Please use a valid format for the email id: '<username>@vitstudent.ac.in' or '<username>@vit.ac.in")
            return render(request, 'registration.html')
        
        # Temporarily store email and user_type in session
        request.session['email'] = email
        request.session['user_type'] = user_type
        request.session['password'] = password
        
        # Redirect to appropriate form based on user type
        if user_type == CustomUser.STUDENT:
            return redirect('student_registration')
        elif user_type == CustomUser.WARDEN:
            return redirect('warden_registration')

    return render(request, 'registration.html')

def studentregistration(request):
    return render(request,'student_registration.html')
def wardenregistration(request):
    return render(request,'warden_registration.html')

def dostudentregistration(request):
    if request.method == 'POST':
        email = request.session.get('email')
        user_type = request.session.get('user_type')

        if not email or user_type != CustomUser.STUDENT:
            messages.error(request, 'Session expired or invalid access. Please register again.')
            return redirect('do_registration')
        
        name = request.POST['name']
        regno = request.POST['registration_number']
        mob = request.POST['mobile']
        gender = request.POST['gender']
        block = request.POST['block']


        # Create the CustomUser instance
        user = CustomUser.objects.create_user(username=email.split('@')[0].split('.')[0], email=email, password=request.session['password'])
        user.user_type = user_type
        user.save()

        # Create the Student instance
        student = students(name=name, regno=regno, mob=mob, gender=gender,block=block, email=user)
        student.save()

        messages.success(request, 'Student account created successfully. You can now log in.')
        return render(request, 'login_page.html')

    return render(request, 'student_registration.html')

def dowardenregistration(request):
    if request.method == 'POST':
        email = request.session.get('email')
        user_type = request.session.get('user_type')

        if not email or user_type != CustomUser.WARDEN:
            messages.error(request, 'Session expired or invalid access. Please register again.')
            return redirect('do_registration')
        hostel = request.POST['hostel']
        block = request.POST['block']

        # Create the CustomUser instance
        user = CustomUser.objects.create_user(username=email.split('@')[0].split('.')[0], email=email, password=request.session['password'])
        user.user_type = user_type
        user.save()

        # Create the Warden instance
        wardens.objects.create(email=user, block=block, hostel=hostel)

        messages.success(request, 'Warden account created successfully. You can now log in.')
        return render(request, 'login_page.html')

    return render(request, 'warden_registration.html')

def get_user_type_from_email(email):
    if '@vitstudent.ac.in' in email:
        return CustomUser.STUDENT
    elif email.endswith('@vit.ac.in'):
        return CustomUser.WARDEN
    else:
        return None
    
def main1(request):
    return render(request,'main1.html')

def main2(request):
    return render(request,'main2.html')

def request_page(request):
    return render(request,'request_page.html')

def deliver_page(request):
    return render(request,'deliver_page.html')

def create_request(request):
    student = students.objects.get(regno=request.user)  
    if request.method == "POST":
        date = request.POST['date']
        pickup_location = request.POST['pickup_location']
        drop_location = request.POST['drop_location']
        time = request.POST['time']

        # Create the request
        req_obj = req.objects.create(
            requester=request.user,
            regno=student.regno,
            date=date,
            pickup_location=pickup_location,
            drop_location=drop_location,
            time=time
        )
        req_obj.save()

        return redirect('deliver_page')

    return render(request, 'request_page.html', {'regno': student.regno})

def deliver(request):
    available_requests = req.objects.filter(status="Pending").exclude(requester=request.user)
    accepted_requests = req.objects.filter(status="Accepted", accepted_by=request.user)
    
    if request.method == "POST":
        request_id = request.POST['request_id']
        req_obj = req.objects.get(id=request_id)
        req_obj.accepted_by = request.user
        req_obj.status = "Accepted"
        req_obj.save()

        return redirect('deliver')

    return render(request, 'deliver_page.html', {
        'pending_requests': available_requests,
        'accepted_requests': accepted_requests,
    })
