from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    """
    View for handling user login.

    If the request method is POST, attempts to authenticate the user using
    provided credentials. If successful, logs in the user and redirects to
    the dashboard. Otherwise, displays an error message.

    If the request method is not POST, renders the login page.

    Args:
    - `request`: The HTTP request object.

    Returns:
    - If the method is POST and login is successful, redirects to the dashboard.
    - If the method is POST and login fails, renders the login page with an error message.
    - If the method is not POST, renders the login page.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Logged in successfully. Welcome, {user.username}!')
            # Redirect to a desired page after login
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')


def dashboard_view(request):
    """
    View for displaying the user dashboard.

    If the user is not authenticated, redirects to the login page.

    Retrieves the user type and renders the dashboard page.

    Args:
    - `request`: The HTTP request object.

    Returns:
    - If the user is authenticated, renders the dashboard page.
    - If the user is not authenticated, redirects to the login page.
    """
    if not request.user:
        return redirect('login')

    user_type = request.user.type.name if hasattr(request.user, 'type') else None
    return render(request, 'dashboard.html', {'user_type': user_type})
