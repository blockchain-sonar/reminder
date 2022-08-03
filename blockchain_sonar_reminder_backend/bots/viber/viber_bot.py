import threading
from urllib.parse import quote, ParseResult
from chevron import render
from blockchain_sonar_reminder_backend.services.reminder import ReminderService
from blockchain_sonar_reminder_backend.utils.resources import render_message, render_template_message

from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

viber = Api(BotConfiguration(
	name='Oleg Reminder Bot',
	avatar='http://site.com/avatar.jpg',
	auth_token='4f912f3262a7e3a7-ad5fec7947a3f090-8be63ffab7a8e7a9'
))

def activate_lazy_set_webhook_job():
	def run_job():
		time.sleep(3)
		viber.set_webhook('https://1d60-5-53-113-77.eu.ngrok.io')

	thread = threading.Thread(target=run_job)
	thread.start()

@app.route('/', methods=['POST'])
def incoming():
	if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
		return Response(status=403)

	# this library supplies a simple way to receive a request object
	viber_request = viber.parse_request(request.get_data())

	if isinstance(viber_request, ViberConversationStartedRequest):
		message = "I'm a Blockchain Sonar's Reminder Bot, please talk to me!"
		viber.send_messages(viber_request.sender.id, [message])
	elif isinstance(viber_request, ViberSubscribedRequest):
		viber.send_messages(viber_request.get_user.id, [
			TextMessage(text="thanks for subscribing!")
		])
	elif isinstance(viber_request, ViberFailedRequest):
		logger.warn("client failed receiving message. failure: {0}".format(viber_request))

	if isinstance(viber_request, ViberMessageRequest):
		if viber_request.message == "/reminders":
			viber.send_messages(viber_request.sender.id, [
			_list_reminders()
		])
		
	elif isinstance(viber_request, ViberFailedRequest):
		logger.warn("client failed receiving message. failure: {0}".format(viber_request))

	return Response(status=200)

def _list_reminders() -> None:
	try:
		render_context: list = {
			"remiders":[
				{
					"tag": "Ololo 1"
				},
				{
					"tag": "Ololo 2"
				}
			]
		}

		response_text: str = render_template_message(__name__, "reminders.mustache.txt", render_context)
		return response_text
	except Exception as ex:
		return ex
	pass

if __name__ == "__main__":
	activate_lazy_set_webhook_job()
	app.run(host='127.0.0.1', port=8080, debug=False)
