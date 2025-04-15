import base64
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Loaded environment variables")
logger.info("GROQ API URL: %s", GROQ_API_URL)
logger.info("GROQ API Key: %s", GROQ_API_KEY)

if not GROQ_API_KEY:
    logger.error("GROQ API is not set in .env")
    raise ValueError("GROQ API is not set in .env")

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError("GROQ API is not set in .env")


def process_image(image_path , query):
    try:
        with open(image_path , "rb") as image_file:
            image_content = image_file.read()
            encoded_image  = base64.b64encode(image_content).decode("utf-8")
        try:    
            img = Image.open(io.BytesIO(image_content))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid Image format :{str(e)}")
            return {"error" : f"Invalid Image format :{str(e)}"}
        messages = [
             {
                "role" :"user"
                "content" : [
                    {"type": "text", "text" :"query"},
                    {"type": "image-url", "image-url" : {"url" : f"data :image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]
        
        def make_api_request(model):
            requests.post(
                GROQ_API_URL,
                json={
                    "model" : model ,
                    "messages" : messages ,
                    "max-tokens" : 1000
                },
                headers = {
                    "Authorization" : f"Bearer {GROQ_API_KEY}",
                    "Content-Type" : "application/json"
                    
                },
                timeout = 30
            )
            return response
        
        llama_11b_response = make_api_request("llama-3.2-11b-vision-preview")
        llama_90b_response  = make_api_request("llama-3.2-90b-vision-preview")
        
        responses = {}
        
        for model , response in [("llama11b", llama_11b_response),("llama90b", llama_90b_response)]:
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                logger.info(f"Processed response from {model} API : {answer}" )
                responses[model] = answer
            else:
                logger.error(f"Error from {model} API : {response.status_code} - {response.text}")    
                responses[model] = f"Error from {model} API : {response.status_code}"
        return responses        
        
            
    except Exception as e:
        logger.error(f"An unexpected error occurred :{str(e)}")
        return {"error" : f"An unexpected error occurred :{str(e)}"}

if __name__ == "__main__":
    image_path = ""
    query = "what are the encoders  in the picture?"
    result = process_image(image_path, query)
    print(result)