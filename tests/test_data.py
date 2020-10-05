# internal modules
from datetime import datetime, timedelta


valide_recipients = [{"uuid": "1", "service": "whatsapp"},
                      {"uuid": "2", "service": "telegram"}]


valide_send_date = datetime.strftime(datetime.now() + timedelta(minutes=30), "%Y-%m-%d %H:%M:%S")


valide_message = {"body": "Hello", "send_at": valide_send_date,
                "recipients": valide_recipients}


wrong_recipients = [{"uuid": 1, "service": "whatsapp"},
                      {"uuid": None, "service": "telegram"}]


wrong_messages = [{"body": 1, "send_at": valide_send_date,
                "recipients": valide_recipients},
                {"body": "".join(["i" for _ in range(801)]), "send_at": valide_send_date,
                "recipients": [{"uuid": 1, "ser": "whatsapp"}]}]


wrong_send_date = "2020.10.04 08:15:00"


valide_message_for_postman = {"body": "Hello",
                              "send_at": datetime.now() + timedelta(days=2),
                              "recipients": valide_recipients}


valide_message_for_success_postman = {"body": "Hello",
                              "recipients": valide_recipients}


def fail_job():
    return 1/0


def success_job():
    return True
