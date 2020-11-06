from threading import Thread

from flask_mail import Message


def _send_async_email(app,msg):
    from index import mail
    with app.app_context():
        mail.send(msg)

def send_mail(app,owner,address):

    msg = Message(owner+'的服务器挂掉了',sender='546536968@qq.com' ,recipients=['546536968@qq.com'])
    msg.body = owner+'服务器挂掉了,地址是'+address
    thread = Thread(target=_send_async_email,args=[app,msg])
    thread.start()
    print('邮件已发送')
    return thread