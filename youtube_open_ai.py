import openai
import os
from dotenv import load_dotenv
from youtube_popular_finder import YoutubePopularFinder
load_dotenv()

class YoutubeOpenAi:

    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self._get_messages()
        self.ai_model = 'gpt-3.5-turbo'
        self.conversation = []

    def __call__(self):
        return_string = 'Youtube:\n'
        if self.messages:
            if self._start_chat():
                # remove initializing messages from conversations
                del self.conversation[:2]
                for message in self.conversation:
                    if message['role'] == 'assistant':
                        if message['content'].upper().strip().rstrip('.') == 'FALSE':
                            continue
                        else:
                            # send to whatsapp
                            print(message['content'])
                            return_string += f"{message['content']}\n"
        return return_string

        
        
    def _start_chat(self):
        # initialize chat
        response = openai.ChatCompletion.create(
            model=self.ai_model,
            messages=[self.messages[0]],
            max_tokens=500
        )
        # remove the initializing message from the list
        self.conversation.append(self.messages.pop(0))
        if response and 'choices' in response:
            self.conversation.append(response.choices[0]['message'])
            for message in self.messages:
                self.conversation.append(message)
                response = openai.ChatCompletion.create(
                    model=self.ai_model,
                    messages=self.conversation,
                    max_tokens=500
                )
                self.conversation.append(response.choices[0]['message'])
                print(response['usage'])
                if 'error' in response:
                    print (response['error']['message'])

        else:
            # maybe send error to whatsapp from here
            print(f"Openai error in youtube, failed to start conversation: {response['error']['message']}")
 
        return True


    def _instructions(self):
        with open("youtube_instruction.txt", "r") as file:
            # Read the entire contents of the file
            return file.read()

    def _get_messages(self):
        videos = YoutubePopularFinder()()
        self.messages = []
        for video in videos:
            # here we can later analyze the whole video and thumbnail
            prompt = f'Title: {video["snippet"]["title"]}, URL: youtube.com/watch?v={video["id"]}'
            self.messages.append({"role": "user", "content": prompt})

        if self.messages:
            self.messages.insert(0, {"role": "system", "content": self._instructions()})
        

