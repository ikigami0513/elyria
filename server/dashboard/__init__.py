from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader("server/dashboard/templates"))