import datetime
from typing import cast
from django import http
from django.contrib.messages.api import error
from django.db.models.fields import IntegerField
from django.forms.widgets import Select
from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm  # predefined form
from django.contrib import auth, messages
# defined module in form.py file
from .form import SignUpForm, UserProfileForm, AdminProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import Member_info_Class, VaccineSlot, vaccineBookingClass  # created Model

from .dataModuleFile import UserAgeCheckClass

import requests
from .models import rishuVaccineSlot

# Create your views here.


def get_html_content2(pincode, date):

    r = requests.get(
        f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}')
    all_api_data = None
    rishuVaccineSlot.objects.all().delete()
    if r.status_code == 200:
        response = r.json()['centers']
        for each in response:  # run loop 10 times
            for session in each['sessions']:
                if session['available_capacity_dose1'] >= 0:
                    all_data = rishuVaccineSlot(
                        name=each['name'],
                        state=each['state_name'],
                        district=each['district_name'],
                        pincode=each['pincode'],
                        date=session['date'],
                        vaccine_type=session['vaccine'],
                        min_age_limit=session['min_age_limit'],
                        available_capacity=session['available_capacity']
                    )
                    all_data.save()
                    all_api_data = rishuVaccineSlot.objects.all().order_by('id')
    return all_api_data


def slot(request):
    api_data = None
    if 'pincode' and 'date' in request.GET:
        pincode = request.GET.get('pincode')
        date = request.GET.get('date')
        # api_data = get_html_content(pincode, date)
        api_data = get_html_content2(pincode, date)

    return render(request, 'slot.html', {'api_data': api_data})


class LengthException(Exception):
    pass


# signUp view
def user_signup(request):
    if request.method == 'POST':
        frm = SignUpForm(request.POST)
        try:
            phone = int(request.POST['username'])

            print(type(phone))
            userLength = len(request.POST['username'])

            if userLength != 10:
                raise LengthException
            else:
                if frm.is_valid():
                    frm.save()
                    messages = "User Registered Successfully!!"
                    return HttpResponseRedirect('/login')
        except LengthException as le:
            messages = "Mobile number must be 10 digit"
            print(phone)
            return render(request, 'usersignup.html', {'form': frm, 'message': messages})
        except ValueError:
            messages = "Mobile number not valid!!"
            return render(request, 'usersignup.html', {'form': frm, 'message': messages})
    else:
        frm = SignUpForm()
    return render(request, 'usersignup.html', {'form': frm})


def index(request):
    return render(request, 'index.html')


# login view
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            frm = AuthenticationForm(request=request, data=request.POST)
            if frm.is_valid():
                # data from html page
                uname = frm.cleaned_data['username']
                upass = frm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'User Logged In Successfully')
                    return HttpResponseRedirect('profile')
        else:
            frm = AuthenticationForm()
        return render(request, 'userlogin.html', {'form': frm})
    else:
        return HttpResponseRedirect('profile')


# log out page
def user_logout(request):
    logout(request)
    message = "Successfully Logout"
    return HttpResponseRedirect('login', {'message': messages})


# change password page
def user_changepass(request):
    if request.method == 'POST':
        # as a argument it request for user and as password take password from html page
        frm = PasswordChangeForm(user=request.user, data=request.POST)
        if frm.is_valid():
            frm.save()
            update_session_auth_hash(request, frm.user)
            return HttpResponseRedirect('index')
        else:
            return HttpResponseRedirect('index')
    else:
        frm = PasswordChangeForm(user=request.user)
        return render(request, 'userlogin.html', {'form': frm})


