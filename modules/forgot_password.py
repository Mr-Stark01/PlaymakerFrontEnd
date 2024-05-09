import smtplib
#SERVER = "localhost"

def send_forgot(email):
    FROM = 'playmaker@noreply.com'
    TO = [email]
    SUBJECT = "Hello ! bellow you can find your forgotten password"

    