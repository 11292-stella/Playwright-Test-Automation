import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
TENANT_LABEL = os.getenv("TENANT_LABEL")