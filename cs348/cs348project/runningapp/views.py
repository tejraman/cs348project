from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Run, BikeRide, Swim, Leaderboard, ProgressReport
from .forms import RunForm, BikeRideForm, SwimForm, RegistrationForm, ProgressReportForm
from django.utils.dateparse import parse_date
from django.db import connection
from django.db.models import Sum, Count, F
from django.db.models.functions import Extract
from django.db.models.functions import Coalesce  
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import FloatField


class CustomLoginView(LoginView):
    template_name = 'runningapp/login.html'

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'
    next_page = 'login'  # or whatever URL you want to redirect to after logout

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'runningapp/register.html', {'form': form})

@login_required
def home(request):
    user = request.user

    # Retrieve filter parameters
    run_distance = request.GET.get("run_distance", "")
    run_start_date = request.GET.get("run_start_date", "")
    run_end_date = request.GET.get("run_end_date", "")
    run_time = request.GET.get("run_time", "")

    # Filter Runs based on parameters
    runs = Run.objects.filter(user=user)
    if run_distance:
        runs = runs.filter(distance_miles__gte=float(run_distance))
    if run_start_date:
        runs = runs.filter(date__gte=parse_date(run_start_date))
    if run_end_date:
        runs = runs.filter(date__lte=parse_date(run_end_date))
    if run_time:
        runs = runs.filter(time_minutes__lte=float(run_time))

    # Similar filtering for Bike Rides and Swims
    bike_distance = request.GET.get("bike_distance", "")
    bike_start_date = request.GET.get("bike_start_date", "")
    bike_end_date = request.GET.get("bike_end_date", "")
    bike_time = request.GET.get("bike_time", "")

    bike_rides = BikeRide.objects.filter(user=user)
    if bike_distance:
        bike_rides = bike_rides.filter(distance_miles__gte=float(bike_distance))
    if bike_start_date:
        bike_rides = bike_rides.filter(date__gte=parse_date(bike_start_date))
    if bike_end_date:
        bike_rides = bike_rides.filter(date__lte=parse_date(bike_end_date))
    if bike_time:
        bike_rides = bike_rides.filter(time_minutes__lte=float(bike_time))

    swim_distance = request.GET.get("swim_distance", "")
    swim_start_date = request.GET.get("swim_start_date", "")
    swim_end_date = request.GET.get("swim_end_date", "")
    swim_time = request.GET.get("swim_time", "")

    swims = Swim.objects.filter(user=user)
    if swim_distance:
        swims = swims.filter(distance_meters__gte=float(swim_distance))
    if swim_start_date:
        swims = swims.filter(date__gte=parse_date(swim_start_date))
    if swim_end_date:
        swims = swims.filter(date__lte=parse_date(swim_end_date))
    if swim_time:
        swims = swims.filter(time_minutes__lte=float(swim_time))

    # Pass filter values back to the template
    context = {
        'runs': runs,
        'bike_rides': bike_rides,
        'swims': swims,
        'run_distance': run_distance,
        'run_start_date': run_start_date,
        'run_end_date': run_end_date,
        'run_time': run_time,
        'bike_distance': bike_distance,
        'bike_start_date': bike_start_date,
        'bike_end_date': bike_end_date,
        'bike_time': bike_time,
        'swim_distance': swim_distance,
        'swim_start_date': swim_start_date,
        'swim_end_date': swim_end_date,
        'swim_time': swim_time,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'runningapp/home.html', context)

@login_required
def add_run(request):
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            run = form.save(commit=False)
            run.user = request.user
            run.save()
            return redirect('home')
    else:
        form = RunForm()
    return render(request, 'runningapp/add_run.html', {'form': form})

@login_required
def edit_run(request, run_id):
    run = get_object_or_404(Run, id=run_id, user=request.user)
    if request.method == 'POST':
        form = RunForm(request.POST, instance=run)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RunForm(instance=run)
    return render(request, 'runningapp/edit_run.html', {'form': form})

@login_required
def delete_run(request, run_id):
    run = get_object_or_404(Run, id=run_id, user=request.user)
    if request.method == 'POST':
        run.delete()
        return redirect('home')
    return render(request, 'runningapp/delete_run.html', {'run': run})

@login_required
def add_swim(request):
    if request.method == 'POST':
        form = SwimForm(request.POST)
        if form.is_valid():
            swim = form.save(commit=False)
            swim.user = request.user
            swim.save()
            return redirect('home')
    else:
        form = SwimForm()
    return render(request, 'runningapp/add_swim.html', {'form': form})

@login_required
def edit_swim(request, swim_id):
    swim = get_object_or_404(Swim, id=swim_id, user=request.user)
    if request.method == 'POST':
        form = SwimForm(request.POST, instance=swim)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SwimForm(instance=swim)
    return render(request, 'runningapp/edit_swim.html', {'form': form})

