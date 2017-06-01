import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '393548126:AAEgckYRm57w1VJldJEuvpUIE4F2CPEitTE'
WEBHOOK_URL = 'https://dd85d05c.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'usererror',
        'TNstate1',
        'TNstate2',
        'TNstate3',
        'TNerror1',
        'TNerror2',
        'NFstate1',
        'NFstate2',
        'NFstate3',
        'NFerror1',
        'NFerror2',
        'NFGCstate1',
        'NFGCstate2',
        'NFGCstate3',
        'NFGCerror1',
        'NFGCerror2'
    ],
    transitions=[
    	{
            'trigger': 'advance',
            'source': 'user',
            'dest': 'usererror',
            'conditions': 'is_going_to_usererror'
        },
        {
            'trigger': 'go_back',
            'source': 'usererror',
            'dest': 'user',
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'TNstate1',
            'conditions': 'is_going_to_TNstate1'
        },
        {
            'trigger': 'advance',
            'source': 'TNstate1',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': 'TNstate1',
            'dest': 'TNstate2',
            'conditions': 'is_going_to_TNstate2'
        },
        {
            'trigger': 'advance',
            'source': 'TNstate2',
            'dest': 'TNstate3',
            'conditions': 'is_going_to_TNstate3'
        },
        {
            'trigger': 'TNback1',
            'source': 'TNstate3',
            'dest': 'TNstate1',
        },
        {
            'trigger': 'advance',
            'source': 'TNstate1',
            'dest': 'TNerror1',
            'conditions': 'is_going_to_TNerror1'
        },
        {
            'trigger': 'TNback1',
            'source': 'TNerror1',
            'dest': 'TNstate1',
        },
        {
            'trigger': 'advance',
            'source': 'TNstate2',
            'dest': 'TNerror2',
            'conditions': 'is_going_to_TNerror2'
        },
        {
            'trigger': 'TNback2',
            'source': 'TNerror2',
            'dest': 'TNstate2',
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'NFstate1',
            'conditions': 'is_going_to_NFstate1'
        },
        {
            'trigger': 'advance',
            'source': 'NFstate1',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': 'NFstate1',
            'dest': 'NFstate2',
            'conditions': 'is_going_to_NFstate2'
        },
        {
            'trigger': 'advance',
            'source': 'NFstate2',
            'dest': 'NFstate3',
            'conditions': 'is_going_to_NFstate3'
        },
        {
            'trigger': 'NFback1',
            'source': 'NFstate3',
            'dest': 'NFstate1',
        },
        {
            'trigger': 'advance',
            'source': 'NFstate1',
            'dest': 'NFerror1',
            'conditions': 'is_going_to_NFerror1'
        },
        {
            'trigger': 'NFback1',
            'source': 'NFerror1',
            'dest': 'NFstate1',
        },
        {
            'trigger': 'advance',
            'source': 'NFstate2',
            'dest': 'NFerror2',
            'conditions': 'is_going_to_NFerror2'
        },
        {
            'trigger': 'NFback2',
            'source': 'NFerror2',
            'dest': 'NFstate2',
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'NFGCstate1',
            'conditions': 'is_going_to_NFGCstate1'
        },
        {
            'trigger': 'advance',
            'source': 'NFGCstate1',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        {
            'trigger': 'advance',
            'source': 'NFGCstate1',
            'dest': 'NFGCstate2',
            'conditions': 'is_going_to_NFGCstate2'
        },
        {
            'trigger': 'advance',
            'source': 'NFGCstate2',
            'dest': 'NFGCstate3',
            'conditions': 'is_going_to_NFGCstate3'
        },
        {
            'trigger': 'NFGCback1',
            'source': 'NFGCstate3',
            'dest': 'NFGCstate1',
        },
        {
            'trigger': 'advance',
            'source': 'NFGCstate1',
            'dest': 'NFGCerror1',
            'conditions': 'is_going_to_NFGCerror1'
        },
        {
            'trigger': 'NFGCback1',
            'source': 'NFGCerror1',
            'dest': 'NFGCstate1',
        },
        {
            'trigger': 'advance',
            'source': 'NFGCstate2',
            'dest': 'NFGCerror2',
            'conditions': 'is_going_to_NFGCerror2'
        },
        {
            'trigger': 'NFGCback2',
            'source': 'NFGCerror2',
            'dest': 'NFGCstate2',
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
