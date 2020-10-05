""" Executable module of message_sender app """

from app.app import app

if __name__ == "__main__":
    # set debug to False
    app.run(host="0.0.0.0", debug=True)
