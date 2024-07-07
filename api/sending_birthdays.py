from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

import settings
from db.dals.alertDal import AlertDAL
import datetime
import asyncio


engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

def smtp(email, data):
    from_mail = settings.Email
    from_passwd = settings.EmailPassword
    smtp_server_adr = "smtp.mail.ru"
    to_mail = email

    msg = MIMEMultipart()
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Subject"] = Header('Напоминание о предстоящих днях рождениях', 'utf-8')
    msg["Date"] = formatdate(localtime=True)

    message_text = "Напоминаем Вам о предстоящих днях рождениях:\n\n"

    for info in data:
        fullname, birthday, user_email = info
        birthday_str = birthday.strftime('%d.%m.%Y')
        message_text += f"- {fullname}, {birthday_str} - {user_email}\n"

    message_text += "\n\nМожете написать им поздравление на нашем сайте - http://localhost:3000"

    msg.attach(MIMEText(message_text, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(smtp_server_adr, 465) as smtp:
            smtp.login(from_mail, from_passwd)
            smtp.sendmail(from_mail, to_mail, msg.as_string())
        print(f"Письмо успешно отправлено на {to_mail}")
    except Exception as e:
        print(f"Ошибка при отправке письма на {to_mail}: {e}")

async def get_alert():
    db = asyncSession()
    alert_ids = []
    try:
        async with db.begin() as tx:
            alert_dal = AlertDAL(db)
            date_now = datetime.datetime.now().date()
            alerts = await alert_dal.get_alert_by_date(date=date_now)

            email_data = {}
            current_date = datetime.date.today()
            current_year = current_date.year

            for alert in alerts:
                alert_ids.append(alert.id)
                user_email = alert.user.email
                followed_user_info = (
                    alert.followed_user.fullname,
                    alert.followed_user.date_of_birthday.replace(year=current_year),
                    alert.followed_user.email
                )

                if user_email not in email_data:
                    email_data[user_email] = []

                email_data[user_email].append(followed_user_info)

            for email in email_data:
                smtp(email, email_data[email])
        if alert_ids != []:
            async with db.begin() as tx:
                alert_dal_new = AlertDAL(db)
                await alert_dal_new.update_alert_dates(ids=alert_ids)

    except Exception as e:
        print(f"Ошибка при выполнении операций с базой данных: {e}")




async def main():
    await get_alert()

if __name__ == "__main__":
    asyncio.run(main())