from threading import Event
import threading
import time
from typing import Optional

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage

from blockchain_sonar_reminder_backend.services.reminder import ReminderService
from blockchain_sonar_reminder_backend.utils.resources import render_template_message
from viberbot.api.viber_requests import ViberMessageRequest

class ViberBot:

	def __init__(self, reminder_service: ReminderService, viber_token: str, webhook_url: Optional[str], bot_name: str, avatar_link: str) -> None:
		assert isinstance(reminder_service, ReminderService)
		assert isinstance(viber_token, str)

		self._webhook_url = webhook_url

		self._viber_api = Api(BotConfiguration(
			name=bot_name,
			avatar=avatar_link,
			auth_token=viber_token
		))

		self._reminder_service = reminder_service

	def __enter__(self):
		def activate_lazy_set_webhook_job():
			def run_job():
				time.sleep(3)
				self._viber_api.set_webhook(self._webhook_url)

			thread = threading.Thread(target=run_job)
			thread.start()

		activate_lazy_set_webhook_job()
		return self

	def __exit__(self, type, value, traceback):
		#self._updater.stop()
		pass

	@property
	def underlaying_bot(self):
		return self._viber_api
	
	def onmessage(self, viber_request: ViberMessageRequest) -> None:
		if isinstance(viber_request, ViberMessageRequest):
			if viber_request.message.text == "/reminders":
				message_text: str = self._list_reminders(viber_request)
				self._viber_api.send_messages(viber_request.sender.id, [
					TextMessage(text = message_text)
				])
			else:
				self._viber_api.send_messages(viber_request.sender.id, [TextMessage(text ="Unsupported command")])
				raise Exception("Unsupported command: %s" % viber_request.message)
		else:
			raise Exception("Failed receiving message")

	def _list_reminders(self, viber_request: ViberMessageRequest) -> None:
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
			text = str(ex)
			return text

