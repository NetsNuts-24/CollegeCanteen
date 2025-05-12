from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import CanteenStatus




def index(request):
    canteen_status = CanteenStatus.objects.first()  # Assuming only one record exists
    return render(request, 'account/index.html', {'canteen_status': canteen_status})

from account.models import Profile  # Make sure this import is at the top

# REGISTER
def inregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if User.objects.filter(username=phone).exists():
            messages.error(request, 'User already exists')
            return render(request, 'account/inregister.html')

        user = User.objects.create_user(
            username=phone,
            first_name=name,
            password=password
        )

        # ✅ Create Profile with mobile number
        profile, created = Profile.objects.get_or_create(user=user)
        profile.mobile = phone
        profile.save()


        login(request, user)
        return redirect('cart:menu_view')  # Redirect after successful registration

    return render(request, 'account/inregister.html')

# LOGIN
from account.models import Profile  # Ensure this is at the top

def login_attempt(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(username=phone, password=password)

        if user is not None:
            # ✅ Ensure Profile exists before accessing it anywhere else
            Profile.objects.get_or_create(user=user)

            login(request, user)
            return redirect('cart:menu_view')
        else:
            messages.error(request, 'Invalid phone or password')
            return render(request, 'account/login.html')

    return render(request, 'account/login.html')



# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('account:login_attempt')


# FORGOT PASSWORD (basic version)
def forgot_password(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        try:
            user = User.objects.get(username=phone)
            request.session['reset_user'] = user.username
            return redirect('account:reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Phone number not found')
            return render(request, 'account/forgot_password.html')

    return render(request, 'account/forgot_password.html')


# RESET PASSWORDfrom django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# RESET PASSWORD
def reset_password(request):
    phone = request.session.get('reset_user')
    if not phone:
        return redirect('account:forgot_password')

    if request.method == 'POST':
        password = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'account/reset_password.html')

        try:
            user = User.objects.get(username=phone)
            user.set_password(password)
            user.save()
            del request.session['reset_user']
            messages.success(request, 'Password reset successful')
            return redirect('account:login_attempt')
        except User.DoesNotExist:
            messages.error(request, 'Something went wrong')
            return redirect('account:forgot_password')

    return render(request, 'account/reset_password.html')



