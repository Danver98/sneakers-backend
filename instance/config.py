class Configuration(object):
    DEBUG = True
    SECRET_KEY = "ddeed"
    CONNECTION_PASSWORD = "C4pyEOgx7lD1dnce"
    CONNECTION_USER = "danver98"

    @property
    def DATABASE_URI(self):
        return "mongodb+srv://{}:{}@cluster0-nsbea.mongodb.net/test?retryWrites=true&w=majority".format(self.CONNECTION_USER,self.CONNECTION_PASSWORD)
    