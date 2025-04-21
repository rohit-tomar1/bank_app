from ..models.models import RecurringPayment
from django.db.models import Sum
from datetime import datetime
from .customer import CustomerRepository



class RecurringPaymentRepository:
    @staticmethod
    def getRecurringPaymentList(customer_id):
        try:
            recurringPaymentList = RecurringPayment.objects.filter(
                customer_id=customer_id).order_by('-pk')
            return recurringPaymentList
        except Exception as e:
            print(e)
            return None


    def createNewRecurringPayment(request,customer_id, amount, currentBalance, accountNo, frequency):
        try:
            if (int(request.session['accountNumber']) == int(accountNo)):
                return False, 'You Can Not Transfer Amount To Your Own Account.'

            if (int(amount) > int(currentBalance)):
                return False, 'insufficient Account For this Transaction. Please Try Again With Less Amount.'

            # otherCustomerAcc = CustomerRepository.findAccountByAccountNo(
            #     accountNo)
            # if otherCustomerAcc == None:
            #     return False, 'Invalid Account Number. Please try again!'


            data = {
                "customer_id": customer_id,
                "amount": amount,
                "account_number": accountNo,
                "frequency": frequency,
                "ct": datetime.now().strftime("%Y/%m/%d")

            }
            print("RecurringPayment Data", data)
            RecurringPayment.objects.create(**data)
            return True, 'Success'
        except Exception as e:
            print(e)
            return False, 'Something went wrong!'