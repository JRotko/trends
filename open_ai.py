import openai
import os
import random
import time
from dotenv import load_dotenv
load_dotenv()

class OpenAi:

    def __init__(self, messages):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.messages=messages
        self.ai_model = 'gpt-3.5-turbo'
        self.conversation = []
        self.max_retries = 5

    def __call__(self):
        return_string = ''
        if self.messages:
            if self._start_chat():
                # remove initializing messages from conversations
                del self.conversation[:2]
                for message in self.conversation:
                    if message['role'] == 'assistant':
                        if 'FALSE' in message['content'].upper().strip().rstrip('.'):
                            continue
                        else:
                            print(message['content'])
                            return_string += f"{message['content']}\n"
        return return_string

        
        
    def _start_chat(self):
        # initialize chat
        response = openai.ChatCompletion.create(
            model=self.ai_model,
            messages=[self.messages[0]],
            max_tokens=500,
            temperature=0.2
        )
        # remove the initializing message from the list
        self.conversation.append(self.messages.pop(0))
        if response and 'choices' in response:
            self.conversation.append(response.choices[0]['message'])
            for message in self.messages:
                self.conversation.append(message)
                delay = 1
                while True:
                    retries=0
                    try:
                        response = openai.ChatCompletion.create(
                            model=self.ai_model,
                            messages=self.conversation,
                            max_tokens=500,
                            temperature=0.2
                        )
                        self.conversation.append(response.choices[0]['message'])
                        print(response['usage'])
                        break
                    # Sometimes the api just rejects new messages. Just have a small delay and try again
                    except openai.error.ServiceUnavailableError as e:
                        print(f"RETRIES: {retries}")
                        retries+=1
                        # Check if max retries has been reached
                        if retries > self.max_retries:
                            raise Exception(
                                f"Maximum number of retries ({max_retries}) exceeded."
                            )
        
                        # Increment the delay. Randomness is suggested in documentation
                        delay *= 2 * (1 + True * random.random())
        
                        # Sleep for the delay
                        time.sleep(delay)
                    except Exception as e:
                        print(e)
        else:
            # maybe send error to whatsapp from here
            print(f"Openai error in youtube, failed to start conversation: {response['error']['message']}")
 
        return True



        

