from flask import Flask, request
import redis
from rq import Queue

app = Flask("message_sender")