# member view for add member and member data match
def memberView(request):
    # check user is login or not
    if request.user.is_authenticated:
        if request.method == 'POST':
            vaccineObj = Member_info_Class()
            # check for 'add'  type

            # check UID is existed or not
            uidData = Member_info_Class.objects.values('uid')

            # cast data into list
            uidVerification = False
            cast(uidData, list())
            for data in uidData:
                for key, value in data.items():
                    data[key] = str(value)
                    # check data matching
                    if data[key] == str(request.POST['uid']):
                        uidVerification = True
            if uidVerification == False:
                vaccineObj.name = request.POST['name']
                vaccineObj.phone = int(request.user.username)
                vaccineObj.uid = request.POST['uid']
                vaccineObj.total_member = 5
                vaccineObj.age = request.POST['age']

                # fetch data from vaccine booking table for store date
                # memberData = vaccineBookingClass.objects.values(
                #     'first_dose', 'second_dose').filter(phone=request.user.username)
                # print(memberData['first_dose'])
                # print(memberData['second_dose'])
                # print(memberData.second_dose)
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                # formatdate = tomorrow.strftime('%d/%m/%y')
                # vaccineObj.first_booking = "null"
                # vaccineObj.second_booking = "null"
                vaccineObj.save()
                print(request.POST['name'])
                messages.success(request, 'data inserted Successfully')
                return render(request, 'index.html', {'message': messages})
            else:
                messages.error(request, 'UID Already Existed!!')
                return render(request, 'index.html', {'message': messages})

            # elif request.POST['show']:
            #     pass
            # else:
            #     data = Member_info_Class.objects.all()
            #     print(data.name)
            #     return render(request, 'vaccineBooking.html', {'Objdata': data})

        else:
            memberData = Member_info_Class.objects.filter(
                phone=request.user.username)
            return render(request, 'member.html', {'data': memberData})
    else:
        return HttpResponseRedirect('login')


# Vaccine Booking Page
def booking(request):
    if request.method == 'POST':

        # Access pincode data from vaccioneslot with the help of vaccine slot class model
        pincodeData = VaccineSlot.objects.values('pin_code')

        # Access UID data from member_info_table with the help of  member_info_class model
        uidData = Member_info_Class.objects.values(
            'uid').filter(phone=request.user.username)

        vaccine_booked_uid = vaccineBookingClass.objects.values('uid')

        # cast query set into list
        cast(pincodeData, list())
        cast(uidData, list())
        cast(vaccine_booked_uid, list())

        print(pincodeData)
        print(uidData)
        print(vaccine_booked_uid)

        is_pincode_found = False
        is_uid_found = False
        is_booked_uid = False

        # for checking UID data for booking vaccine
        for data in vaccine_booked_uid:
            for key, value in data.items():
                data[key] = value
                if data[key] == int(request.POST['uid']):
                    is_booked_uid = True

        # for checking UID data
        for data in pincodeData:
            for key, value in data.items():
                data[key] = value
                if data[key] == int(request.POST['pincode']):
                    is_pincode_found = True

        # for checking UID data
        for adhardata in uidData:
            for key, value in adhardata.items():
                adhardata[key] = value
                if adhardata[key] == int(request.POST['uid']):
                    is_uid_found = True

        print(is_booked_uid)
        print(is_pincode_found)
        print(is_uid_found)

        # if uid and pincode found
        if is_pincode_found and is_uid_found and is_booked_uid == False:
            member_verification = vaccineBookingClass.objects.filter(uid=request.POST['uid']).values(
                'first_dose', 'second_dose', 'first_verification', 'second_verification')
            cast(member_verification, list())
            # print(member_verification)
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            formatdate = tomorrow.strftime('%d/%m/%y')

            # OBJECT cteation of vaccine booking class
            vaccineBooking_Obj = vaccineBookingClass()

            # fetch data for metched data
            memberData = Member_info_Class.objects.get(uid=request.POST['uid'])
            locationData = VaccineSlot.objects.get(
                pin_code=request.POST['pincode'])

            # inserte data
            vaccineBooking_Obj.uid = request.POST['uid']
            vaccineBooking_Obj.name = memberData.name
            vaccineBooking_Obj.city = locationData.city
            vaccineBooking_Obj.pincode = request.POST['pincode']
            vaccineBooking_Obj.name = memberData.name
            vaccineBooking_Obj.phone = memberData.phone
            vaccineBooking_Obj.first_dose = tomorrow
            try:
                print(vaccineBooking_Obj)
                vaccineBooking_Obj.save()
                messages = "inserted successfullyy"
            except Exception:
                print("no duplicate value")
                messages = "uid already regsitered"
            return render(request, "profile.html")
        elif is_pincode_found and is_uid_found and is_booked_uid == True:
            vaccineBooking_Obj = vaccineBookingClass()
            member_verification = vaccineBookingClass.objects.filter(uid=request.POST['uid']).values(
                'first_dose', 'second_dose', 'first_verification', 'second_verification')

            cast(member_verification, list())

            first_d = None
            second_d = None
            first_v = False
            second_v = False
            for data in member_verification:
                for key, value in data.items():
                    first_d = data['first_verification']
                    second_d = data['second_verification']
                    first_v = data['first_dose']
                    second_v = data['second_dose']

            print(second_v)
            if first_v + datetime.timedelta(days=84) > datetime.date.today() and second_v == False:
                obj = vaccineBookingClass.objects.get(uid=request.POST['uid'])
                obj.second_dose = datetime.date.today()
                obj.save()
                messages = "2nd dose slot booked"
                return render(request, "profile.html", {'messages': messages})
            elif first_v == False:
                messages = "Your 1st Verification is pending"
                return render(request, "profile.html", {'messages': messages})
            elif first_v == True and second_v == True:
                messages = "you have done with both vaccine"
                return render(request, "profile.html", {'messages': messages})
            else:
                messages = "you can book slot after ", first_v + \
                    datetime.timedelta(days=84)
                return render(request, "profile.html", {'messages': messages})
        else:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            formatdate = tomorrow.strftime('%d/%m/%y')
            messages = " UID NOT MATCHED!!"
            return render(request, "vaccineBookking.html", {'message': messages})
    else:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        formatdate = tomorrow.strftime('%d/%m/%y')
        return render(request, 'vaccineBookking.html', {'date': formatdate})


