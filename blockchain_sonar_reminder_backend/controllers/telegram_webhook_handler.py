from queue import Queue
from flask import Blueprint, Response, abort, request
from telegram import Bot, Update
from telegram.ext import ExtBot

class TelegramWebhookHandlerController(object):
	"""
	The class TelegramWebhookHandlerController implements Flask version of Telegram's WebhookHandler.
	See https://github.com/python-telegram-bot/python-telegram-bot/blob/v13.13/telegram/ext/utils/webhookhandler.py#L115-L177

	Responsibility of the controller are:
	- handle POST request
	- deserealize raw data
	- push Update into update_queue
	"""

	def __init__(self, bot: Bot, update_queue: Queue):
		self._bot = bot
		self._update_queue = update_queue

		self.blueprint = Blueprint('TelegramWebhookHandler', __name__)
		self.blueprint.add_url_rule('', methods=["POST"], view_func=self._handle_post)

	def _handle_post(self):
		# self.logger.debug('Webhook triggered')
		self._validate_post()
		data = request.get_json()
		# self.logger.debug('Webhook received data: %s', json_string)
		update = Update.de_json(data, self._bot)
		if update:
			# self.logger.debug('Received Update with ID %d on Webhook', update.update_id)
			# handle arbitrary callback data, if necessary
			if isinstance(self._bot, ExtBot):
				self._bot.insert_callback_data(update)
			self._update_queue.put(update)
		return Response(None, 200)

	def _validate_post(self) -> None:
		ct_header = request.headers.get("Content-Type", None)
		if ct_header != 'application/json':
			abort(403)
