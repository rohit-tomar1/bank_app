from django.shortcuts import render, HttpResponse, redirect
from website.forms import CustomersForm 
import pyotp
from django.conf import settings
from django.core.mail import send_mail
from website.forms import CustomersForm, TransactionForm 
from .models.models import Customers
from .models.models import Transaction
from django.db.models import Sum
from django.db import OperationalError
from datetime import date, datetime, time, timedelta
# from backports.datetime_fromisoformat import MonkeyPatch
# MonkeyPatch.patch_fromisoformat()
from django.db.models import Q
from django.core.serializers import serialize
import time

from .utils.otp import OTPHandler

def home(request):
    return render(request, 'login.html', {'title': 'home'})

def about(request):
    return render(request, 'login.html', {'title': 'about'})

def login(request):
    error_message =None
    if request.method == 'POST':
        emailID = request.POST['email']
        password = request.POST['password']
        if Customers.objects.filter(email=request.POST['email']).exists() and Customers.objects.filter(email=request.POST['email'])[0].status == "Active":
            if Customers.objects.filter(email=request.POST['email'])[0].password == password:
                username = Customers.objects.filter(email=request.POST['email'])[0].last_name
                send_otp(request, emailID)
                request.session['username'] = username
                request.session['email'] = emailID
                return redirect('otp')
            else:
                error_message = 'Invalid password. Please enter correct password'
                pass
        else:
           error_message = 'Invalid email ID. Please enter valid Email ID'
           pass
    return render(request, 'login.html', {"error_message": error_message})
    
def main(request):
    isSuccess = False
    if request.method == "POST":  
        form = TransactionForm(request.POST)  
        if form.is_valid():  
            try: 
                form.instance.email = request.session['email'] 
                form.instance.date = datetime.now().strftime("%d/%m/%Y")
                form.instance.status = "Success" 
                form.save() 
                isSuccess = True;
                return redirect('main')

            except:  
                   pass
    else:  
        form = TransactionForm()  
    
    try:
        tableData = Transaction.objects.filter(email=request.session['email']).order_by('-pk') 
        totalIncome = Transaction.objects.filter(transType="deposit", email = request.session['email']).aggregate(total_amount=Sum('amount'))['total_amount']
        totalOutcome = Transaction.objects.filter(email=request.session['email']).exclude(transType="deposit", email = request.session['email']).aggregate(total_amount=Sum('amount'))['total_amount']
        if(totalIncome == None):
            totalIncome = 0
        if(totalOutcome == None):
            totalOutcome = 0
        totalBalance = totalIncome - totalOutcome
    except OperationalError as e:
        tableData = [];
        totalIncome= 0;
        totalOutcome=0;
        totalBalance=0;

    return render(request, 'main.html',{'username': request.session['username'], 'tableData' : tableData, 'totalIncome' : totalIncome,
    "totalOutcome" : totalOutcome, "totalBalance" : totalBalance, "isSuccess": isSuccess})

def card(request):
    if request.method =="POST" :
        request.session['tempData0'] = request.POST
        if request.POST['actionBtn'] == 'Proceed':
            return redirect('dashboard')

    return render(request, 'card.html')


def setting(request):
    editmessage=""
    passwordmessage=""
    closemessage=""
    if request.method=="POST":
        if request.POST['actionBtn'] == 'Submit':
            user = Customers.objects.filter(email=request.session['email'])  
            for obj in user:
                if request.POST['first_name']:
                    obj.first_name = request.POST['first_name']
                if request.POST['last_name']:
                    obj.last_name = request.POST['last_name']
                if request.POST['phone_number']:
                    obj.phone_number = request.POST['phone_number']
                obj.save()
                editmessage = "Saved Successfully"
        if request.POST['actionBtn'] == 'Change Password':
            user = Customers.objects.filter(email=request.session['email'])
            for obj in user:
                if request.POST['password']:
                    obj.password = request.POST['password']  
                obj.save()
                passwordmessage = "Saved Successfully"
        if request.POST['actionBtn'] == 'Close Account':
            user = Customers.objects.filter(email=request.session['email'])
            for obj in user:
                obj.status = "Close" 
                obj.save()
            closemessage = "Closed Successfully"
            time.sleep(5)
            return redirect('login')
                
    return render(request, 'settings.html',{"passwordmessage":passwordmessage,"editmessage":editmessage, "closemessage": closemessage})

def investment(request):
    return render(request, 'investment.html')

def loan(request):
    return render(request, 'loan.html')

def help(request):
    return render(request, 'help.html')

def filterTransaction(date="", amount="", transType="", email=""):
    if date:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")  
    if(date and not amount and  transType=="None"):
        tableDataFilter = Transaction.objects.filter(Q(date=date) & Q(email=email)).order_by('-pk') 
    elif (transType != "None" and not amount and not date ):
        tableDataFilter = Transaction.objects.filter(Q(transType=transType) & Q(email=email)).order_by('-pk')
    elif(amount and not date and transType=="None"):
        tableDataFilter = Transaction.objects.filter(Q(amount=amount) & Q(email=email)).order_by('-pk') 
    elif(date and amount and transType =="None"):
        tableDataFilter = Transaction.objects.filter(Q(amount=amount) & Q(date=date) & Q(email=email)).order_by('-pk') 
    elif(transType != "None" and amount and not date):
        tableDataFilter = Transaction.objects.filter(Q(amount=amount) , Q(transType=transType) ,Q(email=email)).order_by('-pk') 
    elif(transType != "None" and date and not amount):
        tableDataFilter = Transaction.objects.filter(Q(date=date) & Q(transType=transType) & Q(email=email)).order_by('-pk') 
    else :
        tableDataFilter = Transaction.objects.filter(email=email).order_by('-pk') 
    return tableDataFilter

