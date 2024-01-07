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
speed = 0

word_number_pairs = {
    'Fizz': 3,
    'Buzz': 5
    # More pairs can be added dynamically
}

def update_word_number_pairs(command):
    global word_number_pairs

    parts = command.split()
    action = parts[0].lower()
    word = parts[1]

    if action == 'add' and len(parts) == 3:
        # Add a new word-number pair
        try:
            number = int(parts[2])
            word_number_pairs[word] = number
            print(f"\nAdded: {word} for numbers divisible by {number}")
        except ValueError:
            print("\nInvalid number for 'add' command.")
    elif action == 'remove':
        # Remove an existing word-number pair
        if word in word_number_pairs:
            del word_number_pairs[word]
            print(f"\nRemoved: {word}")
        else:
            print(f"\n{word} not found in the current settings.")
    elif action == 'change' and len(parts) == 3:
        # Change the number for an existing word
        if word in word_number_pairs:
            try:
                number = int(parts[2])
                word_number_pairs[word] = number
                print(f"\nChanged {word} to trigger on numbers divisible by {number}")
            except ValueError:
                print("\nInvalid number for 'change' command.")


def update_settings(response):
    global start, limit, speed

    commands = response.split('\n')
    for command in commands:
        parts = command.split()
        if len(parts) < 2:
            print(f"\nInvalid command format: {command}")
            continue

        action = parts[0].lower()

        if action in ['add', 'remove', 'change']:
            update_word_number_pairs(command)
        elif action == 'set' and len(parts) == 3:
            setting = parts[1].lower()
            value = parts[2]
            value = parts[2]

            if setting == 'start':
                try:
                    start = int(value)
                    print(f"\nStart number set to {start}")
                except ValueError:
                    print("\nInvalid value for start number.")
            elif setting == 'limit':
                try:
                    limit = int(value)
                    print(f"\nLimit number set to {limit}")
                except ValueError:
                    print("\nInvalid value for limit number.")
            elif setting == 'speed':
                try:
                    speed = float(value)
                    print(f"\nCounting speed set to {speed} seconds per number")
                except ValueError:
                    print("\nInvalid value for speed.")
        else:
            print(f"\nInvalid command: {command}")




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
        output = ''

        for word, divisor in word_number_pairs.items():
            if num % divisor == 0:
                output += word

        print(output if output else num)
        time.sleep(speed)




def run():
    count_and_print(start, limit)
    print()
    sys.stdout.flush()
    time.sleep(0.8)
    print('Would you like to make any adjustments to the rules?')
    aiconfig()





def aiconfig():
    global word_number_pairs, start, limit, speed

    request = input("")
    request_prompt = [{"role": "system", "content": f"""
You are the AI brain of a FizzBuzz python program. Current settings are:

Start number: {start} (The number the program starts counting from. Default: 1)
Limit number: {limit} (The number the program counts to. Default: 100)
Counting speed: {speed} (seconds per number. Default: 0)
Word-Number Pairs: {', '.join([f'{word} (divisible by {number})' for word, number in word_number_pairs.items()])} (Default: 'Fizz': 3, 'Buzz': 5)

You can modify these settings by issuing commands in the following formats:
- To change start or limit number: 'set start [Number]' or 'set limit [Number]'
- To change counting speed: 'set speed [Seconds]'
- To add a new word-number pair: 'add [Word] [Number]'
- To remove a word-number pair: 'remove [Word]'
- To change the number for a word: 'change [Word] [Number]'

For example, to change the start number to 5, say 'set start 5'. To add a pair that prints 'Boink' for numbers divisible by 10, say 'add Boink 10'.

The user has made the following request: '{request}'. Please interpret this request to the best of your abilities and format your response to adjust the current settings accordingly. Only output your command to the best of your abilities without adding any explanation or questions, as any additoinal text will crash the program.
""" }]

    update_request = chat_with_gpt(client, request_prompt)

    # Print ChatGPT's Response for troubleshooting
    print()
    print("ChatGPT's Response:", update_request)

    update_settings(update_request)
    run()




def main():
    print(FizzBuzz)
    time.sleep(1)
    run()


main()
