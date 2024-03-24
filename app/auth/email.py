import time
import jwt
import smtplib

from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('HASHING_ALGORITHM')
EMAIL_TOKEN_LIFETIME = config('EMAIL_TOKEN_LIFETIME', cast=int)
EMAIL_USERNAME=config('EMAIL_USERNAME')
SMTP_SERVER=config('SMTP_SERVER')
SMTP_SERVER_PORT=config('SMTP_SERVER_PORT',cast=int)
EMAIL_PASSWORD=config('EMAIL_PASSWORD')



async def decode_reset_password_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = decoded_token.get("expires", 0)
        if expiration_time >= time.time():
            return decoded_token
        else:
            return None
    except:
        return None


async def send_verification_email(email:str,user_id:str):
    payload = {
        'email':email,
        'user_id':user_id,
        'expires':time.time() + EMAIL_TOKEN_LIFETIME * 24 * 60* 60
    }
    token = jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)

    path='templates/verification_email.html'
    with open(path, 'r') as file:
        html_content = file.read()
    
    html_content_with_token = html_content.replace('{{token}}', token)

    msg = MIMEMultipart()
    msg['From'] = 'temirlan.kazhigerey@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'GIVEME.kz Account Activation'
    msg.attach(MIMEText(html_content_with_token,'html'))


    try:
        with smtplib.SMTP(SMTP_SERVER,SMTP_SERVER_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USERNAME,EMAIL_PASSWORD)
            smtp.send_message(msg)

    except Exception as e:
        error_message = f"Failed to send email: {str(e)}"
        print(error_message)
        return {'error': error_message}
    

def forget_password_request(email:str):
    payload = {
        'email':email,
        'expires':time.time() + EMAIL_TOKEN_LIFETIME * 24 * 60* 60
    }
    forget_password_token = jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    
    path = 'templates/forget_password_link.html'
    with open(path,'r') as html_file:
        html_content = html_file.read()
    html_with_token=html_content.replace('{{token}}',forget_password_token)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = email
    msg['Subject'] = 'GIVEME.kz Forget Password Request'
    msg.attach(MIMEText(html_with_token,'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER,SMTP_SERVER_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USERNAME,EMAIL_PASSWORD)
            smtp.send_message(msg)
    except:
        return {'error':'Failed to send email'}
    return {'success': True}
