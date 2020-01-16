import os 
class Configuration(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "a{!8OIMiUbkjgoHLj<6hExVIFhXt+%"
    CONNECTION_PASSWORD = "C4pyEOgx7lD1dnce"
    CONNECTION_USER = "danver98"
    CLUSTER = "cluster0-nsbea"

    @property
    def DATABASE_URI(self):
        return "mongodb+srv://{}:{}@{}.mongodb.net/test?retryWrites=true&w=majority".format(self.CONNECTION_USER,self.CONNECTION_PASSWORD,self.CLUSTER)
    
class ProductionConfiguration(Configuration):
    ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY') or "%CsVWbiaN}mk)0cj)~IV#fd+C*p,1o"

class DevelopmentConfiguration(Configuration):
    DEBUG = True
    ENV = 'development'
    CONNECTION_PASSWORD="UJPzENtW2usNKzUj"
    CLUSTER ="cluster1-im2oj"
    DATABASE_URI = "mongodb+srv://{}:{}@{}.mongodb.net/test?retryWrites=true&w=majority".format(Configuration.CONNECTION_USER,CONNECTION_PASSWORD,CLUSTER)