from random import randint

class Messenger:

    def send_message(self, message):
        if randint(1, 2) == 2:
            raise ValueError("Problem -----------")
        return message

    def check_progress(self, job_id):
        return {"job": job_id, "status": "success"}
