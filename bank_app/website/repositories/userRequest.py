from ..models.models import UserRequest


class UserRequestRepository:
    openStatus = 'O'
    closeStatus = 'C'
    requestType = {
        "checkbook": 'checkbook',
        "fraud": 'fraud',
        "loan": 'loan',
        "allType": ['checkbook', 'fraud', 'loan']
    }

    @staticmethod
    def createNewRequest(customerId, requestType, summary):
        customerData = {
            "customer_id": customerId,
            "requestType": requestType,
            "summary": summary,
            "status": UserRequestRepository.openStatus,
        }
        UserRequest.objects.create(**customerData)
        return True, 'Request has been rasied Successfully.'
