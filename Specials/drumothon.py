import json

"""
█▀▀▄ █▀▀█ █  █ █▀▄▀█ █▀▀▀█ ▀▀█▀▀ █  █ █▀▀▀█ █▄  █ 
█  █ █▄▄▀ █  █ █ █ █ █   █   █   █▀▀█ █   █ █ █ █ 
█▄▄▀ █  █ ▀▄▄▀ █   █ █▄▄▄█   █   █  █ █▄▄▄█ █  ▀█

Drumothon is a DrumoScript-to-Python compiler.
Be aware that this is in beta, so there aren't as many features as DrumoScript yet.  
"""

with open('config.json', 'r') as f:
  configjson = json.loads(f.read())
  basics = configjson.get('basics')
  print_keyword = basics.get("print")
  varDelimiter = configjson.get('varDelimiter')
  listDelimiter = configjson.get('listDelim')
  dictDelimiter = configjson.get('dictDelim')

def compile():
  with open(configjson.get('entrypoint'), 'r') as f:
    code = f.readlines()
    f.close()
  compiled = []
  for line in code:
    lexemes = line.split()
    for item in lexemes:
      item = item.replace("\n", "")
      if item == print_keyword:
        val = lexemes[lexemes.index(item) + 1:]
        val = " ".join(val)
        val = val.replace('"', '')
        var = 0
        if val.startswith(varDelimiter) and val.endswith(varDelimiter):
          var = 1
          val = val.replace(varDelimiter, '')
        elif val.split()[0].startswith(listDelimiter) and val.split()[0].endswith(listDelimiter):
          var = 1
          val = val.split()
          val = f"{val[1]}[{val[0].replace(listDelimiter, '')}]"
        elif val.split()[0].startswith(dictDelimiter) and val.split()[0].endswith(dictDelimiter):
          var = 1
          val = val.split()
          val = f"{val[1]}.get('{val[0].replace(dictDelimiter, '')}')"
        if var == 1:
          compiled.append(f'print({val})')
        else:
          compiled.append(f'print("{val}")')
        break
      elif item in ('str', 'int'):
        varname = lexemes[lexemes.index(item) + 1]
        varval = " ".join(lexemes[lexemes.index(item) + 2:])
        if varval.isdigit():
          compiled.append(f'{varname} = {varval}')
        elif varval.split()[0] == 'stdin':
          compiled.append(f'{varname} = input("{varval.replace("stdin ", "")} - ")')
        elif varval.split()[0] == 'read':
          compiled.append(f'with open("{varval.split()[1]}", "r") as f:\n\t{varname} = f.read()\n\tf.close()')
        else:
          compiled.append(f'{varname} = "{varval}"')
        break
      elif item in ('list', 'dict'):
        if item == 'list':
          listname = lexemes[lexemes.index(item) + 1]
          vals = []
          val = []
          for i in lexemes[lexemes.index(item) + 2:]:
            if i != '-':
              val.append(i)
            else:
              vals.append(" ".join(val))
              val = []
          vals.append(" ".join(val))
          val = []
          for i in vals:
            if i.isdigit():
              vals[vals.index(i)] = int(i)
          compiled.append(f'{listname} = {vals}')
        elif item == 'dict':
          dictname = lexemes[lexemes.index(item) + 1]
          key = ""
          vals = []
          keys = []
          val = []
          for i in lexemes[lexemes.index(item) + 2:]:
            if i != '-':
              if key != "":
                val.append(i)
              else:
                key = i
                keys.append(key)
            else:
              vals.append(" ".join(val))
              val = []
              key = ""
          vals.append(" ".join(val))
          val = []
          key = ""
          for i in vals:
            if i.isdigit():
              vals[vals.index(i)] = int(i)
          dictvals = {}
          for i in keys:
            dictvals[i] = vals[keys.index(i)]
          compiled.append(f'{dictname} = {dictvals}')
        break
      elif item == '<<':
        compiled.append(f'# {" ".join(lexemes[lexemes.index(item) + 1:-1])}')
        break
      elif item == 'set':
        varname = lexemes[lexemes.index(item) + 1]
        varval = " ".join(lexemes[lexemes.index(item) + 2:])
        if varval.isdigit():
          varval = int(varval)
          compiled.append(f"{varname} = {varval}")
        elif varval.split()[0] == 'stdin':
          compiled.append(f'{varname} = input("{varval.replace("stdin ", "")} - ")')
        elif varval.split()[0] == 'read':
          compiled.append(f'with open("{varval.split()[1]}", "r") as f:\n\t{varname} = f.read()\n\tf.close()')
        else:
          compiled.append(f'{varname} = "{varval}"')
        break
      elif item == 'stdin':
        compiled.append(f'input("{" ".join(lexemes[lexemes.index(item) + 1:])}")')
        break
  print(compiled)

compile()