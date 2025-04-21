from django.views import View
from django.shortcuts import render, redirect

from ..repositories.recurringPayment import RecurringPaymentRepository
from django.core.serializers import serialize
from datetime import datetime, time
from ..repositories.transaction import TransactionRepository
class RecurringPaymentView(View):

    def get(self, request):
        tableData = [],
        error_message=''
        try:
            customerId = request.session['customerId']
            if 'errorMessage' in request.session:
                error_message = request.session['errorMessage']
                request.session['errorMessage'] = ''

            tableData = RecurringPaymentRepository.getRecurringPaymentList(
                customerId)
            print("tableData", tableData)
       
        except Exception as e:
            print(e)

        return render(request, 'investment.html', {"tableData": tableData,"error_message": error_message})

    def post(self, request):
        errorMessage = 'Something went wrong!'
        try:
            customerId = request.session['customerId']
            amount = request.POST['amount']
            frequency = request.POST['frequency']
            accountNo = request.POST['account_number']
            _, _, _, currentBalance = TransactionRepository.getTransactionList(
                   customerId)
            status, errorMessage = RecurringPaymentRepository.createNewRecurringPayment(
            request,customerId, amount, currentBalance, accountNo, frequency)

            request.session['errorMessage'] = errorMessage
            return redirect("investment") 
        except Exception as e:
            print(e)
            request.session['errorMessage'] = errorMessage
            return redirect("investment") 
        
   