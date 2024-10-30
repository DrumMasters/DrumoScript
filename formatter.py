import json

"""
█▀▄ █▀█ █ █ █▀▄▀█ █▀█ █▀▀ █▀█ █▀█ █▀▄▀█
█▄▀ █▀▄ █▄█ █ ▀ █ █▄█ █▀  █▄█ █▀▄ █ ▀ █

DrumoForm is DrumoScript's new formatter. Now the code will be organized with tabs!
"""

with open('config.json', 'r') as f:
  config = json.load(f)
entrypoint = config.get('entrypoint')
with open(entrypoint, 'r') as f:
  code = f.readlines()

def format_code():
  formattedCode = []
  IndentLevel = 0
  indentType = input("Use tabs or spaces? [T|S] ")
  indentType = "\t" if indentType.upper() == 'T' else '  '
  for item in code:
    for itemsplit in item.split():
      if itemsplit in ('if', 'elif', 'else', 'proc', 'repeat'):
        IndentLevel += 1
        if itemsplit in('if', 'proc', 'repeat'):
          if itemsplit != 'proc':
            if code.index(item) != 0:
              formattedCode.append("\n" + indentType * (IndentLevel - 1) + item + "\n")
            else:
              formattedCode.append(indentType * (IndentLevel - 1) + item + "\n")
          else:
            if code.index(item) != 0:
              formattedCode.append("\n" + indentType * (IndentLevel - 1) + item)
            else:
              formattedCode.append(indentType * (IndentLevel - 1) + item)
        else:
          IndentLevel -= 1
          formattedCode.append(indentType * (IndentLevel - 1) + item + "\n")
        break
      elif itemsplit in ('end', 'endp', 'endr'):
        IndentLevel -= 1
        formattedCode.append(indentType * (IndentLevel) + item)
        break
      elif itemsplit == '<<':
        formattedCode.append(f"\n{indentType * (IndentLevel) + item}\n")
        break
      elif itemsplit == 'print':
        formattedCode.append(f"{indentType * (IndentLevel) + item}\n")
        break
      elif itemsplit == 'exec':
        formattedCode.append(f"\n{indentType * (IndentLevel) +  item}\n")
        break
      else:
        formattedCode.append(indentType * IndentLevel + item)
        break
  print("Format preview:")
  print("".join(formattedCode))
  answer = input("Apply formatting? [Y|N] ")

  if answer.upper() == "Y":
    with open(entrypoint, 'w') as f:
      f.write("".join(formattedCode))
      f.close()
  else:
    print("Formatting exited.")