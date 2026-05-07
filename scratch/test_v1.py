
import os
from fastapi import Request
from fastapi.templating import Jinja2Templates
from unittest.mock import MagicMock

BASE_DIR = r"d:\Projects\Shopping_Mall_Call_Agent"
FRONTEND_DIR = os.path.join(BASE_DIR, "Front_End")
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

request = MagicMock(spec=Request)
request.scope = {"type": "http"}

print("--- Test 1: TemplateResponse(name, context) ---")
try:
    response = templates.TemplateResponse("index.html", {"request": request})
    print("Success")
except Exception as e:
    print(f"Failed: {e}")

print("\n--- Test 2: TemplateResponse(request, name) ---")
try:
    response = templates.TemplateResponse(request, "index.html")
    print("Success")
except Exception as e:
    print(f"Failed: {e}")

print("\n--- Test 3: TemplateResponse(name='index.html', context={'request': request}) ---")
try:
    response = templates.TemplateResponse(name="index.html", context={"request": request})
    print("Success")
except Exception as e:
    print(f"Failed: {e}")
