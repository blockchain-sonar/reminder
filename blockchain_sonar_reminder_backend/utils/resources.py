import chevron
import json
from pathlib import Path
import pkgutil
from typing import Any


def read_resource(resource_path: str) -> bytes:
	assert isinstance(resource_path, str)

	resource_data_bytes = pkgutil.get_data(__name__, resource_path)
	if resource_data_bytes is None:
		raise Exception("Not found template: %s" % resource_path)

	return resource_data_bytes

def read_resource_json(resource_path: str) -> dict:
	assert isinstance(resource_path, str)

	resource_data_bytes = read_resource(resource_path)

	resource_data_str: str = resource_data_bytes.decode("utf-8")

	json_data = json.loads(resource_data_str)

	return json_data

def render_message(package: str, template_name: str, data_context: Any) -> str:
	assert isinstance(package, str)
	assert isinstance(template_name, str)
	# assert isinstance(data_context, dict)

	templates_directory_path: Path = Path("templates")
	template_path: Path = templates_directory_path.joinpath(template_name)
	template_resource: str = template_path.as_posix()

	template_data_bytes = pkgutil.get_data(package, template_resource)
	if template_data_bytes is None:
		raise Exception("Not found template: %s" % template_name)

	template_data_str: str = template_data_bytes.decode("utf-8")

	render_result = chevron.render(template_data_str, data_context)

	assert isinstance(render_result, str)

	return render_result
