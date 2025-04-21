from ..models.models import Transaction
from django.db.models import Sum
from datetime import datetime

from .customer import CustomerRepository


class TransactionRepository:
    transactionType = {
        "depositType": 'deposit',
        "withdrawType": 'withdraw',
        "transferType": 'transfer',
        "creditType": 'credit',
        "allType": ['deposit', 'withdraw', 'transfer', 'credit']
    }

    @staticmethod
    def getTransactionList(customer_id):
        try:
            include_trans_type = [
                TransactionRepository.transactionType.get('depositType'),
                TransactionRepository.transactionType.get('creditType')
            ]
            exclude_trans_types = [
                TransactionRepository.transactionType.get('depositType'),
                TransactionRepository.transactionType.get('creditType')
            ]
            transactionList = Transaction.objects.filter(
                customer_id=customer_id).order_by('-pk')
            totalIncome = Transaction.objects.filter(transType__in=include_trans_type, customer_id=customer_id).aggregate(
                total_amount=Sum('amount'))['total_amount']

            totalOutcome = Transaction.objects.filter(customer_id=customer_id).exclude(
                transType__in=exclude_trans_types, customer_id=customer_id).aggregate(total_amount=Sum('amount'))['total_amount']

            if totalIncome == None:
                totalIncome = 0

            if totalOutcome == None:
                totalOutcome = 0

            totalBalance = totalIncome - totalOutcome

            return transactionList, totalIncome, totalOutcome, totalBalance
        except Exception as e:
            print(e)
            return 0, 0, 0, 0

    def deposit(customer_id, amount, transType='', summary=''):
        try:
            data = {
                "customer_id": customer_id,
                "amount": amount,
                "summary": summary,
                "transType": transType or TransactionRepository.transactionType.get('depositType'),
                "date": datetime.now().strftime("%Y/%m/%d")

            }
            Transaction.objects.create(**data)
            return True, 'Success'
        except Exception as e:
            print(e)
            return False, 'Something went wrong!'

    def transfer(request, accountNo, amount, currentBalance, transType=''):
        try:
            if (int(request.session['accountNumber']) == int(accountNo)):
                return False, 'You Can Not Transfer Amount To Your Own Account.'

            if (int(amount) > int(currentBalance)):
                return False, 'insufficient Account For this Transaction. Please Try Again With Less Amount.'

            customerId = request.session['customerId']
            otherCustomerAcc = CustomerRepository.findAccountByAccountNo(
                accountNo)
            if otherCustomerAcc == None:
                return False, 'Invalid Account Number. Please try again!'

            TransactionRepository.withdraw(
                customerId,
                amount,
                currentBalance,
                transType,
                summary='Transfer to :' +
                CustomerRepository.getFullName(
                    otherCustomerAcc) + " | AccNo.: " + accountNo
            )

            TransactionRepository.deposit(
                otherCustomerAcc.id,
                amount,
                TransactionRepository.transactionType.get('creditType'),
                summary='Received from : ' +
                request.session['customerName'] + " | AccNo.: " +
                request.session['accountNumber']
            )

            return True, 'Success'
        except Exception as e:
            print(e)
            return False, 'Something went wrong!'

    def withdraw(customer_id, amount, currentBalance, transType='', summary=''):
        try:
            if (int(amount) > int(currentBalance)):
                return False, 'insufficient Account For this Transaction. Please Try Again With Less Amount.'

            data = {
                "customer_id": customer_id,
                "amount": amount,
                "summary": summary,
                "transType": transType or TransactionRepository.transactionType.get('depositType'),
                "date": datetime.now().strftime("%Y/%m/%d")

            }
            Transaction.objects.create(**data)
            return True, 'Success'
        except Exception as e:
            print(e)
            return False, 'Something went wrong!'
