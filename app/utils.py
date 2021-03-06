# internal modules
from datetime import datetime, timedelta
import json

# external modules
from redis import Redis
from rq import Retry, Queue
from rq.job import Job

# project modules
from .config import REDIS_PASSWORD, \
                    RETRY_COUNT, \
                    RETRY_INTERVAL, \
                    DELETE_FAILED_TIMEOUT, \
                    DELETE_FINISHED_TIMEOUT


class Validator:

    """
    Class for validating message
    """

    def validate(self, message):

        """ Main method of validate an incoming message """

        if not isinstance(message.get("body"), str):
            raise TypeError ("Body of the message must be string")
        if len(message.get("body")) > 800:
            raise ValueError ("Max lenght of the message is 800")

        if send_at := message.get("send_at"):
            message["send_at"] = self.validate_send_at(send_at)

        valide_recip = self.validate_recipients(message.get("recipients"))
        message["recipients"] = [r for r in valide_recip if r]
        return message

    def validate_recipients(self, recipients):

        """ Method of validate recipients """

        if not isinstance(recipients, list):
            raise TypeError ("Recipients of the message must be list of dicts")

        # removing dublicates
        sorted_list = set(list(json.dumps(rec, sort_keys=True) for rec in recipients))
        return list(map(self.validate_recipient, [json.loads(rec) for rec in sorted_list]))

    def validate_recipient(self, recipient):

        """ Method of validate one recipient """

        if not isinstance(recipient, dict):
            raise TypeError ("Recipient of the message must be a dict")
        if not isinstance(recipient.get("service"), str):
            raise TypeError ("Service parameter must be a str")
        if not isinstance(recipient.get("uuid"), str):
            raise TypeError ("UUID parameter must be a str")
        return recipient

    def validate_send_at(self, send_at):

        """ Method of validate send date """

        if not isinstance(send_at, str):
            raise TypeError ("send_at parameter must be a str")
        formate_string = "%Y-%m-%d %H:%M:%S"

        send_at = datetime.strptime(send_at, formate_string)

        if send_at < datetime.now() + timedelta(minutes=2):
            raise ValueError ("Date must be in a future!")

        return send_at


class Postman:

    """
    Class for sending messages and checking their statuses
    """

    def __init__(self, messengers):
        self.messengers = messengers
        # create redis connection
        self.redis_conn = Redis(host="redis", port="6379", password=REDIS_PASSWORD)

        # create queues
        self.main_queue = Queue("medium", connection=self.redis_conn,
                                failed_ttl=DELETE_FAILED_TIMEOUT,
                                default_timeout=DELETE_FINISHED_TIMEOUT)
        self.check_queue = Queue("check", connection=self.redis_conn,
                                failed_ttl=DELETE_FAILED_TIMEOUT,
                                default_timeout=DELETE_FINISHED_TIMEOUT)
        self.scheduled_queue = Queue("scheduled", connection=self.redis_conn,
                                    failed_ttl=DELETE_FAILED_TIMEOUT,
                                    default_timeout=DELETE_FINISHED_TIMEOUT)

    def send_message(self, message):

        """
        Method for sending messages for specific messengers using queues

        :param message: dict object
        format is {"body": "Hello",
                   "send_at": "2020-10-04 08:15:00",
                   "recipients": [
                       {"uuid": 1, "service": "whatsapp"},
                       {"uuid": None, "service": "telegram"}
                   ]}
        """
        started_jobs = []
        scheduled = []
        for messenger in message["recipients"]:
            service = self.messengers.get(messenger.get("service"))
            if not service:
                raise ValueError ("Unknown messenger!!!")

            queued = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

            description = (f"Message to user: {messenger.get('uuid')} with body: {message.get('body')} "
                    f"Queued at {queued} to messenger: {messenger.get('service')}")

            if message.get("send_at"):
                scheduled_send_job = self.scheduled_queue.enqueue_at(message.get("send_at"),
                                               service.send_message,
                                               message,
                                               retry=Retry(max=RETRY_COUNT, interval=RETRY_INTERVAL),
                                               description=description)
                scheduled.append(scheduled_send_job.description)
            else:
                send_job = self.main_queue.enqueue(service.send_message,
                                                   message,
                                                   retry=Retry(max=RETRY_COUNT, interval=RETRY_INTERVAL),
                                                   description=description)

                started_jobs.append(send_job.description)

        result = {"started": started_jobs, "scheduled": scheduled}
        return result

    def get_scheduled(self):

        """ Deffered message search method """

        scheduled = self.__get_jobs_descriptions(self.scheduled_queue.scheduled_job_registry.get_job_ids())
        return {"scheduled": scheduled}

    def get_finished(self):

        """ Finished jobs (message) search method """

        finished_scheduled = self.__get_jobs_descriptions(self.scheduled_queue.finished_job_registry.get_job_ids())
        finished_main = self.__get_jobs_descriptions(self.main_queue.finished_job_registry.get_job_ids())
        finished_with_fail = self.__get_jobs_descriptions(self.main_queue.failed_job_registry.get_job_ids() +
                self.scheduled_queue.failed_job_registry.get_job_ids())

        return {"finished_scheduled": finished_scheduled,
                "finished_main": finished_main,
                "finished_with_fail": finished_with_fail}

    def delete_all(self):

        """ Finished jobs (message) delete method """

        self.main_queue.empty()
        self.scheduled_queue.empty()
        self.check_queue.empty()

        for j in self.main_queue.failed_job_registry.get_job_ids():
            self.main_queue.failed_job_registry.remove(j)

        for j in self.scheduled_queue.failed_job_registry.get_job_ids():
            self.scheduled_queue.failed_job_registry.remove(j)

        for j in self.main_queue.finished_job_registry.get_job_ids():
            self.main_queue.finished_job_registry.remove(j)

        for j in self.scheduled_queue.finished_job_registry.get_job_ids():
            self.scheduled_queue.finished_job_registry.remove(j)

        return "Success"

    def __get_jobs_descriptions(self, jobs):

        """ Jobs (message) descriptions search method """

        jobs = Job.fetch_many(jobs, connection=self.redis_conn)
        return [job.description for job in jobs]