def transaction(request):
    date=''
    amount=''
    transType='None'
    try:
        if request.method =="POST":
            if request.POST['actionBtn'] == "Filter":
                date=request.POST['date']
                amount=request.POST['amount']
                transType=request.POST['transType']
                if(date or amount or transType):
                    tableData = filterTransaction(date, amount, transType, request.session['email'])
            if request.POST['actionBtn'] == "Clear Filter":
                date=''
                amount = ''
                transType = 'None'
                tableData = Transaction.objects.filter(email=request.session['email']).order_by('-pk')
                
        else:
            tableData = Transaction.objects.filter(email=request.session['email']).order_by('-pk') 
        totalUnFilteredDataCount =  Transaction.objects.filter(email=request.session['email']).order_by('-pk').count() 

    except OperationalError as e:
        tableData = [];
    return render(request, 'transaction.html', {"tableData" : tableData, "date": date, "amount":amount, "transType":transType, "totalUnFilteredDataCount":totalUnFilteredDataCount, "transactionData": serialize('json', tableData)})

def signup1(request):
    if request.method =="POST" :
         request.session['tempData1'] = request.POST
         if request.POST['actionBtn'] == 'Proceed':
             return redirect('signup2')

    return render(request, 'signup1.html')

def signup2(request):
    if request.method =="POST" :
         request.session['tempData2'] = request.POST
         if request.POST['actionBtn'] == 'Proceed':
            return redirect('signup3')
         else:
            return redirect('signup1')
    return render(request, 'signup2.html')

def signup3(request):
    if request.method =="POST" :
         request.session['tempData3'] = request.POST
         if request.POST['actionBtn'] == 'Proceed':
             return redirect('signup4')
         else:
             return redirect('signup2')
    return render(request, 'signup3.html')

def signup4(request):
    if request.method == "POST":
        request.session['tempData4'] = request.POST
        request.session['username'] = dict(request.session['tempData1'].items()).get('last_name')
        request.session['email'] = dict(request.session['tempData2'].items()).get('email')
        if request.POST['actionBtn'] == 'Proceed':
             send_otp(request, dict(request.session['tempData2'].items()).get('email'))
             return redirect('otp')
        else:
             return redirect('signup3')

    return render(request, 'signup4.html')

def addNewUserDataToDatabase(request):
    if request.method == "POST": 
        form = CustomersForm(request.POST)  
        if form.is_valid(): 
            try:  
                form.instance.title = dict(request.session['tempData1'].items()).get('title')
                form.instance.first_name = dict(request.session['tempData1'].items()).get('first_name')
                form.instance.middle_name = dict(request.session['tempData1'].items()).get('middle_name')
                form.instance.last_name =dict(request.session['tempData1'].items()).get('last_name')
                form.instance.email = dict(request.session['tempData2'].items()).get('email')
                form.instance.phone_number= dict(request.session['tempData2'].items()).get('phone_number')
                form.instance.dob =dict(request.session['tempData2'].items()).get('dob')
                form.instance.address =dict(request.session['tempData3'].items()).get('address')
                form.instance.city=dict(request.session['tempData3'].items()).get('city')
                form.instance.country= dict(request.session['tempData3'].items()).get('country')
                form.instance.postal_code =dict(request.session['tempData3'].items()).get('postal_code')
                form.instance.password =dict(request.session['tempData4'].items()).get('password')
                form.instance.status = "Active"
                form.save() 
                 
                return
            except Exception as e:  
                pass  
        else:
            pass

def formOTP(request):
    otp1 = request.POST['otp1'];
    otp2 = request.POST['otp2'];
    otp3 = request.POST['otp3'];
    otp4 = request.POST['otp4'];
    otp5 = request.POST['otp5'];
    otp6 = request.POST['otp6'];
    otp = otp1+otp2+otp3+otp4+otp5+otp6
    return otp

def otp(request):
    error_message =None
    if request.method == 'POST':
        otp = formOTP(request)
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']    
        if otp=="":
            error_message ="Please enter OTP"
        elif request.session['otp'] != otp :
            error_message = "Invalid OTP. Please enter valid OTP" 
        elif datetime.fromisoformat(otp_valid_until) < datetime.now():
            error_message = "Password Epired. Please Login/ Sign Up again "
        else:
            error_message = None
        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval = 60)
                if totp.verify(otp):
                    if request.session['otp'] == formOTP(request) :
                        if request.POST['actionBtn'] == 'Verify Email':
                            addNewUserDataToDatabase(request)
                            return redirect('main')                         
                        else:
                            return redirect('signup1')
                    else :
                        if request.POST['actionBtn'] == 'Cancel':
                            return redirect('signup1')
                        else:
                            pass    
            else:   
                if request.POST['actionBtn'] == 'Cancel':
                    return redirect('signup1')
                else:
                    pass  
        else:
            if request.POST['actionBtn'] == 'Cancel':
                    return redirect('signup1')
            else:
                 pass  
    else:  
        pass      
    return render(request, 'otp.html',{"error_message" : error_message, "emailID": request.session['email']})
    
def send_otp(request, emailID):
    totp = pyotp.TOTP(pyotp.random_base32(), interval = 60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now()+ timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    request.session['otp'] = otp
    #email functionality
    # subject = 'OTP Testing Mail'
    # message = f'Hi this is your OTP {otp}.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [emailID]
    # send_mail( subject, message, email_from, recipient_list )

    print(f"YOUR OTP IS {otp}")
