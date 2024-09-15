import requests
import json

# URL of the Flask API
api_url = "http://127.0.0.1:5000/ask"

# Question to ask the API
question = {
    "question": "What was the hypothesis 2?"
}

# Make a POST request to the API
response = requests.post(api_url, json=question)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()
    
    # Print the answer and source documents
    print("Answer:", result['answer'])
    # print("\nSources:")
    # for idx, source in enumerate(result['sources']):
    #     print(f"Source {idx + 1}: {source}")
else:
    # Print the error if the request failed
    print(f"Error: {response.status_code}")
    print(response.json())
