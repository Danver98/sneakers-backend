from flask import request, Blueprint,flash,redirect,url_for,render_template,get_flashed_messages
import random 
bp = Blueprint('author',__name__,url_prefix='/author')

@bp.route('/card_entry/',method = ['POST'])
def card_entry():
  if request.method == 'POST':
    nomber_card = request.form['nomber_card']
    holder = request.form['holder']
    per_of_valid = request.form['per_of_valid']
    cvv = request.form['cvv']
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
        return redirect(url_for('main_page'))
      else:
        #вернуться на заполнение карты
        flash('Отмена')#возможно не нужно
        return render_template('auth/card_entry.html', credentials = credentials , messages = get_flashed_messages)
        #возможно ошибки        ^^^^ 

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

