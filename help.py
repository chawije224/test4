class MainHelper:

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.uid = message.message_id
        self.subproc = None


class OtherHelper:

    def __init__(self, listener):
        self.__listener = listener
        self.__dir = f'{listener.uid}'
        self.__pssh = None
        self.__vid = None
        self.__aud = None
        self.__keys = None
        self.__mpd = None