@login_required
def delete_swim(request, swim_id):
    swim = get_object_or_404(Swim, id=swim_id, user=request.user)
    if request.method == 'POST':
        swim.delete()
        return redirect('home')
    return render(request, 'runningapp/delete_swim.html', {'swim': swim})

@login_required
def add_bike(request):
    if request.method == 'POST':
        form = BikeRideForm(request.POST)
        if form.is_valid():
            bike = form.save(commit=False)
            bike.user = request.user
            bike.save()
            return redirect('home')
    else:
        form = BikeRideForm()
    return render(request, 'runningapp/add_bike.html', {'form': form})

@login_required
def edit_bike(request, bike_id):
    bike = get_object_or_404(BikeRide, id=bike_id, user=request.user)
    if request.method == 'POST':
        form = BikeRideForm(request.POST, instance=bike)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BikeRideForm(instance=bike)
    return render(request, 'runningapp/edit_bike.html', {'form': form})

@login_required
def delete_bike(request, bike_id):
    bike = get_object_or_404(BikeRide, id=bike_id, user=request.user)
    if request.method == 'POST':
        bike.delete()
        return redirect('home')
    return render(request, 'runningapp/delete_bike.html', {'bike': bike})



@login_required
def leaderboard(request):
    filter_by = request.GET.get('filter_by', 'distance')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    with connection.cursor() as cursor:
        if filter_by == 'distance':
            cursor.execute("""
                SELECT 
                    u.username,
                    COALESCE(run.total_distance, 0) +
                    COALESCE(bike.total_distance, 0) +
                    COALESCE(swim.total_distance, 0) AS total_distance
                FROM runningapp_user u
                LEFT JOIN (
                    SELECT user_id, SUM(distance_miles) AS total_distance
                    FROM runningapp_run
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) run ON u.id = run.user_id
                LEFT JOIN (
                    SELECT user_id, SUM(distance_miles) AS total_distance
                    FROM runningapp_bikeride
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) bike ON u.id = bike.user_id
                LEFT JOIN (
                    SELECT user_id, SUM(distance_miles) AS total_distance
                    FROM runningapp_swim
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) swim ON u.id = swim.user_id
                ORDER BY total_distance DESC
            """, [start_date, end_date, start_date, end_date, start_date, end_date])
        elif filter_by == 'time':
            cursor.execute("""
                SELECT 
                    u.username,
                    COALESCE(run.total_time, 0) +
                    COALESCE(bike.total_time, 0) +
                    COALESCE(swim.total_time, 0) AS total_time
                FROM runningapp_user u
                LEFT JOIN (
                    SELECT user_id, SUM(time_minutes) AS total_time
                    FROM runningapp_run
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) run ON u.id = run.user_id
                LEFT JOIN (
                    SELECT user_id, SUM(time_minutes) AS total_time
                    FROM runningapp_bikeride
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) bike ON u.id = bike.user_id
                LEFT JOIN (
                    SELECT user_id, SUM(time_minutes) AS total_time
                    FROM runningapp_swim
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) swim ON u.id = swim.user_id
                ORDER BY total_time DESC
            """, [start_date, end_date, start_date, end_date, start_date, end_date])
        else:  # Filter by total activities
            cursor.execute("""
                SELECT 
                    u.username,
                    COALESCE(run.total_activities, 0) +
                    COALESCE(bike.total_activities, 0) +
                    COALESCE(swim.total_activities, 0) AS total_activities
                FROM runningapp_user u
                LEFT JOIN (
                    SELECT user_id, COUNT(id) AS total_activities
                    FROM runningapp_run
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) run ON u.id = run.user_id
                LEFT JOIN (
                    SELECT user_id, COUNT(id) AS total_activities
                    FROM runningapp_bikeride
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) bike ON u.id = bike.user_id
                LEFT JOIN (
                    SELECT user_id, COUNT(id) AS total_activities
                    FROM runningapp_swim
                    WHERE date BETWEEN COALESCE(%s, date) AND COALESCE(%s, date)
                    GROUP BY user_id
                ) swim ON u.id = swim.user_id
                ORDER BY total_activities DESC
            """, [start_date, end_date, start_date, end_date, start_date, end_date])

        rows = cursor.fetchall()
        leaderboard_data = [(index + 1, row[0], row[1]) for index, row in enumerate(rows)]

    context = {
        'leaderboard': leaderboard_data,
        'start_date': start_date,
        'end_date': end_date,
        'filter_by': filter_by,
    }
    return render(request, 'runningapp/leaderboard.html', context)

@login_required
def add_progress(request):
    if request.method == 'POST':
        form = ProgressReportForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            return redirect('home')
    else:
        form = ProgressReportForm()
    return render(request, 'runningapp/add_progress.html', {'form': form})

@login_required
def view_progress_reports(request):
    progress_reports = ProgressReport.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'runningapp/view_progress.html', {'progress_reports': progress_reports})







