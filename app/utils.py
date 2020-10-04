from datetime import datetime
from rq import requeue_job

import time

class Validator:

    """
    Class for validating message
    """

    def validate(self, message):
        if not isinstance(message.get("body"), str):
            raise TypeError ("Body of the message must be string")
        if len(message.get("body")) > 800:
            raise ValueError ("Max lenght of the message is 800")

        if send_at := message.get("send_at"):
            self.validate_send_at(send_at)

        valide_recip = self.validate_recipients(message.get("recipients"))
        message["recipients"] = [r for r in valide_recip if r]
        return message

    def validate_recipients(self, recipients):
        if not isinstance(recipients, list):
            raise TypeError ("Recipients of the message must be list of dicts")

        return list(map(self.validate_recipient, recipients))

    def validate_recipient(self, recipient):
        if not isinstance(recipient, dict):
            raise TypeError ("Recipient of the message must be a dict")
        if not isinstance(recipient.get("service"), str):
            raise TypeError ("Service parameter must be a str")
        if not isinstance(recipient.get("uuid"), str):
            raise TypeError ("UUID parameter must be a str")
        return recipient

    def validate_send_at(self, send_at):
        if not isinstance(send_at, str):
            raise TypeError ("send_at parameter must be a str")
        formate_string = "%Y-%m-%d %H:%M:%S"
        datetime.strptime(send_at, formate_string)
        return send_at


class Postman:

    def __init__(self, main_queue, resend_queue, messengers, scheduler):
        self.main_queue = main_queue
        self.resend_queue = resend_queue
        self.messengers = messengers
        self.scheduler = scheduler

    def send_message(self, message):
        jobs = []
        for messenger in message["recipients"]:
            service = self.messengers.get(messenger.get("service"))
            if not service:
                raise ValueError ("Unknown messenger!!!")

            send_job = self.main_queue.enqueue(service.send_message,
                                     args=[message],
                                     exc_handler=self.job_exception_handler)
            time.sleep(5)
            # success_job = self.main_queue.enqueue(self.on_success, self, depends_on=send_job)

        return send_job.result

    def job_exception_handler(self, job, exc_type, exc_value, traceback):
        return exc_type

    def retry_job(self, job):
        pass

    def on_success(self):
        return {"status": 200, "message": "success"}

def say_hello():
    return "Hello"
