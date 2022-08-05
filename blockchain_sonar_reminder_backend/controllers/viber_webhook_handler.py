from email import message
from queue import Queue
from flask import Blueprint, Response, abort, request

from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from blockchain_sonar_reminder_backend.bots.viber.viber_bot import ViberBot

class ViberWebhookHandlerController(object):
	"""
	The class TelegramWebhookHandlerController implements Flask version of Telegram's WebhookHandler.
	See https://github.com/python-telegram-bot/python-telegram-bot/blob/v13.13/telegram/ext/utils/webhookhandler.py#L115-L177

	Responsibility of the controller are:
	- handle POST request
	- deserealize raw data
	- push Update into update_queue
	"""

	def __init__(self, bot: ViberBot):
		self._bot = bot

		self.blueprint = Blueprint('ViberWebhookHandler', __name__)
		self.blueprint.add_url_rule('', methods=["POST"], view_func=self._handle_post)

	def _handle_post(self):
		if not self._bot.underlaying_bot.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
			return Response(status=403)

		# this library supplies a simple way to receive a request object
		viber_request = self._bot.underlaying_bot.parse_request(request.get_data())

		if isinstance(viber_request, ViberConversationStartedRequest):
			message = "I'm a Blockchain Sonar's Reminder Bot, please talk to me!"
			self._bot.underlaying_bot.send_messages(viber_request.sender.id, [message])
		elif isinstance(viber_request, ViberSubscribedRequest):
			self._bot.underlaying_bot.send_messages(viber_request.get_user.id, [
				TextMessage(text="thanks for subscribing!")
			])
		elif isinstance(viber_request, ViberFailedRequest):
			#logger.warn("client failed receiving message. failure: {0}".format(viber_request))
			pass

		if isinstance(viber_request, ViberMessageRequest):
			self._bot.onmessage(viber_request)
			
			
		elif isinstance(viber_request, ViberFailedRequest):
			#logger.warn("client failed receiving message. failure: {0}".format(viber_request))
			pass


		return Response(None, 200)

	def _validate_post(self) -> None:
		ct_header = request.headers.get("Content-Type", None)
		if ct_header != 'application/json':
			abort(403)
