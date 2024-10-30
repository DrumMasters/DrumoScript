import nltk
import random
import os
import json
from nltk.sentiment import SentimentIntensityAnalyzer

greetings = ["hello", "hi", "hey", "greetings"]
support_request = "support"
thanks = "thank"
generate_code = "generate"
boilerplates = [
"""
proc {proc_name}
<< your code here >>
endp
"""
]
support = ["Every setback is a setup for a comeback. Keep pushing forward, and your success will be unstoppable.",
           "Embrace the challenges ahead, for they are the stepping stones to your greatest achievements.",
           "In the journey of life, the most rewarding destinations often require the toughest climbs. Keep climbing!",
           "Your dreams are the blueprints of your future. Build them with determination, and watch them become reality.",
           "You possess within you the power to turn your dreams into goals and your goals into accomplishments. Believe in yourself and keep moving forward."
          ]
requests = {"basics": 
            ["print", 
             "escape", 
             "input", 
             "clear",
             "wait"],
            "vars":  ["string", 
                      "integer", 
                      "increment", 
                      "decrement", 
                      "random", 
                      "concatenate", 
                      "remove", 
                      "http", 
                      "list", 
                      "dict"]
           }

boilerplates_generated = []

nltk.download("vader_lexicon")
sid = SentimentIntensityAnalyzer()

def cls():
  os.system('clear')

def generate_boilerplate(template, funcname):
  boilerplates_generated.append(template.format(proc_name=funcname))
  return template.format(proc_name=funcname)

def respond(user_input):
  score = sid.polarity_scores(user_input)
  compound = score["compound"]
  ui_split = user_input.split()
  response = ""
  func = 0
  funcname = ""
  boilerplate_to_integrate = ""
  idx = 0
  for item in ui_split:
    if item == 'generate':
      for i in ui_split[ui_split.index(item) + 1:]:
        # Function Check
        if 'function' in i or 'func' in i or 'procedure' in i or 'proc' in i:
          if func == 0:
            func = 1
            continue
        if 'title' or 'name' in i:
          if func == 1:
            func = 2
            continue
        if func == 2:
          funcname = i.replace(".", "").replace('"', '').replace("'", "")
          response = f"Sure! Here's a template for your code:\n {generate_boilerplate(boilerplates[0], funcname)}"
          break
      if func == 1 and not funcname:
        funcname = "template"
        response = f"Sure! Here's a template for your code:\n{generate_boilerplate(boilerplates[0], funcname)}"
      break
    elif item == 'integrate':
      integ_func = 0
      fti = 1
      for i in ui_split[ui_split.index(item) + 1:]:
        if i in ('function', 'func', 'procedure', 'proc') and integ_func != 1:
          integ_func = 1
          continue
        elif integ_func == 1:
          idx = 0
          if i.isdigit():
            idx = int(i) - 1
          boilerplate_to_integrate = boilerplates_generated[idx]
          continue
        elif i in ('latest', 'that'):
          idx = -1
          boilerplate_to_integrate = boilerplates_generated[idx]
        elif integ_func == 1 and (i == 'into' or i == 'in'):
          fti = 1
          continue
        elif fti == 1:
          file_to_integrate = i
          if os.path.exists(file_to_integrate):
            with open(file_to_integrate, 'a') as f:
              f.write(boilerplate_to_integrate)
              response = f"I've succesfully integrated your function into {file_to_integrate}."
              f.close()
          else:
            response = "Sorry, I didn't manage to find the file you wanted me to integrate your code in. Could you please be more specific?"
    elif item == 'parse':
      parse = ui_split[ui_split.index(item) + 1]
      if os.path.exists(f"{parse}.json"):
        with open(f'{parse}.json', 'r') as f:
          to_parse = json.load(f)
          f.close()
        response_parse = ""
        for item in to_parse:
          response_parse += f"{item} = \"{to_parse.get(item)}\",\n"
        response_parse = response_parse.rstrip(",\n")
        if len(to_parse) < 5:
          response = f"Sure! I'll try to parse {parse}.json:\n{response_parse}\nOverall, this JSON file is quite small."
        elif len(to_parse) < 10:
          response = f"Sure! I'll try to parse {parse}.json:\n{response_parse}\nOverall, this JSON file is a bit big!"
        else:
          response = f"Sure! I'll try to parse {parse}.json:\n{response_parse}\nOverall, this JSON file is quite large!"
      else:
        response = "Sorry, I couldn't find the JSON file you were looking to parse. Maybe be a bit more specific? :)"
    for greeting in greetings:
      if greeting in item:
        response = "Greetings, user! How may I help you?"
    for request in requests.get("basics"):
      if request in item:
        if request == 'print':
          with open('References/Basics/print.txt', 'r') as f:
            response = f.read()
        elif request == 'escape':
          with open('References/Basics/escape_seq.txt', 'r') as f:
            response = f.read()
        elif request == 'input':
          with open('References/Basics/input.txt', 'r') as f:
            response = f.read()
        elif request == 'clear':
          with open('References/Basics/cls.txt', 'r') as f:
            response = f.read()
        elif request == 'wait':
          with open('References/Basics/wait.txt', 'r') as f:
            response = f.read()
    for request in requests.get("vars"):
      if request in item:
        if request == "string":
          with open('References/Variables/strings.txt', 'r') as f:
            response = f.read()
        elif request == "integer":
          with open('References/Variables/integers.txt', 'r') as f:
            response = f.read()
        elif request == "increment":
          with open('References/Variables/increment.txt', 'r') as f:
            response = f.read()
        elif request == "decrement":
          with open('References/Variables/decrement.txt', 'r') as f:
            response = f.read()
        elif request == "random":
          with open('References/Variables/random.txt', 'r') as f:
            response = f.read()
        elif request == "concatenate":
          with open('References/Variables/concat.txt', 'r') as f:
            response = f.read()
        elif request == "remove":
          with open('References/Variables/removal.txt', 'r') as f:
            response = f.read()
        elif request == "http":
          with open('References/Variables/httpget.txt', 'r') as f:
            response = f.read()
        elif request == "list":
          with open('References/Variables/list.txt', 'r') as f:
            response = f.read()
        elif request == "dict":
          with open('References/Variables/dict.txt', 'r') as f:
            response = f.read()
    if item == support_request:
      response = f"Allow me to give you a motivational message to help out.\n\n\"{support[random.randint(0, 4)]}\""
    elif thanks in item:
      response = "No problem! Feel free to ask any more questions or just chat!"
      
  if not response:
      response = "Sorry, I didn't quite understand your request. Could you please rephrase?"
  
  if compound < 0:
    response = "I detect a hint of frustration in your voice. Let's see if we can help.\n" + response
  elif compound > 0.1:
    response = "I see you're in a nice mood! Let's see if I can help you more.\n" + response
  
  return response

cls()
print("[AI]:")
print(
    "Hello there, user! I'm DrumAI, a new AI for DrumoScript. I'm here to help you with any coding problems you need solved!\n"
)
print("Not sure what to ask? Ask one of these templates below!")
print("- How do I print text to the console?")
print("- Generate me a function titled proc.")
print("- Parse file")
print("Of course, these are just templates. Feel free to ask whatever you like!\n")

while True:
  input_result = input("[You]: ")
  print()
  response = respond(input_result.lower())
  print(f"[AI]:\n{response}\n\nBy the way, please forgive me if I misinterpreted your request. I'm still in beta. :)\n")
