# internal modules
from datetime import datetime, timedelta
import json
import time
from unittest import TestCase, main
from unittest.mock import Mock, MagicMock, patch, call, create_autospec

# external modules
from fakeredis import FakeStrictRedis
from redis import Redis
from rq import SimpleWorker, Queue

# project modules
from app import *
from .test_data import *


class TestPostman(TestCase):

    def setUp(self):
        redis_conn = FakeStrictRedis()
        # create queues
        main_queue = Queue("test_medium", connection=redis_conn,
                                failed_ttl=DELETE_FAILED_TIMEOUT,
                                default_timeout=DELETE_FINISHED_TIMEOUT)
        scheduled_queue = Queue("test_scheduled", connection=redis_conn,
                                    failed_ttl=DELETE_FAILED_TIMEOUT,
                                    default_timeout=DELETE_FINISHED_TIMEOUT)
        self.worker = SimpleWorker([main_queue, scheduled_queue],
                               connection=main_queue.connection)

        self.postman = Postman({"viber": Viber(), "whatsapp": WhatsApp(), "telegram": Telegram()})
        self.postman.redis_conn = redis_conn
        self.postman.scheduled_queue = scheduled_queue
        self.postman.main_queue = main_queue

    def tearDown(self):
        self.postman.main_queue.empty()
        self.postman.main_queue.delete(delete_jobs=True)
        self.postman.scheduled_queue.empty()
        self.postman.scheduled_queue.delete(delete_jobs=True)

    def test_send_message_with_failure(self):
        with self.assertRaises(ValueError):
            self.postman.send_message(wrong_messages[1])

        job = self.postman.main_queue.enqueue(fail_job)
        self.worker.work(burst=True)
        self.assertEqual(len(self.postman.main_queue.failed_job_registry.get_job_ids()), 1)
        self.assertEqual(self.postman.main_queue.failed_job_registry.get_job_ids()[0], job.id)

    def test_send_scheduled_message(self):
        result = self.postman.send_message(valide_message_for_postman)
        self.assertEqual(len(self.postman.scheduled_queue.scheduled_job_registry.get_job_ids()), 2)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result["scheduled"]), 2)
        self.assertListEqual(result["scheduled"], ['Message to user: 1 with body: Hello', 'Message to user: 2 with body: Hello'])

    def test_send_message_with_success(self):
        result = self.postman.send_message(valide_message_for_success_postman)
        self.assertListEqual(result["started"], ['Message to user: 1 with body: Hello', 'Message to user: 2 with body: Hello'])

    def test_get_scheduled(self):
        result = self.postman.send_message(valide_message_for_postman)
        scheduled = self.postman.get_scheduled()
        self.assertEqual(sorted(result["scheduled"]), sorted(scheduled["scheduled"]))
