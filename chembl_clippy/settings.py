from chembl_clippy.singleton import Singleton

@Singleton
class Settings:
    def __init__(self):
        self.host = '10.7.32.34'
        self.port = '8079'

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def setHost(self, host):
        self.host = host

    def setPort(self, port):
        self.port = port

    def getBaseURL(self):
        return 'http://' + self.host + ':' + self.port
