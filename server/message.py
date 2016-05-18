# Message class object definition

class Messsage(object):
    '''
    Class used to represent a sturcture of the data contained in a message
    '''
    def __init__(self, version, message_type, payload=None, client_id=None):
        '''
        Intialization function of message class object.
        Input:
            Version: Message Version, required for all messages
            Message Type: Message Type, required for all messages
            Payload: Payload contained in the data, not required for all messages
            Client ID: ID associated in message, not required for all messages
        '''
        self.version = version
        self.message_type = message_type
        self.payload = payload
        self.client_id = client_id