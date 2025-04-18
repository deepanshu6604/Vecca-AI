import random
import speech_recognition as sr
import pyttsx3
import requests
import pygame
from io import BytesIO


class Speakers:
    #def __init__(self):
    #    self.model = genai.GenerativeModel(GENAI_MODEL_NAME)
    def generate_and_play_tts(text):
    
        # API credentials and voice manifest URL
        user_id = "CoDt8WUUPITrndxtkipe8AvlCRo2"  # Replace with actual user ID
        api_key = "e3009e995f88443e98dc0448fce2dae6"  # Replace with actual API key
        voice_manifest_url = "s3://voice-cloning-zero-shot/a2aacd03-af8b-4584-ba46-d7ce5bd11c8f/original/manifest.json"  # Replace with actual voice manifest URL
        
        url = "https://api.play.ht/api/v2/tts/stream"
        
        headers = {
            'X-USER-ID': user_id,
            'AUTHORIZATION': api_key,
            'accept': 'audio/mpeg',
            'content-type': 'application/json'
        }
        
        data = {
            "text": text,
            "voice_engine": "Play3.0",  # Check if this is the latest voice engine
            "voice": voice_manifest_url,
            "output_format": "mp3"
        }
        
        # Send the request to the API
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                # Initialize Pygame mixer for audio playback
                pygame.mixer.init()

                # Convert the response content (MP3 audio) to a byte stream
                audio_data = BytesIO(response.content)

                # Load the audio from the byte stream into Pygame
                pygame.mixer.music.load(audio_data)
                
                # Play the audio
                pygame.mixer.music.play()

                # Wait for the audio to finish before returning
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                print("Audio playback finished")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
        
speak = Speakers()   
Speakers.generate_and_play_tts("hello my name is deepanshu vishwakarma")     
