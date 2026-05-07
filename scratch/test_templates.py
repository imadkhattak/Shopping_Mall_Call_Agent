
import os
from fastapi import Request
from fastapi.templating import Jinja2Templates

BASE_DIR = r"d:\Projects\Shopping_Mall_Call_Agent"
FRONTEND_DIR = os.path.join(BASE_DIR, "Front_End")
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

print(f"Templates dir: {os.path.join(FRONTEND_DIR, 'templates')}")
print(f"Exists: {os.path.exists(os.path.join(FRONTEND_DIR, 'templates'))}")

try:
    # Simulating the call in main.py
    # return templates.TemplateResponse(request, "index.html")
    # We need a dummy request
    from unittest.mock import MagicMock
    request = MagicMock(spec=Request)
    request.scope = {"type": "http"}
    
    response = templates.TemplateResponse("index.html", {"request": request})
    print("Template rendering successful")
except Exception as e:
    print(f"Template rendering failed: {e}")
    import traceback
    traceback.print_exc()
