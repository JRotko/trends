from pytrends.request import TrendReq
import pandas as pd



class Google:
    def __call__(self):
        #get today's treniding topics
        pytrends = TrendReq(hl='en-US', tz=360)

        for i in range(5):
            try:
                trendingtoday = pytrends.realtime_trending_searches(pn='US')
                break
            except Exception as e:
                if i == 5:
                    return f'Tried to fetch google trends {i} times withouth success'
                sleep(i)
        

        messages=[]
        for index, row in trendingtoday.iterrows():
            prompt = f'{row["entityNames"]}'
            messages.append({"role": "user", "content": prompt})
        # set instructions in front of the list and return it
        if messages:
            with open('google_instruction.txt', 'r') as file:
                instructions = file.read().replace('\n', ' ')
            messages.insert(0, {"role": "system", "content": instructions})
            print(messages)
            return messages
        # return false if nothing found
        return False
        
        
