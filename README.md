# Message Sender

This application-template for sending messages to popular instant messengers (Viber, Telegram, WhatsApp) without integration with services

## Getting Started

### Set the .env file

See the **.env.example** file and create **.env** in a root directory

### Change the docker-compose file

In docker-compose file change the password for redis to REDIS_PASSWORD from env

```
...
services:
  redis:
    container_name: redis
    image: redis:alpine
    command: redis-server --requirepass sOmE_sEcUrE_pAsS #here
    ports:
...
```
And set TimeZone to your TimeZone

```
...
    environment:
        - REDIS_REPLICATION_MODE=master
        - TZ=Europe/Moscow #here
...
```
### Instalation

To install and run the code in the docker containers,
make script
```
run.sh
```
executable
```
chmod +x ./run.sh
```

This script will start building the redis service and our application.

and run it in the project root
```
./run.sh
```

#### Tests

To running tests execute
```
python -m unittest -v tests/*.py
```
in the project root

## Examples for API

#### POST (upload)

ATTENTION! date has only one acceptable format - "2020-10-05 13:48:00"

```
curl -i -X POST \
        -H "Content-Type: application/json"  0.0.0.0:5000/send_message \
        -d '{"body": "Hello", "send_at": "2020-10-05 13:48:00",
                "recipients": [{"uuid": "1", "service": "whatsapp"},
                      {"uuid": "2", "service": "telegram"}]}' \
        -u username:password
```

Returns lists of scheduled and currently started jobs

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 129
Server: Werkzeug/1.0.1 Python/3.8.6
Date: Mon, 05 Oct 2020 14:57:35 GMT

{
  "scheduled": [],
  "started": [
      "Message to user: 2 with body: Hello Queued at 2020-10-06 07:45:55 to messenger: telegram",
      "Message to user: 1 with body: Hello Queued at 2020-10-06 07:45:55 to messenger: whatsapp"
  ]
}
```

Returns error message and 401 code if unauthorized

```
HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 37
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/1.0.1 Python/3.8.6
Date: Mon, 05 Oct 2020 14:53:52 GMT

{
  "error": "Unauthorized access"
}
```

Returns error message and 400 code if you sent a wrong data

```
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/1.0.1 Python/3.8.6
Date: Mon, 05 Oct 2020 15:01:46 GMT

{
  "error": "Date must be in a future!"
}
```

#### GET

##### Get all scheduled messages

```
curl -i  -X GET 0.0.0.0:5000/get_scheduled -u username:password
```

 Returns list of scheduled messages and 200 code

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 22
Server: Werkzeug/1.0.1 Python/3.8.6
Date: Mon, 05 Oct 2020 15:04:49 GMT

{
  "scheduled": [
    "Message to user: 2 with body: Hi Queued at 2020-10-06 07:45:55 to messenger: telegram",
    "Message to user: 1 with body: Hi Queued at 2020-10-06 07:45:55 to messenger: telegram"
  ]
}
```

##### Get all finished sendings

```
curl -i  -X GET 0.0.0.0:5000/get_scheduled -u username:password
```

Returns list of ALL finished processes and 200 code

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 431
Server: Werkzeug/1.0.1 Python/3.8.6
Date: Mon, 05 Oct 2020 15:07:30 GMT

{
  "finished_main": [
    "Message to user: 1 with body: Buy Queued at 2020-10-06 07:37:17 to messenger: whatsapp",
    "Message to user: 1 with body: Buy Queued at 2020-10-04 07:37:17 to messenger: whatsapp",
    "Message to user: 2 with body: Hello Queued at 2020-10-06 07:45:55 to messenger: telegram",
    "Message to user: 1 with body: Hello Queued at 2020-10-06 07:45:55 to messenger: telegram"
  ],
  "finished_scheduled": [
    "Message to user: 2 with body: Buy Queued at 2020-10-05 07:45:55 to messenger: telegram",
    "Message to user: 1 with body: Buy Queued at 2020-10-05 07:45:55 to messenger: telegram",
  ],
  "finished_with_fail": []
}
```
#### DELETE

Delete all finished and failed messages in queues and in memory

```
curl -i -X DELETE 0.0.0.0:5000/delete_all -u username:password
```

Returns success message

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 10
Server: Werkzeug/1.0.1 Python/3.8.6
Date: Mon, 05 Oct 2020 15:18:14 GMT

"Success"
```

## Technology Stack

##### Flask

A simple and lightweight framework that allows you to quickly create an API without unnecessary configurations

##### Redis

A very fast and easy alternative to heavy and slow databases, ideal for a message broker

##### RQ (redis queue)

Excellent message queuing library for Redis

- Priority queues. RQs priority queue model is simple and efficient - workers read from queues in order
- The RQ api is simple.
- flexible configuration of queue parameters
- before worker's death it's wait until the currently running task is finished, stop the work loop and gracefully register its own death.
- all unfinished (and completed) tasks are kept in memory until the timeout expires


## Authors

* **Katerina Frolova** - *Initial work* - [katerina-f](https://github.com/katerina-f)
