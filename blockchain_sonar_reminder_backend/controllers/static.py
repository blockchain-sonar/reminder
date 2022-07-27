#
# See https://flask.palletsprojects.com/en/2.1.x/tutorial/static/
# See https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
# See https://stackoverflow.com/questions/55248703/how-use-flask-route-with-class-based-view
#

from flask import Blueprint, abort, send_from_directory

class StaticController(object):

	def __init__(self, static_folder: str):
		self._static_folder = static_folder

		self.blueprint = Blueprint('Static', __name__)
		self.blueprint.add_url_rule('/<path:name>', methods=["GET"], view_func=self._download_file)
		self.blueprint.add_url_rule('/', methods=["GET"], view_func=self._download_index)

	def _download_file(self, name: str):
		if name.endswith(".html"):
			# Prevent ".html" in URL
			abort(404)

		if name == "index":
			# Prevent "index" in URL
			abort(404)

		filename: str = name
		if "." not in filename:
			filename: str = filename + ".html"

		return send_from_directory(self._static_folder, filename)

	def _download_index(self):
		return send_from_directory(self._static_folder, "index.html")
