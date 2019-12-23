"""
from prostor-smsjson import JsonGate
gate = JsonGate('api_login', 'api_password')

print gate.credits() # узнаем текущий баланс
print gate.senders() # получаем список доступных подписей
"""
messages = [{
"clientId" : "1",
"phone": "71234567890",
"text": "first message",
"sender": "TEST"
},
{
"clientId" : "2",
"phone": "71234567891",
"text": "second message",
"sender": "TEST",
},
{
"clientId" : "3",
"phone": "71234567892",
"text": "third message",
"sender": "TEST",
}
]
"""
print gate.send(messages, 'testQueue') #отправляем пакет sms

messages =
[{"clientId":"1","smscId":11255142},{"clientId":"2","smscId":11255143},{"clie
ntId":"3","smscId":11255144}]
print gate.status(messages) # получаем статусы для пакета sms
print gate.statusQueue('testQueue', 10) # получаем статусы из очереди 'testQueue'
"""