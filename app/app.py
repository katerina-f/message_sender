
#
from flask import Flask, request, jsonify, make_response
from .utils import Validator, Postman
from .messengers import Telegram, Viber, WhatsApp
from .authorized import auth


app = Flask("message_sender")

# create instances
validator = Validator()
postman = Postman({"viber": Viber(), "whatsapp": WhatsApp(), "telegram": Telegram()})

@app.route("/send_message", methods=["POST"])
@auth.login_required
def send_message():
    if not request.json:
        return make_response(jsonify({'error': "Message required!!!"}), 400)

    try:
        message = validator.validate(request.json)
        return jsonify(postman.send_message(message))
    except (TypeError, ValueError) as err:
        return make_response(jsonify({'error': str(err)}), 400)


@app.route("/get_scheduled", methods=["GET"])
@auth.login_required
def get_scheduled():
    return jsonify(postman.get_scheduled())


@app.route("/delete_all", methods=["DELETE"])
@auth.login_required
def delete_all():
    return jsonify(postman.delete_all())


@app.route("/get_finished", methods=["GET"])
@auth.login_required
def get_finished():
    return jsonify(postman.get_finished())
