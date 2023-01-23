from time import sleep
import openai


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


# Todo: Allow user to provide their own api_key
openai.api_key = open_file('commint/model/openapikey.txt')

def getCompletion(prompt, engine='text-davinci-003', temp=0.85, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.5, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def validate(comment: str, code: str) -> str:
    prompt = open_file('commint/model/prompt.txt').replace(
        '<<COMMENT>>', comment).replace('<<CODE>>',code)
    
    return getCompletion(prompt)