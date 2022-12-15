from django import http
from django.contrib import auth
from django.db.models.query import RawQuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, UsernameField
from Registration.models import registrants, centers, statuses, time_slots, vaccination_status, vacancies
import datetime
from django.urls import resolve


def reset_tables():
    vacancies.objects.all().update(empty_slots=5)
    centers.objects.filter(
        no_of_covaxin__isnull=False).update(no_of_covaxin=100)
    centers.objects.filter(
        no_of_covishield__isnull=False).update(no_of_covishield=100)
    centers.objects.filter(
        no_of_sputnik__isnull=False).update(no_of_sputnik=100)

# Create your views here.


def home(request):
    date_today = datetime.datetime.now().strftime('%Y-%m-%d')
    today_1 = vaccination_status.objects.filter(
        date_of_1st_dose=date_today).count()
    today_2 = vaccination_status.objects.filter(
        date_of_2nd_dose=date_today).count()
    today = today_1 + today_2
    total_1 = vaccination_status.objects.filter(
        booking_status_id=2).count()
    total_2 = vaccination_status.objects.filter(
        booking_status_id=3).count()
    total = total_1 + (2 * total_2)
    return render(request, 'index.html', {"total": total, "today": today})


def vaccines(request):
    return render(request, 'vaccines.html')


def centres(request):
    if request.method == "POST":
        query_city = request.POST.get('city')
        list_of_centers = list(centers.objects.filter(
            city=query_city).values_list('center_name', flat=True))
        center_stats = []
        for center in list_of_centers:
            center_stats.append([center])
            stat = []
            if centers.objects.filter(center_name=center).filter(no_of_covaxin__isnull=True).all().first() is not None:
                stat.append("no")
            else:
                stat.append("yes")
            if centers.objects.filter(center_name=center).filter(no_of_covishield__isnull=True).all().first() is not None:
                stat.append("no")
            else:
                stat.append("yes")
            if centers.objects.filter(center_name=center).filter(no_of_sputnik__isnull=True).all().first() is not None:
                stat.append("no")
            else:
                stat.append("yes")
            center_stats[len(center_stats)-1] += (stat)
        
        return render(request, 'centres.html', {'centers': center_stats})
    else:
        pass
    return render(request, 'centres.html')


def read_more(request):
    return render(request, 'readmore.html')


def about_us(request):
    return render(request, 'aboutus.html')


