FizzBuzz = """
┌──╴      ┌─╮          │
├──╷╶─┐╶─┐├─┴╮╷ ╷╶─┐╶─┐│
│  │╭─╯╭─╯│  ││ │╭─╯╭─╯│
╵  ╵└─╴└─╴└──╯╰─┘└─╴└─╴╷
"""


import sys
import time
import os
from blessed import Terminal
from openai import OpenAI# for AI magic

term = Terminal()
client = OpenAI()

start = 1
limit = 100
speed = 0.01

fizz='Fizz'
fizzNum=int(3)

buzz='Buzz'
buzzNum=int(5)

fizzbuzz= fizz + buzz + '!' 


def chat_with_gpt(client, messages, model="gpt-4-1106-preview", stream=False):
    """
Model:                  Input Cost:         Output Cost:         
gpt-4-1106-preview      $0.010 / 1K tokens	$0.030 / 1K tokens
gpt-3.5-turbo-1106      $0.001 / 1K tokens	$0.002 / 1K tokens

    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )
        if stream:
            return map(map_chunks, response)
        else:
            return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)
    
def map_chunks(chunk):
    return chunk.choices[0].delta.content




def count_and_print(start, limit):
    for num in range(start, limit + 1):
        if num / fizzNum == int(num / fizzNum) and num / buzzNum == int(num / buzzNum):
            print(fizzbuzz)
        elif num / fizzNum == int(num / fizzNum) and num / buzzNum != int(num / buzzNum):
            print(fizz)
        elif num / buzzNum == int(num / buzzNum) and num / fizzNum != int(num / fizzNum):
            print(buzz)
        else:
            print(num)
        time.sleep(speed)



def run():
    count_and_print(start,limit)
    print()
    sys.stdout.flush()
    time.sleep(0.8)
    print('Would you like to make any adjustments to the rules??')
    aiconfig()





def aiconfig():
    global start, limit, speed, fizz, fizzNum, buzz, buzzNum, fizzbuzz

    request = input()
    request_prompt = [{"role": "system", "content": f"""
You are the AI brain of a FizzBuzz python program. Here are the current settings for the fizzbuzz output:
start = {start} (the number to start counting from)
limit = {limit} (the number to count to)
speed = {speed} (how fast it counts, or sleep.time between printing each number)

'Fizz' Settings:
fizz = {fizz} (The first word to display)
fizzNum = {fizzNum} (Replaces num with word if divisible by this)

'Buzz' Settings:
buzz = {buzz} (The second word to display)
buzzNum = {buzzNum} (Replaces num with word if divisible by this)

'FizzBuzz' Settings:
fizzbuzz = {fizzbuzz} (the text to display when both conditions are met)

The user has made the following request: '{request}'. Please interpret this request to the best of your abilities and adjust the current settings. If the user changes 'Fizz' or 'Buzz', ake sure to adjust the combined 'FizzBuzz' accordingly as well. Only print a comma-separated settings string and nothing else. Do not add any clarification, explanation, or questions.
Current Settings:{start},{limit},{speed},{fizz},{fizzNum},{buzz},{buzzNum},{fizzbuzz}
Update Settings:"""}]
    update_settings = chat_with_gpt(client, request_prompt)
    update_values = update_settings.split(",")

    start = int(update_values[0])
    limit = int(update_values[1])
    speed = float(update_values[2])

    fizz=update_values[3]
    fizzNum=int(update_values[4])

    buzz=update_values[5]
    buzzNum=int(update_values[6])

    fizzbuzz= update_values[7]
    run()



def main():
    run()


main()