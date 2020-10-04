from flask import Flask, request, abort, jsonify
from flask_restful import Api
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from .utils import Validator, Postman, say_hello
from .telegram import Telegram
from .viber import Viber
from .whatsapp import WhatsApp
from .authorized import auth
from .config import REDIS_PASSWORD

import time

app = Flask("message_sender")
api = Api(app)

# create redis connections
redis_conn = Redis(host="redis", port="6379", password="sOmE_sEcUrE_pAsS")
main_queue = Queue("medium", connection=redis_conn)
resend_queue = Queue("high", connection=redis_conn)
scheduler = Scheduler(connection=redis_conn)

# create instances
validator = Validator()
postman = Postman(main_queue, resend_queue,
                 {"viber": Viber, "whatsapp": WhatsApp, "telegram": Telegram},
                 scheduler)

@app.route("/message", methods=["POST"])
@auth.login_required
def send_message():
    if not request.json:
        abort(400)

    job = main_queue.enqueue(say_hello)
    time.sleep(2)
    return jsonify(job.get_status())
    try:
        message = validator.validate(request.json)
        return jsonify(postman.send_message(message))
    except (TypeError, ValueError) as err:
        abort(400, str(err))
