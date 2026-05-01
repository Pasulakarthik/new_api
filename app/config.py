import os
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

template_dir = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=template_dir)

templates.env = Environment(
    loader=FileSystemLoader(template_dir),
    cache_size=0  
)