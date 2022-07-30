#
# Application Factory.
# See for details https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/#basic-factories
#

from typing import Optional
from flask import Flask, Response
from werkzeug.exceptions import HTTPException

import os

from blockchain_sonar_reminder_backend.bots.telegram.telegram_bot import TelegramBot

from blockchain_sonar_reminder_backend.controllers.static import StaticController
from blockchain_sonar_reminder_backend.controllers.telegram_webhook_handler import TelegramWebhookHandlerController

from blockchain_sonar_reminder_backend.services.reminder import ReminderService

from .version import __version__

def create_app():
	print("%s v%s" % (__name__, __version__))

	app = Flask(__name__, static_folder=None)
	
	# https://stackoverflow.com/a/54151093/2011679
	app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

	app.config.from_prefixed_env("BSR")

	#
	# Parse/validate configuration
	#
	callback_base_url: Optional[str] = app.config.get("CALLBACK_BASE_URL")
	telegram_bot_token: Optional[str] = app.config.get("TELEGRAMBOT_TOKEN")

	if telegram_bot_token is None:
		raise Exception("TELEGRAMBOT_TOKEN was not provided")

	telegram_bot_webhook_url = None
	telegram_bot_webhook_url_prefix = None
	if callback_base_url is not None:
		telegram_bot_webhook_url_prefix = "/webhook/telegram"
		telegram_bot_webhook_url = callback_base_url + telegram_bot_webhook_url_prefix

	#
	# Instantiate application members
	#
	reminder_service = ReminderService()
	telegram_bot = TelegramBot(reminder_service, telegram_bot_token, telegram_bot_webhook_url)


	#
	# Setup Flask controllers
	#
	app.register_error_handler(HTTPException, _handle_exception)

	root_path = app.root_path
	frontend_path = os.path.join(root_path, "..", "..", "frontend")
	if os.path.isdir(frontend_path):
		# Register StaticController
		static_controller = StaticController(frontend_path)
		app.register_blueprint(static_controller.blueprint, url_prefix="/webapp")
		app.logger.info("Frontend directory was found: %s" % frontend_path)
	else:
		app.logger.warn("Frontend directory was not found: %s" % frontend_path)

	# Register TelegramWebhookHandlerController
	if telegram_bot_webhook_url_prefix is not None:
		telegram_webhook_handler_controller = TelegramWebhookHandlerController(bot=telegram_bot.underlaying_bot, update_queue=telegram_bot.update_queue)
		app.register_blueprint(telegram_webhook_handler_controller.blueprint, url_prefix=telegram_bot_webhook_url_prefix)

	#
	# Spin up application members
	#
	telegram_bot.__enter__()

	return app

def _handle_exception(e: HTTPException) -> None:
	"""Return empty response instead of HTML for HTTP errors."""
	# start with the correct headers and status code from the error
	response: Response = e.get_response()
	response.status = "%s %s" % (response.status_code, e.name)
	response.data = b""
	response.headers = {"BS-REASON-PHRASE": e.name}
	return response

