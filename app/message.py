import logging
from enum import Enum
import unittest

class MessageTypes(Enum):
    REQUEST = "111111"
    RELEASE = "222222"
    GRANT = "000000"

class Message:
    """# Message class
        This class is responsible for creating and parsing messages in a OO way.
        The raw message format is: messageID|processID|messageType
        Eg: 1|3|000000
        The raw message must have a total size of 10 bytes, 10 characters.
        And thus, the messageID can only have 1 character, the processID can only have 1 character and the messageType can only have 6 characters.
    """
    def __init__(self, messageID: str, processID: str, messageType: MessageTypes):
        self._logger = logging.getLogger(__name__)
        
        if len(messageID) != 1:
            self._logger.error("MessageID size is not 1 byte")
            raise Exception("MessageID size is not 1 byte")
        if len(processID) != 1:
            self._logger.error("ProcessID size is not 1 byte")
            raise Exception("ProcessID size is not 1 byte")
        
        if messageType not in MessageTypes:
            self._logger.error("Message type is not valid")
            raise Exception("Message type is not valid")
        
        if not isinstance(messageType, MessageTypes):
            self._logger.error("Message type is not valid")
            raise Exception("Message type is not valid")
        
        self.messageID = messageID
        self.processID = processID
        self.messageType = messageType

    def create_message(self):
        """
        Creates a message in the format: messageID|processID|messageType,
        with the values of the object. and a total size of 10 bytes.
        Eg: 1|3|000000
        """
        message = f"{self.messageID}|{self.processID}|{self.messageType.value}"
        if len(message) != 10: #Sanity check
            self._logger.error(f"Message size is not 10 bytes")
            raise Exception("Message size is not 10 bytes")
        return message

    def parse_message(self, message:str):
        """
        Parses a message in the format: messageID|processID|messageType,
        and set the values of the object.
        Eg: 1|3|000000
        the message must have a total size of 10 bytes, 10 characters, otherwise this method will raise an exception.
        """
        if len(message) != 10:
            self._logger.error("Message size is not 10 bytes")
            raise Exception("Message size is not 10 bytes")
        parts = message.split("|")
        self.messageID = parts[0]
        self.processID = parts[1]
        self.messageType = MessageTypes(parts[2])


class TestMessage(unittest.TestCase):
    """
    A test case for the Message class.
    """
    def test_create_message(self):
        message = Message('1', '2', MessageTypes.REQUEST)
        self.assertEqual(message.create_message(), '1|2|111111')

    def test_parse_message(self):
        message = Message('1', '2', MessageTypes.REQUEST)
        message.parse_message('3|4|222222')
        self.assertEqual(message.messageID, '3')
        self.assertEqual(message.processID, '4')
        self.assertEqual(message.messageType, MessageTypes.RELEASE)

    def test_invalid_message_type(self):
        with self.assertRaises(Exception):
            Message('1', '2', 'INVALID')

    def test_invalid_message_length(self):
        with self.assertRaises(Exception):
            Message('12', '2', MessageTypes.REQUEST)
        with self.assertRaises(Exception):
            Message('1', '23', MessageTypes.REQUEST)

    def test_invalid_parse_message_length(self):
        message = Message('1', '2', MessageTypes.REQUEST)
        with self.assertRaises(Exception):
            message.parse_message('12345678901')

if __name__ == '__main__':
    unittest.main()