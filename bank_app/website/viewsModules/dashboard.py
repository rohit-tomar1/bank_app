from django.views import View
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..repositories.transaction import TransactionRepository


@method_decorator(never_cache, name='dispatch')
class DashboardView(View):

    def get(self, request):
        isSuccess = False
        tableData = []
        totalIncome = 0
        totalOutcome = 0
        totalBalance = 0
        error_message = ''
        account_number = ''
        account_type = ''
        username = ''

        try:
            customerId = request.session['customerId']
            account_number = request.session['accountNumber']
            account_type = request.session['accountType'].capitalize()
            username = request.session['customerName']
            if 'errorMessage' in request.session:
                error_message = request.session['errorMessage']
                request.session['errorMessage'] = ''

            tableData, totalIncome, totalOutcome, totalBalance = TransactionRepository.getTransactionList(
                customerId)

        except Exception as e:
            print(e)
            pass

        return render(request, 'main.html', {'username': username, 'account_number': account_number, 'account_type': account_type, 'tableData': tableData, 'totalIncome': totalIncome,
                                             "totalOutcome": totalOutcome, "totalBalance": totalBalance, "isSuccess": isSuccess, "error_message": error_message})

    def post(self, request):
        customerId = request.session['customerId']
        amount = request.POST['amount']
        transType = request.POST['transType']
        errorMessage = ''
        customerId = request.session['customerId']
        tableData, totalIncome, totalOutcome, currentBalance = TransactionRepository.getTransactionList(
            customerId)
        if transType == TransactionRepository.transactionType.get('depositType'):
            summary = request.POST['remark']
            status, errorMessage = TransactionRepository.deposit(
                customerId, amount, transType, summary)

        elif transType == TransactionRepository.transactionType.get('withdrawType'):
            summary = request.POST['remark']
            status, errorMessage = TransactionRepository.withdraw(
                customerId, amount, currentBalance, transType, summary)

        elif transType == TransactionRepository.transactionType.get('transferType'):
            otherAccountNo = request.POST['account_number']
            status, errorMessage = TransactionRepository.transfer(
                request, otherAccountNo, amount, currentBalance, transType)

        request.session['errorMessage'] = errorMessage
        return redirect('main')
