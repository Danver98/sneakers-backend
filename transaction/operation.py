from flask import jsonify, request, Blueprint,flash,redirect,url_for,render_template,get_flashed_messages
import random 
import user
bp = Blueprint('author',__name__,url_prefix='/author')

#какой url?
def place_order():

  # принимаем объект корзины
  buy_content = user.get_basket_data()

  # ждем заполнения карты и подтверждения 
  card_entry()

  # true - удаляем(хотя надо перенести в колекцию "на обработку") объект корзины
  # сообщае что все ок
  # чистим
  # возращаем на главную страницу

  # false - забываем корзину(чистим)
  # возращаем на главную страницу

  # если ошибка не правильно заполнена карта то во зращаем на карту
  #
@bp.route('/card_entry/',method = ['POST'])
def card_entry():
  if request.method == 'POST':
    data = request.get_json(force=True)
    nomber_card = data['nomber_card']
    holder = data['holder']
    per_of_valid = data['per_of_valid']
    cvv = data['cvv']
    error = None
    if not nomber_card:
      error = "Не введен номер карты"
      flash(error)
    if not holder:
      error = "Не введен владелец карты"
      flash(error)
    if not per_of_valid:
      error = "Не введен срок карты"
      flash(error)
    if not cvv:
      error = "Не введен секретный ключ карты"
      flash(error) 
    if error is None:
      confirmation = request.form['confirmation'] #спрашиваю подтверждение на перевод
      if confirmation == 'true':
        #транзакция подтверждена
        nomber_order= random.randint(000,999) 
        flash('Ваш заказ {} оформлен'.format(nomber_order))
        order = user.get_basket
        
        orders = database.get_db_connection()[database.COLLECTION_NAME]
        orders.insert(order.get_order_data())
        return jsonify(order = True,credentials = credentials, messages = get_flashed_messages())

        
      else:
        #вернуться на заполнение карты
        flash('Отмена')#возможно не нужно
        return jsonify(order = False,credentials = credentials, messages = get_flashed_messages())
        
# 
# scanf credit cart data
# 
# if true
#  =unique number
# push to BD log 
# print messeg
# else
#  print messeg



# debit = 1120 = 11.2p
# balans = debit - credit


#log data
#log old debit
#log old credit
#log new debit
#log new credit
#log type operetion: prihod\rashod\storno
#log coment\prichini

