from time import time
from django.db import connection

def clear_session_data():
    expiry_time = int(time())
    cursor = connection.cursor()
    cursor.execute("DELETE FROM app_sessiondata WHERE expiry_time < %s",[expiry_time])
    cursor.fetchone()

def clear_qr_requests():
    expiry_time = int(time())
    cursor = connection.cursor()
    cursor.execute("DELETE FROM app_requestqr WHERE expiry_time < %s",[expiry_time])
    cursor.fetchone()