
valide_recipients = [{"uuid": "1", "service": "whatsapp"},
                      {"uuid": "2", "service": "telegram"}]

valide_send_date = "2020-10-04 08:15:00"

valide_message = {"body": "Hello", "send_at": valide_send_date,
                "recipients": valide_recipients}


wrong_recipients = [{"uuid": 1, "service": "whatsapp"},
                      {"uuid": None, "service": "telegram"}]

wrong_messages = [{"body": 1, "send_at": valide_send_date,
                "recipients": valide_recipients},
                {"body": "".join(["i" for _ in range(801)]), "send_at": valide_send_date,
                "recipients": valide_recipients}]

wrong_send_date = "2020.10.04 08:15:00"
