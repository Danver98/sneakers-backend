import urllib
import json

class JsonGate:
  """class for using prostor-sms.ru service via JSON interface"""
  
  __host = 'json.gate.prostor-sms.ru'
  
  def __init__(self, api_login, api_password):
    self.login = api_login
    self.password = api_password
 
  def __sendRequest(self, uri, params={}):
    url = self.__getUrl(uri)
    data = self.__formPacket(params)
    try:
      f = urllib.request.urlopen(url, data)
      result = f.read()
      return eval(result)
    except IOError as e:
      return dir(e)
 
  def __getUrl(self, uri):
    return "http://%s/%s/" % (self.getHost(), uri)
 
  def __formPacket(self, params={}):
    params["login"] = self.login
    params["password"] = self.password
    for key,value in params.items():
      if value is None:
        del params[key]
    packet = json.dumps(params)
    return packet
 
  def getHost(self):
    """Return current requests host """
    return self.__host
 
  def setHost(self, host):
    """Changing default requests host """
    self.__host = host
 
  def send(self, messages, statusQueueName=None, scheduleTime=None):
    """Sending sms packet"""
    params = {"messages": messages,
       'statusQueueName': statusQueueName,
          'scheduleTime': scheduleTime,
             }
    return self.__sendRequest('send', params)
 
  def status(self, messages):
    """Retrieve sms statuses packet by its' ids """
    params = {"messages": messages}
    return self.__sendRequest('status', params)
 
  def statusQueue(self, statusQueueName, limit = 5):
    """Retrieve latest statuses from queue """
    params = {'statusQueueName': statusQueueName, 'statusQueueLimit':limit}
    return self.__sendRequest('statusQueue', params)
 
  def credits(self):
    """Retrieve current credit balance """
    return self.__sendRequest('credits')
 
  def senders(self):
    """Retrieve available signs """
    return self.__sendRequest('senders')


if __name__ == "__main__":
  print(JsonGate.__doc__)