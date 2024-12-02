import requests

STEEL_BASE_URL = "http://0.0.0.0:3000/v1"

def scrape_web_page(url, wait_for=1000):
    endpoint = f"{STEEL_BASE_URL}/scrape"
    payload = {
        "url": url,
        "waitFor": wait_for
    }
    response = requests.post(endpoint, json=payload)
    return response.json()

def take_screenshot(url, full_page=True, output_file="screenshot.png"):
    endpoint = f"{STEEL_BASE_URL}/screenshot"
    payload = {
        "url": url,
        "fullPage": full_page
    }
    response = requests.post(endpoint, json=payload, stream=True)
    with open(output_file, "wb") as f:
        f.write(response.content)
    return output_file
