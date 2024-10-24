import requests
import base64
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def analyze_image_with_gemini(image_bytes):  
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    api_url = "https://gemini-api.google.com/analyze-image"
    headers = {
        "Authorization": "Your_api_key",
        "Content-Type": "application/json"
    }

    payload = {
        "image_data": image_base64,
        "task": "analyze_food_or_equipment_issue"
    }

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)

    try:
        response = http.post(api_url, json=payload, headers=headers)
        response.raise_for_status()

        return response.json().get("solution", "No solution provided")
    except requests.exceptions.RequestException as e:
        return f"Error in analyzing the image: {e}"

# Example function to handle image solution
def get_solution_from_gemini(image):
    return analyze_image_with_gemini(image)
