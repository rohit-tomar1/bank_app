from ..models.models import Cards
from ..utils.cryptography import Cryptography
from random import randint


class CardsRepository:
    activeStatus = 'A'
    inActiveStatus = 'I'
    encryptedFields = ['card_number', 'pin_number', 'security_code']

    @staticmethod
    def createNewCard(customerId):
        customerData = {
            "customer_id": customerId,
            "status": CardsRepository.activeStatus,
        }
        customerData['card_number'] = '4147' + \
            str(randint(1000, 9999)) + \
            str(randint(1000, 9999)) + str(randint(1000, 9999))
        customerData['security_code'] = str(randint(1000, 9999))
        customerData['pin_number'] = str(randint(100, 999))
        customerData['valid_till'] = str(
            randint(1, 12)) + '/' + str(randint(30, 35))
        

        encryptedCustomerData = CardsRepository.encryptData(customerData)
        Cards.objects.create(**encryptedCustomerData)
        return True, 'Success'

    @staticmethod
    def encryptData(data):
        for key in CardsRepository.encryptedFields:
            if key in data:
                data[key] = Cryptography.encryption(str(data.get(key)))

        return data

    @staticmethod
    def decryptData(data):
        for key in CardsRepository.encryptedFields:
            if key in data:
                data[key] = Cryptography.decryption(str(data.get(key)))

        return data

    @staticmethod
    def getCardDetails(customerId):
        data = Cards.objects.filter(
            customer_id=customerId, status=CardsRepository.activeStatus)
        cardData = data
        if len(data) > 1:
            cardData = data[0]
        return CardsRepository.decryptData(cardData)

    def blockCard(cardId):
        cardDetails = Cards.objects.get(id=cardId)
        setattr(cardDetails, 'status', CardsRepository.inActiveStatus)
        cardDetails.save()
        return True, "Success"

    def unBlockCard(cardId):
        cardDetails = Cards.objects.get(id=cardId)
        setattr(cardDetails, 'status', CardsRepository.activeStatus)
        cardDetails.save()
        return True, "Success"

    def updateCardPin(cardId, newPin):
        cardDetails = Cards.objects.get(id=cardId)
        setattr(cardDetails, 'pin_number',
                Cryptography.encryption(str(newPin)))
        cardDetails.save()
        return True, "Success"
