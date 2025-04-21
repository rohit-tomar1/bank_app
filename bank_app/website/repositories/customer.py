from ..models.models import Customers
from ..utils.cryptography import Cryptography
from .cards import CardsRepository


class CustomerRepository:
    activeStatus = 'A'
    inActiveStatus = 'I'
    fields = ['account_type', 'title', 'first_name', 'middle_name', 'last_name', 'email',
              'phone_number', 'dob', 'address', 'city', 'country', 'postal_code', 'password']
    encryptedFields = ['phone_number', 'password']

    @staticmethod
    def findById(id):
        data = Customers.objects.filter(
            id=id, status=CustomerRepository.activeStatus)
        if data.exists():
            return data.first()

        return None

    @staticmethod
    def getCustomerDetails(id):
        customer = CustomerRepository.findById(id)
        if customer:
            decryptedData = CustomerRepository.decryptData(customer)
            return decryptedData

        return None

    @staticmethod
    def findByEmail(emailId):
        data = Customers.objects.filter(
            email=emailId, status=CustomerRepository.activeStatus)
        if data.exists():
            return data.first()

        return None

    @staticmethod
    def findAccountByAccountNo(accountNumber):
        data = Customers.objects.filter(
            account_number=accountNumber, status=CustomerRepository.activeStatus)
        if data.exists():
            return data.first()

        return None

    @staticmethod
    def createNewCustomer(request):
        formData = {**request.session['tempData1'], **request.session['tempData2'],
                    **request.session['tempData3'], **request.session['tempData4']}

        customerData = {}
        for key in CustomerRepository.fields:
            customerData[key] = formData.get(key)

        isExist = CustomerRepository.findByEmail(customerData['email'])
        if isExist:
            return False, 'Email Id Already Registered. Please try other one.'

        encryptedCustomerData = CustomerRepository.encryptData(customerData)
        new_customer = Customers.objects.create(**encryptedCustomerData)

        # update account number
        customer_id = new_customer.id
        customer = Customers.objects.get(id=customer_id)
        accountNumber = str(100000+customer_id)
        setattr(customer, 'account_number', accountNumber)
        setattr(customer, 'status', CustomerRepository.activeStatus)
        customer.save()

        caredStatus, msg = CardsRepository.createNewCard(customer_id)
        request.session['customerId'] = customer_id
        CustomerRepository.setUserSession(request)
        return True, 'Success'

    @staticmethod
    def encryptData(data):
        for key in CustomerRepository.encryptedFields:
            if key in data:
                data[key] = Cryptography.encryption(str(data.get(key)))

        return data

    @staticmethod
    def decryptData(customerInstance):
        data = {field.name: getattr(customerInstance, field.name)
                for field in customerInstance._meta.fields}
        for key in CustomerRepository.encryptedFields:
            if key in data:
                data[key] = Cryptography.decryption(str(data.get(key)))

        return data

    @staticmethod
    def getFullName(customerData):
        return customerData.first_name + ' ' + \
            customerData.middle_name + ' '+customerData.last_name

    @staticmethod
    def setUserSession(request):
        customer_id = request.session['customerId']
        customerData = CustomerRepository.findById(customer_id)

        if customerData:
            request.session['customerName'] = CustomerRepository.getFullName(
                customerData)
            request.session['accountNumber'] = customerData.account_number
            request.session['accountType'] = customerData.account_type
            request.session['isLogin'] = True

    @staticmethod
    def deleteUserSession(request):
        request.session.flush()
        print('delete User Session success')

    @staticmethod
    def updateProfile(request, updateData):
        customerId = request.session['customerId']
        customer = Customers.objects.get(id=customerId)
        if 'first_name' in updateData:
            setattr(customer, 'first_name', updateData['first_name'])

        if 'last_name' in updateData:
            setattr(customer, 'last_name', updateData['last_name'])

        if 'phone_number' in updateData:
            phone_number = Cryptography.encryption(
                str(updateData['phone_number']))
            setattr(customer, 'phone_number', phone_number)

        if 'password' in updateData:
            password = Cryptography.encryption(str(updateData['password']))
            setattr(customer, 'password', password)

        if 'account_type' in updateData:
            setattr(customer, 'account_type', updateData['account_type'])

        if 'status' in updateData:
            setattr(customer, 'status', updateData['status'])

        customer.save()
        CustomerRepository.setUserSession(request)
        return True
