import google.generativeai as genai

genai.configure(api_key="AIzaSyAe3gnt863nPVFliIWVwufWKRRtbdMYwvQ")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello, how are you?")
print(response.text)