def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'signup.html', {'error': 'Username is already taken!'})
        except User.DoesNotExist:
            if(registrants.objects.filter(email=request.POST['email']).count() != 0):
                return render(request, 'signup.html', {'error': 'This Email ID already exists!'})
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name')
            email = request.POST.get('email')
            dob = request.POST.get('dob')
            city = request.POST.get('city')
            gender = request.POST.get('gender')
            vaccine = request.POST.get('vaccine')

            registrants.objects.create(username=username, password=password,
                                       email=email, name=name, date_of_birth=dob, city=city, gender=gender)
            user = User.objects.create_user(
                request.POST['username'], password=request.POST['password'])
            auth.login(request, user)
            id = registrants.objects.filter(
                username=username).values_list('registrant_id').first()[0]
            print(id)
            new_entry = vaccination_status(
                registrant_id_id=id, vaccine_name=vaccine, booking_status_id=1)
            new_entry.save()
            return redirect('/loggedin/1/')

    return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            username=request.POST.get('username'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            return redirect('/loggedin/1')

        else:
            messages.error(request, "Incorrect Username or Password!")
            return render(request, 'signin.html')
    return render(request, 'signin.html')


def signout(request):
    auth.logout(request)
    return redirect("/")


def loggedin_1(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        center = request.POST.get('center_name')
        return redirect(f'/loggedin/2/?center={center}')
    user = request.user
    name = user.username
    registrant_id = registrants.objects.filter(
        username=name).values_list('registrant_id').first()[0]
    vaccine = vaccination_status.objects.filter(
        registrant_id_id=registrant_id).values_list('vaccine_name').first()[0]
    status = vaccination_status.objects.filter(
        registrant_id_id=registrant_id).values_list('booking_status_id').first()[0]
    city = registrants.objects.filter(
        username=name).values_list('city').first()[0]
    if vaccine == 'Covaxin':
        list_of_centers = centers.objects.filter(
            city=city).filter(no_of_covaxin__isnull=False).filter(no_of_covaxin__gt=0).values_list('center_name')
    elif vaccine == 'Covishield':
        list_of_centers = centers.objects.filter(
            city=city).filter(no_of_covishield__isnull=False).filter(no_of_covishield__gt=0).values_list('center_name')
    else:
        list_of_centers = centers.objects.filter(
            city=city).filter(no_of_sputnik__isnull=False).filter(no_of_sputnik__gt=0).values_list('center_name')
    list_of_centers = [list_of_centers[i][0]
                       for i in range(len(list_of_centers))]
    return render(request, 'logged-in-1.html', {'name': name, 'vaccine': vaccine, 'registrant_id': registrant_id, 'date': (datetime.datetime.now()+datetime.timedelta(1)).strftime('%d-%m-%Y'), 'status': status, 'centers': list_of_centers})


def loggedin_2(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        user = request.user
        name = user.username
        current_url = request.get_full_path()
        center = (str(current_url).split("?"))[1]
        center = (center.split("="))[1]
        id = centers.objects.filter(
            center_name=center).values_list('center_id').first()[0]
        registrant_id = registrants.objects.filter(
            username=name).values_list('registrant_id').first()[0]
        vaccine = vaccination_status.objects.filter(
            registrant_id_id=registrant_id).values_list('vaccine_name').first()[0]
        status = vaccination_status.objects.filter(
            registrant_id_id=registrant_id).values_list('booking_status_id').first()[0]

        if 'book_1' in request.POST or 'book_2' in request.POST or 'book_3' in request.POST or 'book_4' in request.POST:
            if status == 3:
                messages.error(request, "You have already booked two slots!")
                return redirect(f'/loggedin/2/?center={center}')
            if status == 2:
                date_1 = str(vaccination_status.objects.filter(
                    registrant_id_id=registrant_id).values_list('date_of_1st_dose').first()[0])
                date_2 = str((datetime.datetime.now() +
                             datetime.timedelta(1)).strftime('%Y-%m-%d'))
                start = datetime.datetime.strptime(date_1, '%Y-%m-%d')
                end = datetime.datetime.strptime(date_2, '%Y-%m-%d')
                diff = (end.date() - start.date()).days
                print(diff)
                if diff < 60:
                    current_date_temp = datetime.datetime.strptime(
                        date_1, "%Y-%m-%d")
                    newdate = (current_date_temp +
                               datetime.timedelta(days=60)).strftime('%d/%m/%Y')
                    print(current_date_temp)
                    print(newdate)
                    messages.error(
                        request, f"There should be 2 months gap between both the doses. Please book the slot after {newdate}.")
                    return redirect(f'/loggedin/2/?center={center}')
            center_status = centers.objects.get(center_id=id)
            if vaccine == "Covishield":
                center_status.no_of_covishield = center_status.no_of_covishield - 1
            elif vaccine == "Covaxin":
                center_status.no_of_covaxin = center_status.no_of_covaxin - 1
            else:
                center_status.no_of_sputnik = center_status.no_of_sputnik - 1
            center_status.save()
            user_status = vaccination_status.objects.get(
                registrant_id_id=registrant_id)
            if status == 1:
                user_status.date_of_1st_dose = (
                    datetime.datetime.now()+datetime.timedelta(1)).strftime('%Y-%m-%d')
                user_status.center_1_id = id
                user_status.booking_status_id = user_status.booking_status_id + 1
            elif status == 2:
                user_status.date_of_2nd_dose = (
                    datetime.datetime.now()+datetime.timedelta(1)).strftime('%Y-%m-%d')
                user_status.center_2_id = id
                user_status.booking_status_id = user_status.booking_status_id + 1
            user_status.save()

        if 'book_1' in request.POST:
            time_slot = "08:00:00.000000"
            center_slot = vacancies.objects.filter(
                center_id=id).get(slot_no_id=1)
            center_slot.empty_slots = center_slot.empty_slots - 1
            center_slot.save()
            return redirect(f'/loggedin/3/?center={center}')
        if 'book_2' in request.POST:
            time_slot = "10:00:00.000000"
            center_slot = vacancies.objects.filter(
                center_id=id).get(slot_no_id=2)
            center_slot.empty_slots = center_slot.empty_slots - 1
            center_slot.save()
            return redirect(f'/loggedin/3/?center={center}')
        if 'book_3' in request.POST:
            time_slot = "02:00:00.000000"
            center_slot = vacancies.objects.filter(
                center_id=id).get(slot_no_id=3)
            center_slot.empty_slots = center_slot.empty_slots - 1
            center_slot.save()
            return redirect(f'/loggedin/3/?center={center}')
        if 'book_4' in request.POST:
            time_slot = "04:00:00.000000"
            center_slot = vacancies.objects.filter(
                center_id=id).get(slot_no_id=4)
            center_slot.empty_slots = center_slot.empty_slots - 1
            center_slot.save()
            return redirect(f'/loggedin/3/?center={center}')

    user = request.user
    name = user.username
    current_url = request.get_full_path()
    center = (str(current_url).split("?"))[1]
    center = (center.split("="))[1]
    id = centers.objects.filter(
        center_name=center).values_list('center_id').first()[0]
    if(vacancies.objects.filter(center_id=id).filter(slot_no_id=1).values_list('empty_slots').first()[0] > 0):
        is_available_1 = "Available"
    else:
        is_available_1 = "Not Available"

    if(vacancies.objects.filter(center_id=id).filter(slot_no_id=2).values_list('empty_slots').first()[0] > 0):
        is_available_2 = "Available"
    else:
        is_available_2 = "Not Available"

    if(vacancies.objects.filter(center_id=id).filter(slot_no_id=3).values_list('empty_slots').first()[0] > 0):
        is_available_3 = "Available"
    else:
        is_available_3 = "Not Available"

    if(vacancies.objects.filter(center_id=id).filter(slot_no_id=4).values_list('empty_slots').first()[0] > 0):
        is_available_4 = "Available"
    else:
        is_available_4 = "Not Available"

    registrant_id = registrants.objects.filter(
        username=name).values_list('registrant_id').first()[0]
    vaccine = vaccination_status.objects.filter(
        registrant_id_id=registrant_id).values_list('vaccine_name').first()[0]
    status = vaccination_status.objects.filter(
        registrant_id_id=registrant_id).values_list('booking_status_id').first()[0]

    return render(request, 'logged-in-2.html', {'status': status, 'name': name, 'registrant_id': registrant_id, 'vaccine': vaccine, 'center': center, 'is_available_1': is_available_1, 'is_available_2': is_available_2, 'is_available_3': is_available_3, 'is_available_4': is_available_4})


def loggedin_3(request):
    if not request.user.is_authenticated:
        return redirect("/")
    user = request.user
    name = user.username
    current_url = request.get_full_path()
    center = (str(current_url).split("?"))[1]
    center = (center.split("="))[1]
    id = centers.objects.filter(
        center_name=center).values_list('center_id').first()[0]
    registrant_id = registrants.objects.filter(
        username=name).values_list('registrant_id').first()[0]
    vaccine = vaccination_status.objects.filter(
        registrant_id_id=registrant_id).values_list('vaccine_name').first()[0]
    status = vaccination_status.objects.filter(
        registrant_id_id=registrant_id).values_list('booking_status_id').first()[0]
    return render(request, 'logged-in-3.html', {'status': status, 'name': name, 'registrant_id': registrant_id, 'vaccine': vaccine, 'center': center})
