# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
from os import environ
import subprocess
import sys
import openai
import getch
import pyperclip

openai.api_key = environ["OPENAI_API_KEY"]
question = sys.argv[1]

MODEL = "gpt-3.5-turbo-0301"
TRY_AGAIN ="show me another alternative, just in case. just print the command."
simple_messages=[
        {"role": "system", "content": "You are a macos bash utility that helps users remember how to write shell commands and scripts.\
         User will write what they wan to accomplish, and you will respond with a single command that will help them do that. \
         Keep descriptions concise. Only respond with command, no other formatting or text. No description as well."},
        {"role": "user", "content": "how do I list files in a directory (including hidden files)"},
        {"role": "assistant", "content": "ls -a"},
        {"role": "user", "content": "how do I update my shell so it uses the latest changes to my .zshrc"},
        {"role": "assistant", "content": "source ~/.zshrc"}
    ]

# Append a new user message
simple_messages.append({"role": "user", "content": f"{question}"})

print("Umm...")

raw_response = openai.ChatCompletion.create(
  model=MODEL,
  messages=simple_messages
)

response = raw_response.choices[0].message.content

def clear():
    # print("\033[H\033[J")
    sys.stdout.write("\033[F")

def printResponse(response):
    print(f"\r            ", end="", flush=True)
    print(f"\r{response}", end="\n", flush=True)
    print("r: Regenerate, c: Copy, x: Execute, q: Esc", end="", flush=True)

def execute(command):
    try:
        output = subprocess.check_output(f"{command}", shell=True)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"{e}")

while True:
    if response == "": # If the response is empty, break
        print("No response")
        break

    clear()
    printResponse(response)
    
    # Read user input and append to messages
    choice = getch.getch()

    if choice == "q":
        break
    elif choice == "r":
        # Append the response to the messages
        simple_messages.append({"role": "assistant", "content": f"{response}"})
        simple_messages.append({"role": "user", "content": f"{TRY_AGAIN}"})
        clear()
        printResponse("Thinking...")
        # Get the next response
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=simple_messages
        ).choices[0].message.content

    elif choice == "c":
        pyperclip.copy(response)
        break

    elif choice == "x":
        # print(f"\n{response}")
        # break
        output = subprocess.check_output(response, shell=True)
        print(output.decode())
        break