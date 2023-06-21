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
        self.responses=[]

    def __call__(self):
        return_string = ''
        if self.messages:
            if self._start_chat():
                for response in self.responses:
                    if 'FALSE' in response.upper():
                        continue
                    else:
                        return_string += response

        return return_string

        
        
    def _start_chat(self):
        # initialize chat
        response = openai.ChatCompletion.create(
            model=self.ai_model,
            messages=[self.messages[0]],
            max_tokens=600,
            temperature=0.2
        )
        # remove the initializing message from the list
        self.conversation.append(self.messages.pop(0))
        if response and 'choices' in response:
            self.conversation.append(response.choices[0]['message'])
            for message in self.messages:
                delay = 1
                while True:
                    service_retries=0
                    rate_retries=0
                    try:
                        response = openai.ChatCompletion.create(
                            model=self.ai_model,
                            messages=self.conversation + [message],
                            max_tokens=600,
                            temperature=0.2
                        )
                        # add the prompt from previous message to add clarity in the response
                        # gpt3.5 was too stupid to reliably provide the youtube link/google keywords
                        self.responses.append(f"Prompt: {message['content'][:100]}\nResponse: {response.choices[0]['message']['content']}\n\n")
                        print(response['usage'])
                        break
                    # Sometimes the api just rejects new messages. Just have a small delay and try again
                    except openai.error.ServiceUnavailableError as e:
                        print(f"RETRIES: {service_retries}")
                        service_retries+=1
                        # Check if max retries has been reached
                        if service_retries > self.max_retries:
                            raise Exception(
                                f"Maximum number of service retries ({max_retries}) exceeded."
                            )
        
                        # Increment the delay. Randomness is suggested in documentation
                        delay *= 2 * (1 + True * random.random())
        
                        # Sleep for the delay
                        time.sleep(delay)

                    except openai.error.RateLimitError as e:
                        sleep(60)
                        rate_retries+=1
                        # Check if max retries has been reached
                        if rate_retries > self.max_retries:
                            raise Exception(
                                f"Maximum number of rate retries ({max_retries}) exceeded."
                            )
                    except Exception as e:
                        print(e)

        return True



        