# Add Vaccine slot
def vaccineSlotView(request):
    if request.method == 'POST':
        slotObj = VaccineSlot()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        # formatdate = tomorrow.strftime('%yy/%mm/%dd')
        slotObj.date = tomorrow
        slotObj.city = request.POST['city']
        slotObj.pin_code = request.POST['pin_code']
        slotObj.vaccine_12 = request.POST['vac_12']
        slotObj.vaccine_18 = request.POST['vac_18']
        slotObj.vaccine_45 = request.POST['vac_45']
        slotObj.vaccine_60 = request.POST['vac_60']

        slotObj.save()
        return HttpResponseRedirect('index')
    else:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        formatdate = tomorrow.strftime('%d/%m/%y')
        return render(request, 'vaccineslot.html', {'date': formatdate})


# User profile view
def user_profile(request):
    if request.user.is_authenticated:  # check user logged in or not
        if request.user.username == 7782846390:
            print("U r a admin")
        else:
            print("U R A User..")
        name = (request.user.first_name + " " +
                request.user.last_name).capitalize()
        if request.user.is_superuser == True:
            frm = AdminProfileForm(instance=request.user)
            return render(request, 'profile.html', {'name': name, 'form': frm})
        else:
            # derived from pre-defied form userchangeform
            frm = UserProfileForm(instance=request.user)
            return render(request, 'profile.html', {'name': name, 'form': frm})
    else:
        return HttpResponseRedirect('login')


# profile view


# def Access_Auth_User


def datafetchview(request):
    # uidData = vaccineBookingClass.objects.values(
    #     'phone').filter(uid=123456789123)
    data = vaccineBookingClass.objects.all()
    print(data)
    return render(request, 'datafetch.html')


# verification view for verify user uid and Ref Id number
def verification_view(request):
    if request.user.is_superuser:
        messages = ""
        if request.method == "POST":
            try:
                # access data from vaccine Booking table
                member_vaccine_data = vaccineBookingClass.objects.get(
                    uid=request.POST['uid'])

                # access data from member info table
                member_profile_data = Member_info_Class.objects.get(
                    uid=request.POST['uid'])

                # verification of user data
                if member_vaccine_data.uid == int(request.POST['uid']) and member_vaccine_data.id == int(request.POST['ref_id']):
                    # Update value for Second booking
                    if member_vaccine_data.first_verification == True:
                        member_vaccine_data.second_verification = True
                        member_profile_data.second_booking = member_vaccine_data.second_dose

                    # Update value for first booking
                    member_vaccine_data.first_verification = True
                    member_profile_data.first_booking = member_vaccine_data.first_dose

                    # save value
                    member_vaccine_data.save()
                    member_profile_data.save()

                    messages = "Data Matched Successfully(Verified)"
                    return render(request, 'verification.html', {'messages': messages})
                else:
                    messages = "Data Not Matched Successfully"
                    return render(request, 'verification.html', {'messages': messages})
            except Exception as e:
                member_vaccine_data = vaccineBookingClass.objects.get(
                    uid=int(request.POST['uid']))
                messages = "Data Not Matched"
            return render(request, 'verification.html', {'messages': messages})
        else:
            return render(request, 'verification.html', {'messages': messages})
    else:
        return render(request, "profile.html")


def contact_view(request):
    return render(request, "contact.html")
