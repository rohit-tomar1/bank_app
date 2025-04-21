from django.views import View
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ..repositories.transaction import TransactionRepository, Transaction
from django.core.serializers import serialize
from datetime import datetime, time


@method_decorator(never_cache, name='dispatch')
class TransactionView(View):

    def get(self, request):
        date = ''
        amount = ''
        transType = 'None'
        customerId = request.session['customerId']
        tableData = []
        try:
            tableData, _, _, _ = TransactionRepository.getTransactionList(
                customerId)
            totalUnFilteredDataCount = tableData.count()

        except Exception as e:
            print(e)

        return render(request, 'transaction.html', {"tableData": tableData, "date": date, "amount": amount, "transType": transType, "totalUnFilteredDataCount": totalUnFilteredDataCount, "transactionData": serialize('json', tableData)})

    def post(self, request):
        date = ''
        amount = ''
        transType = 'None'
        tableData = []
        totalUnFilteredDataCount = 0
        try:
            customerId = request.session['customerId']
            if request.POST['actionBtn'] == "Filter":
                date = request.POST['date']
                amount = request.POST['amount']
                transType = request.POST['transType']
                if (date or amount or transType):
                    tableData = TransactionView.filterTransaction(
                        date, amount, transType, customerId)
                    totalUnFilteredDataCount = tableData.count()

            if request.POST['actionBtn'] == "Clear Filter":
                tableData, _, _, _ = TransactionRepository.getTransactionList(
                    customerId)
                totalUnFilteredDataCount = tableData.count()

        except Exception as e:
            print(e)

        return render(request, 'transaction.html', {"tableData": tableData, "date": date, "amount": amount, "transType": transType, "totalUnFilteredDataCount": totalUnFilteredDataCount, "transactionData": serialize('json', tableData)})

    @staticmethod
    def filterTransaction(date="", amount="", transType="", customer_id=""):
        activeFiler = {
            "customer_id": customer_id
        }
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")
            start_date = datetime.combine(date, time.min)
            end_date = datetime.combine(date, time.max)

            activeFiler['date__range'] = (start_date, end_date)

        if transType and transType != 'None':
            activeFiler['transType'] = transType
        if amount:
            activeFiler['amount'] = amount

        tableDataFilter = Transaction.objects.filter(
            **activeFiler).order_by('-pk')

        return tableDataFilter