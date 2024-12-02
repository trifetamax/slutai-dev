from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from steel_integration import scrape_web_page, take_screenshot

app = Flask(__name__)

# Load your local LLM
tokenizer = AutoTokenizer.from_pretrained("local-model-path")
model = AutoModelForCausalLM.from_pretrained("local-model-path")

@app.route('/post', methods=['POST'])
def predict():
    data = request.json
    user_input = data['text']
    
    # Process with LLM
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"response": response_text})

@app.route('/init', methods=['POST'])
def scrape():
    data = request.json
    url = data['url']
    wait_time = data.get('waitFor', 1000)
    scraped_data = scrape_web_page(url, wait_for=wait_time)
    return jsonify(scraped_data)

@app.route('/screenshot', methods=['POST'])
def screenshot():
    data = request.json
    url = data['url']
    full_page = data.get('fullPage', True)
    file_path = take_screenshot(url, full_page=full_page)
    return jsonify({"screenshot_path": file_path})

if __name__ == "__main__":
    app.run(debug=True)
