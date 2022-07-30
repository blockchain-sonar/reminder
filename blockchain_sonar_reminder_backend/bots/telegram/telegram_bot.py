from threading import Event
from typing import Optional

from telegram import Chat, Message, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Handler, Updater
from telegram.utils.helpers import escape_markdown

from blockchain_sonar_reminder_backend.services.reminder import ReminderService
from blockchain_sonar_reminder_backend.utils.resources import render_template_message

class _TelegramMarkdownWrap:
	def __init__(self, wrap) -> None:
		assert not isinstance(wrap, dict)
		assert not isinstance(wrap, list)
		self._wrap = wrap

	def __getattr__(self, attr):
		thing = getattr(self._wrap, attr)
		if isinstance(thing, list): return [_TelegramMarkdownWrap(x) for x in thing]
		if isinstance(thing, dict): return map(lambda key: _TelegramMarkdownWrap(thing[key]), thing.keys())
		return _TelegramMarkdownWrap(thing)

	def __str__(self) -> str:
		return escape_markdown(str(self._wrap))

class TelegramBot:

	def __init__(self, reminder_service: ReminderService, telegram_token: str, webhook_url: Optional[str]) -> None:
		assert isinstance(reminder_service, ReminderService)
		assert isinstance(telegram_token, str)

		self._webhook_url = webhook_url

		self._updater = None
		self._reminder_service = reminder_service

		self._updater = Updater(token=telegram_token)
		
		start_handler = CommandHandler('start', self._start)
		self._updater.dispatcher.add_handler(start_handler)

		status_handler = CommandHandler('reminders', self._authorize(self._list_reminders))
		self._updater.dispatcher.add_handler(status_handler)

		# echo_handler = MessageHandler(Filters.text & (~Filters.command), self._message)
		# self._updater.dispatcher.add_handler(echo_handler)

		pass

	@property
	def underlaying_bot(self):
		return self._updater.bot

	@property
	def update_queue(self):
		return self._updater.update_queue

	def __enter__(self):
		webhook_url = self._webhook_url
		if webhook_url is None:
			# Using Telegram polling due webhook URL was not provided
			# TODO exclude for test/production zones
			self._updater.start_polling()
		else:
			# Using Telegram webhook for callbacks
			is_success_setup_webhook = self._updater.bot.set_webhook(webhook_url)
			if not is_success_setup_webhook:
				raise Exception("Failure to set Telegram webhook URL.")

			# Replace piece of logig from start_polling()
			self._updater.running = True
			self._updater.job_queue.start()
			dispatcher_ready = Event()
			self._updater._init_thread(self._updater.dispatcher.start, "dispatcher", ready=dispatcher_ready)
			dispatcher_ready.wait()

		return self

	def __exit__(self, type, value, traceback):
		self._updater.stop()
		pass

	def idle(self) -> None:
		self._updater.idle()

	def _start(self, update: Update, context: CallbackContext) -> None:
		context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a Blockchain Sonar's Reminder Bot, please talk to me!")

	# def _message(self, update: Update, context: CallbackContext) -> None:
	# 	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

	def _list_reminders(self, update: Update, context: CallbackContext) -> None:
		try:
			message = update.message
			bot_name = message.bot.name
			text = message.text

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

			context.bot.send_message(
				chat_id = update.effective_chat.id,
				reply_to_message_id = message.message_id,
				text = response_text,
				parse_mode = ParseMode.MARKDOWN
			)
		except Exception as ex:
			context.bot.send_message(
				chat_id = update.effective_chat.id,
				reply_to_message_id = message.message_id,
				text = str(ex)
			)
		pass

	def _authorize(self, handler: Handler) -> Handler:

		def authorize_handler(update: Update, context: CallbackContext) -> None:
			effective_chat: Chat = update.effective_chat
			current_chat: str = effective_chat.title
			if (effective_chat.type == Chat.PRIVATE):
				handler(update, context)
			else:
				message: Message = update.message
				context.bot.send_message(
					chat_id = update.effective_chat.id,
					reply_to_message_id = message.message_id,
					text = "Forbidden. Did your authorize? For group chat you have to authorize...",
					parse_mode = ParseMode.MARKDOWN
				)

		return authorize_handler

