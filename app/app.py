
# external modules
from flask import Flask, request, jsonify, make_response

# project modules
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

    """
    View for sending message

    Required message in request.json

    """

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

    """ View for getting deffered messages """

    return jsonify(postman.get_scheduled())


@app.route("/delete_all", methods=["DELETE"])
@auth.login_required
def delete_all():

    """ View for deleting all finshed jobs (including failed) """

    return jsonify(postman.delete_all())


@app.route("/get_finished", methods=["GET"])
@auth.login_required
def get_finished():

    """ View for getting ALL finished jobs (including failed) """

    return jsonify(postman.get_finished())
