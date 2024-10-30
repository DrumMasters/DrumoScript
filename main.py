import json
import os
import random
import requests
import formatter as format
import colorama
import time
from colorama import Fore

colorama.init(autoreset=True)

"""

█▀▀▄  █▀▀█  █  █  █▀▄▀█  █▀▀▀█  █▀▀▀█  █▀▀█  █▀▀█ ▀█▀  █▀▀█ ▀▀█▀▀
█  █  █▄▄▀  █  █  █ █ █  █   █  ▀▀▀▄▄  █     █▄▄▀  █   █▄▄█   █
█▄▄▀  █  █  ▀▄▄▀  █   █  █▄▄▄█  █▄▄▄█  █▄▄█  █  █ ▄█▄  █      █

DrumoScript is a sleek and cool programming language that has elegant, but simple syntax.

Features:
- Basics:
  - Printing
  - Escape sequences
  - Input
  - Clearing the screen
  - Wait command
- Variables:
  - Strings
  - Integers
  - Incrementation/decrementation
  - String Concatenation
  - Randomness
  - HTTP REQUESTS
  - Lists
  - Dictionaries
- Comments:
  - Normal comments
  - Inline comments
- Advanced:
  - Processes (basically, executes DrumoScript code from a string or variable)
  - File I/O (creating files, writing to files, resetting files, creating folders, deleting folders)
  - If statements (comes with operators!)
  - PROCEDURES (functions)
  - Macros (reusable variables without having to declare them)
  - Repeat Statements!
  - HTTP POST REQUESTS
- Others:
  - FORMATTER (DrumoForm)
  - COMPILER (Drumothon) [BETA]
"""

with open('config.json', 'r') as f:
  configjson = json.load(f)

# Configurations

lang_name = configjson.get("language")  # Language name
lang_ver = configjson.get("version")  # Language version
lang_author = configjson.get("author")  # Language author

entrypoint = configjson.get("entrypoint")  # Entrypoint
shell = int(configjson.get("shell"))  # Shell
if shell == 1:
  shell_name = configjson.get("shell_name")
debug = configjson.get("debug")  # Debug
formatter = configjson.get("formatter") # Formatter

# Keywords
basics = configjson.get('basics')
print_keyword = basics.get("print")
process_keyword = basics.get("process")
append_keyword = basics.get("append")
setvar_keyword = basics.get("setvar")
wait_keyword = basics.get("delay")
advanced = configjson.get('advanced')
task_keyword = advanced.get("task")
#####################################
primitive_dt = configjson.get('dataTypes').get('primitive')
str_keyword = primitive_dt[0]
int_keyword = primitive_dt[1]
composite_dt = configjson.get('dataTypes').get('composite')
list_keyword = composite_dt[0]
dict_keyword = composite_dt[1]
comment = configjson.get('comment')
comment_start = comment[0]
comment_end = comment[1]
keywords = configjson.get('keywords')
esc_seqs = configjson.get('escape_sequences')
newline = esc_seqs[0]
tab = esc_seqs[1]
vtab = esc_seqs[2]
backspace = esc_seqs[3]
varDelimiter = configjson.get('varDelimiter')
listDelimiter = configjson.get('listDelim')
dictDelimiter = configjson.get('dictDelim')
macroDelimiter = configjson.get('macroDelimiter')
input_keyword = configjson.get('inputKeyword')
createFileKeywords = configjson.get('createFileKeywords')
createKeyword = createFileKeywords[0]
writeKeyword = createFileKeywords[1]
resetKeyword = createFileKeywords[2]
mkdirKeyword = createFileKeywords[3]
emptyKeyword = createFileKeywords[4]
deleteKeyword = createFileKeywords[5]
rmdirKeyword = createFileKeywords[6]
readKeyword = createFileKeywords[7]
if_keyword = keywords[0]
elif_keyword = keywords[1]
else_keyword = keywords[2]
end_keyword = keywords[3]
proc_keyword = keywords[4]
endp_keyword = keywords[5]
call_keyword = keywords[6]
endr_keyword = keywords[7]
increment_keyword = configjson.get("increment")
decrement_keyword = configjson.get("decrement")
concat_keyword = configjson.get("concat")
remove_keyword = configjson.get("remove")
import_keyword = configjson.get("import")
macro_keyword = configjson.get("macro")
random_keyword = configjson.get("random")
repeat_keyword = configjson.get("rep")
httpKeywords = configjson.get("httpKeywords")
httpGet_keyword = httpKeywords.get("get")
httpPost_keyword = httpKeywords.get("post")
cls_keyword = configjson.get("cls")

if os.path.exists(entrypoint):
  with open(entrypoint, 'r') as f:
    code = f.readlines()
    for item in code:
      code[code.index(item)] = item.replace("\n", "")
else:
  print(f"Error: File '{entrypoint}' not found.")
  exit(1)

if debug:  # Debugging
  print("Debug:")
  print("\tConfig.json:")
  for key in configjson:
    if key != "debug":
      print(f"\t\t{key}: {configjson.get(key)}")
  with open(entrypoint, 'r') as f:
    code = f.readlines()
  print(f"\t{entrypoint}:")
  if code != []:
    for line in code:
      line = line.replace('\n', '')
      print(f"\t\t{line}")
  else:
    print(f"\t\t({entrypoint} is empty)")
  print()


def cls():
  os.system('clear')  # Clear screen


if not formatter:
  print(f"{lang_name}™ v{lang_ver}")
  print(f"© {lang_author}, 2024")
  if shell != 1:
    answer = input(f"Do you wish to run {entrypoint}? [Y|N] ")
    if answer.upper() == 'Y':
      cls()  # Clear screen
    else:
      exit(0)
else:
  format.format_code()
  exit(0)

# Dictionaries
vars = {}
ints = {}
macros = {}
lists = {}
dicts = {}

# Lists
proc_names = []
proc_codes = []

# Repeat Statements
repeat_st = 0
repeat_code = []
repeat_times = [0]

# Predefined Variables
do_code = 1
proc = 0


def error(error, line):
  if type(line) == int:
    print(f"{Fore.RED}Error: '{error}' at line {line + 1}")
  else:
    print(f"{Fore.RED}Error: '{error}' at line {line}")
  exit(1)

def p(proc):
  if proc in proc_names:
    procedure = proc_codes[proc_names.index(proc)]
    do_code = 1
    repeat = 0
    for item in procedure:
      lexed, do_code, ntal, repeat = lex(item, do_code, 0, repeat)
      if do_code == 1 and repeat == 0:
        parse(lexed)
  else:
    if shell != 1:
      error("Procedure not found", code.index(line))
    else:
      error("Procedure not found", "<stdin>")


def repeat_statement():
  to_repeat = repeat_times.pop()
  dc = 1
  i = 0
  while i != to_repeat:
    for item in repeat_code:
      lexed, dc, ntal, ntal2 = lex(item, dc, 0, 0)
      if dc == 1:
        parse(lexed)
    i += 1
  repeat_code.clear()


def lex(line, do_code, proc, repeat):
  tokens = []
  lexemes = line.split()
  do_c = do_code
  cur_str = ""
  ignore = 0
  procedure = proc
  rep = repeat

  for lexeme in lexemes:
    if do_c == 1 and procedure == 0 and repeat == 0:
      if ignore != 1:
        # Printing support, basically strings and integers.
        if cur_str != "":
          cur_str.append(lexeme)

          if lexeme.endswith('"'):
            replaced_str = " ".join(cur_str).replace(newline, "\n")
            tokens.append(f'STR:{replaced_str[:-1]}')
        elif lexeme.startswith('"'):
          if lexeme.endswith('"'):
            if lexeme != newline:
              tokens.append(f'STR:{lexeme[1:-1]}')
            else:
              tokens.append(f'STR:\n')
          else:
            cur_str = [lexeme[1:].replace(newline, "")]
        elif lexeme.isdigit():
          tokens.append(f'INT:{int(lexeme)}')
        elif lexeme == newline:
          tokens.append('NEWLINE')
        elif lexeme in (increment_keyword, decrement_keyword):
          ignore = 1
          var_name = lexemes[lexemes.index(lexeme) + 1]
          to_increment = 0
          if len(lexemes) > 2:
            if lexemes[lexemes.index(lexeme) + 2].isdigit():
              to_increment = int(lexemes[lexemes.index(lexeme) + 2])
            else:
              to_increment = ints.get(lexemes[lexemes.index(lexeme) + 2])
          else:
            to_increment = 1
          if var_name in ints:
            if lexeme == increment_keyword:
              ints[var_name] += to_increment
            else:
              ints[var_name] -= to_increment
          else:
            if shell != 1:
              error("Variable not found", code.index(line))
            else:
              error("Variable not found", "<stdin>")
        elif lexeme.startswith(varDelimiter) and lexeme.endswith(varDelimiter):
          if lexeme != '--':
            var_name = lexeme.replace(varDelimiter, '')
            tokens.append(f'VAR:{var_name}')
        elif lexeme.startswith(listDelimiter) and lexeme.endswith(listDelimiter):
          listname = lexemes[lexemes.index(lexeme) + 1]
          if listname in lists:
            tokens.append(f'LIST:{listname}:{lexeme.replace(listDelimiter, "")}')
          else:
            if shell != 1:
              error("List not found", code.index(line))
            else:
              error("List not found", "<stdin>")
        elif lexeme.startswith(dictDelimiter) and lexeme.endswith(dictDelimiter):
          dictname = lexemes[lexemes.index(lexeme) + 1]
          if dictname in dicts:
            tokens.append(f'DICT:{dictname}:{lexeme.replace(listDelimiter, "")}')
          else:
            if shell != 1:
              error("Dictionary not found", code.index(line))
            else:
              error("Dictionary not found", "<stdin>")
        elif lexeme.startswith(macroDelimiter) and lexeme.endswith(
            macroDelimiter):
          mac_name = lexeme.replace(macroDelimiter, '')
          tokens.append(f'MACRO:{mac_name}')
        elif lexeme == print_keyword:
          tokens.append('OP:print')
        # Variables
        elif lexeme in primitive_dt:
          ignore = 1
          var_name = lexemes[lexemes.index(lexeme) + 1]
          var_val = " ".join(lexemes[lexemes.index(lexeme) + 2:])
          # Strings
          if lexeme == primitive_dt[0]:
            if var_name not in vars and var_name not in ints and var_name not in macros and var_name not in lists and var_name not in dicts:
              if var_val.split()[0] == input_keyword:
                vars[var_name] = input(
                    f"{var_val.replace(input_keyword + ' ', '')} - ")
              elif var_val.split()[0] == readKeyword:
                filename = var_val.split()[1]
                if os.path.exists(filename):
                  with open(filename, 'r') as f:
                    vars[var_name] = f.read()
                else:
                  if shell != 1:
                    error("File not found", code.index(line))
                  else:
                    error("File not found", "<stdin>")
              elif var_val.split()[0] == httpGet_keyword:
                reqtype = var_val.split()[1]
                site = var_val.split()[2]
                response = requests.get(site)
                if reqtype == "text":
                  vars[var_name] = response.text
                elif reqtype == "headers":
                  vars[var_name] = response.headers
                elif reqtype == "statusCode":
                  vars[var_name] = response.status_code
              elif var_val.split()[0].startswith(listDelimiter) and var_val.split()[0].endswith(listDelimiter):
                idx = int(var_val.split()[0].replace(listDelimiter, ""))
                listname = var_val.split()[1]
                if listname in lists:
                  vars[var_name] = lists.get(listname)[idx]
                else:
                  if shell != 1:
                    error("List not found", code.index(line))
                  else:
                    error("List not found", "<stdin>")
              elif var_val.split()[0].startswith(dictDelimiter) and var_val.split()[0].startswith(dictDelimiter):
                key = var_val.split()[0].replace(dictDelimiter, "")
                dictname = var_val.split()[1]
                if dictname in dicts:
                  vars[var_name] = dicts.get(dictname).get(key)
                else:
                  if shell != 1:
                    error("Dictionary not found", code.index(line))
                  else:
                    error("Dictionary not found", "<stdin>")
              else:
                vars[var_name] = var_val
            else:
              if shell != 1:
                error(
                    "String variable name is the same as another data type's name or the variable is already defined",
                    code.index(line))
              else:
                error(
                  "String variable name is the same as another data type's name or the variable is already defined",
                    "<stdin>")
          # Integers
          else:
            if var_val.isdigit():
              if var_name not in vars and var_name not in ints and var_name not in macros and var_name not in lists and var_name not in dicts:
                var_val = int(var_val)
                ints[var_name] = var_val
              else:
                if shell != 1:
                  error(
                      "Integer variable name is the same as another data type's name or the integer variable is already defined",
                      code.index(line))
                else:
                  error(
                      "Integer variable name is the same as another data type's name or the integer variable is already defined",
                      "<stdin>")
            else:
              if var_val.split()[0] == input_keyword:
                try:
                  var_val = int(
                      input(f"{var_val.replace(input_keyword + ' ', '')} - "))
                  ints[var_name] = var_val
                except ValueError:
                  if shell != 1:
                    error("Invalid value for integer variable",
                          code.index(line))
                  else:
                    error("Invalid value for integer variable", "<stdin>")
              elif var_val.split()[0] == readKeyword:
                filename = var_val.split()[1]
                if os.path.exists(filename):
                  with open(filename, 'r') as f:
                    try:
                      ints[var_name] = int(f.read())
                    except ValueError:
                      if shell != 1:
                        error("Invalid value for integer variable",
                              code.index(line))
                      else:
                        error("Invalid value for integer variable", "<stdin>")
                else:
                  if shell != 1:
                    error("File not found", code.index(line))
                  else:
                    error("File not found", "<stdin>")
              elif var_val.split()[0] == random_keyword:
                try:
                  item1 = int(var_val.split()[1])
                  item2 = int(var_val.split()[2])
                  var_val = random.randint(item1, item2)
                  ints[var_name] = var_val
                except ValueError:
                  if shell != 1:
                    error("Invalid value for integer variable",
                          code.index(line))
                  else:
                    error("Invalid value for integer variable", "<stdin>")
              elif var_val.split()[0].startswith(listDelimiter) and var_val.split()[0].endswith(listDelimiter):
                idx = int(var_val.split()[0].replace(listDelimiter, ""))
                listname = var_val.split()[1]
                if listname in lists:
                  try:
                    ints[var_name] = int(lists.get(listname)[idx])
                  except ValueError:
                    if shell != 1:
                      error("Invalid value for integer variable",
                            code.index(line))
                    else:
                      error("Invalid value for integer variable", "<stdin>")
                else:
                  if shell != 1:
                    error("List not found", code.index(line))
                  else:
                    error("List not found", "<stdin>")
              elif var_val.split()[0].startswith(dictDelimiter) and var_val.split()[0].startswith(dictDelimiter):
                key = var_val.split()[0].replace(dictDelimiter, "")
                dictname = var_val.split()[1]
                if dictname in dicts:
                  try:
                    ints[var_name] = int(dicts.get(dictname).get(key))
                  except ValueError:
                    if shell != 1:
                      error("Invalid value for integer variable",
                            code.index(line))
                    else:
                      error("Invalid value for integer variable", "<stdin>")
                else:
                  if shell != 1:
                    error("Dictionary not found", code.index(line))
                  else:
                    error("Dictionary not found", "<stdin>")
              else:
                if shell != 1:
                  error("Invalid value for integer variable", code.index(line))
                else:
                  error("Invalid value for integer variable", "<stdin>")
        # Comments
        elif lexeme.startswith(comment_start) or lexeme == comment_start:
          ignore = 1
        # Input
        elif lexeme == input_keyword:
          input(f'{" ".join(lexemes[lexemes.index(lexeme) + 1:])} - ')
        # Setting variables
        elif lexeme == setvar_keyword:
          ignore = 1
          var_name = lexemes[lexemes.index(lexeme) + 1]
          var_val = " ".join(lexemes[lexemes.index(lexeme) + 2:])
          if var_val.startswith(input_keyword):
            var_val = input(f"{var_val.replace(input_keyword + ' ', '')} - ")
          elif var_val.startswith(readKeyword):
            var_val = var_val.replace(f"{readKeyword} ", "")
            if os.path.exists(var_val):
              with open(var_val, 'r') as f:
                var_val = f.read()
            else:
              if shell != 1:
                error("File does not exist", code.index(line))
              else:
                error("File does not exist", "<stdin>")
          elif var_val.startswith(httpGet_keyword):
            reqtype = var_val.split()[1]
            site = var_val.split()[2]
            response = requests.get(site)
            if reqtype == "text":
              var_val = response.text
            elif reqtype == "headers":
              var_val = response.headers
            elif reqtype == "statusCode":
              var_val = response.status_code
          elif var_val.split()[0].startswith(listDelimiter) and var_val.split()[0].endswith(listDelimiter):
            var_val = var_val.split()
            var_val[0] = var_val[0].replace(listDelimiter, '')
            idx = int(var_val[0])
            listname = var_val[1]
            if listname in lists:
              var_val = lists.get(listname)[idx]
            else:
              if shell != 1:
                error("List not found", code.index(line))
              else:
                error("List not found", "<stdin>")
          elif var_val.split()[0].startswith(dictDelimiter) and var_val.split()[0].endswith(dictDelimiter):
            var_val = var_val.split()
            var_val[0] = var_val[0].replace(dictDelimiter, '')
            key = var_val[0]
            dictname = var_val[1]
            if dictname in dicts:
              var_val = dicts.get(dictname).get(key)
            else:
              if shell != 1:
                error("Dictionary not found", code.index(line))
              else:
                error("Dictionary not found", "<stdin>")
          if var_name in vars:
            vars[var_name] = var_val
          elif var_name in ints:
            try:
              ints[var_name] = int(var_val)
            except ValueError:
              error("Invalid value to set integer variable to", "<stdin>")
          else:
            error(f"Unknown variable to set to {var_val}", "<stdin>")
        # Process (basically, Python's exec() but for DrumoScript)
        elif lexeme == process_keyword:
          ignore = 1
          tokens.append(
              f'PROCESS:{" ".join(lexemes[lexemes.index(lexeme) + 1:])}')
        # File I/O
        elif lexeme == createKeyword:
          ignore = 1
          filename = lexemes[lexemes.index(lexeme) + 1]
          with open(filename, 'w') as f:
            f.write("")
            f.close()
        elif lexeme == writeKeyword:
          ignore = 1
          filename = lexemes[lexemes.index(lexeme) + 1]
          to_write = " ".join(lexemes[lexemes.index(lexeme) + 2:])
          with open(filename, 'a') as f:
            f.write(to_write + "\n")
            f.close()
        elif lexeme == resetKeyword:
          ignore = 1
          filename = lexemes[lexemes.index(lexeme) + 1]
          with open(filename, 'w') as f:
            f.write("")
            f.close()
        elif lexeme == mkdirKeyword:
          ignore = 1
          dirname = lexemes[lexemes.index(lexeme) + 1]
          os.mkdir(dirname)
        elif lexeme == emptyKeyword:
          ignore = 1
          dirname = lexemes[lexemes.index(lexeme) + 1]
          for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            if os.path.exists(filepath):
              os.remove(filepath)
        elif lexeme == deleteKeyword:
          ignore = 1
          filename = lexemes[lexemes.index(lexeme) + 1]
          if os.path.exists(filename):
            os.remove(filename)
          else:
            if shell != 1:
              error("File does not exist", code.index(line))
            else:
              error("File does not exist", "<stdin>")
        elif lexeme == rmdirKeyword:
          ignore = 1
          dirname = lexemes[lexemes.index(lexeme) + 1]
          if os.path.exists(dirname):
            os.rmdir(dirname)
          else:
            if shell != 1:
              error("Directory does not exist", code.index(line))
            else:
              error("Directory does not exist", "<stdin>")
        # If Statements
        elif lexeme in (if_keyword, elif_keyword):
          ignore = 1
          var = lexemes[lexemes.index(lexeme) + 1]
          op = lexemes[lexemes.index(lexeme) + 2]
          var_val = " ".join(lexemes[lexemes.index(lexeme) + 3:])
          if var_val.startswith(varDelimiter) and var_val.endswith(varDelimiter):
            rvv = var_val.replace(varDelimiter, "")
            if rvv in vars or rvv in ints or rvv in macros:
              if rvv in vars:
                var_val = vars.get(rvv)
              elif rvv in ints:
                var_val = ints.get(rvv)
              elif rvv in macros:
                var_val = macros.get(rvv)
          if var_val.isdigit():
            var_val = int(var_val)
          if var in vars or var in ints or var in macros:
            pass
          else:
            if shell != 1:
              error("Variable not found", code.index(line))
            else:
              error("Variable not found", "<stdin>")
          if var in vars:
            if op == '=':
              do_c = 1 if vars.get(var) == var_val else 0
            elif op == '!':
              do_c = 1 if vars.get(var) != var_val else 0
          elif var in ints:
            try:
              if op == '=':
                do_c = 1 if ints.get(var) == int(var_val) else 0
              elif op == '<':
                do_c = 1 if ints.get(var) <= int(var_val) else 0
              elif op == '>':
                do_c = 1 if ints.get(var) >= int(var_val) else 0
              elif op == '!':
                do_c = 1 if ints.get(var) != int(var_val) else 0
            except ValueError:
              if shell != 1:
                error("Invalid value", code.index(line))
              else:
                error("Invalid value", "<stdin>")
          elif var in macros:
            if op == '=':
              do_c = 1 if macros.get(var) == var_val else 0
            elif op == '!':
              do_c = 1 if macros.get(var) != var_val else 0
        elif lexeme == else_keyword:
          do_c = 1 - do_c
        elif lexeme == end_keyword:
          do_c = 1
        # Procedures
        elif lexeme == proc_keyword:
          procedure = 1
          proc_name = lexemes[lexemes.index(lexeme) + 1]
          proc_names.append(proc_name)
          proc_codes.append([])
          break
        elif lexeme == call_keyword:
          ignore = 1
          pte = lexemes[lexemes.index(lexeme) + 1]
          p(pte)
        # Concatenation
        elif lexeme == concat_keyword:
          ignore = 1
          var = lexemes[lexemes.index(lexeme) - 1]
          to_concat = lexemes[lexemes.index(lexeme) + 1]
          if var in vars:
            vars[var] += ' ' + to_concat
          else:
            if shell != 1:
              error("Variable not found", code.index(line))
            else:
              error("Variable not found", "<stdin>")
        # String Removal
        elif lexeme == remove_keyword:
          ignore = 1
          var = lexemes[lexemes.index(lexeme) - 1]
          to_remove = lexemes[lexemes.index(lexeme) + 1]
          if var in vars:
            vars[var] = vars[var].replace(to_remove, '')
          else:
            if shell != 1:
              error("Variable not found", code.index(line))
            else:
              error("Variable not found", "<stdin>")
        # Including Files
        elif lexeme == import_keyword:
          import_filepath = lexemes[lexemes.index(lexeme) + 1]
          if os.path.exists(f"std/{import_filepath}.dms"):
            with open(f"std/{import_filepath}.dms", "r") as f:
              c = f.readlines()
              for item in c:
                c[c.index(item)] = c[c.index(item)].replace("\n", "")
              f.close()
            for item in c:
              if item.startswith("proc "):
                proc_names.append(item.replace("proc ", ""))
                proc_codes.append([])
              else:
                if item != "endp":
                  proc_codes[-1].append(item)
          else:
            if shell != 1:
              error("File to include not found", code.index(line))
            else:
              error("File to include not found", "<stdin>")
        # Macros
        elif lexeme == macro_keyword:
          ignore = 1
          macro_name = lexemes[lexemes.index(lexeme) + 1]
          macro_val = lexemes[lexemes.index(lexeme) + 2:]
          macro_val = ' '.join(macro_val)
          if macro_val.isdigit():
            macro_val = int(macro_val)
          if not macro_name in vars and not macro_name in ints and not macro_name in lists and not macro_name in macros:
            macros[macro_name] = macro_val
          else:
            if shell != 1:
              error("Macro name is the same as another data type's name", code.index(line))
            else:
              error("Macro name is the same as another data type's name", "<stdin>")
        # Repeat Statements
        elif lexeme == repeat_keyword:
          repeat_time = lexemes[lexemes.index(lexeme) + 1]
          if repeat_time.isdigit():
            repeat_time = int(repeat_time)
          else:
            if repeat_time in ints:
              repeat_time = int(ints.get(repeat_time))
            else:
              if shell != 1:
                error("Invalid amount to repeat", code.index(line))
              else:
                error("Invalid amount to repeat", "<stdin>")
          repeat_times.append(repeat_time)
          rep = 1
          ignore = 1
        # Lists
        elif lexeme == list_keyword:
          ignore = 1
          listname = lexemes[lexemes.index(lexeme) + 1]
          listvals = lexemes[lexemes.index(lexeme) + 2:]
          if listname not in (vars, ints, macros, lists, dicts):
            lists[listname] = []
            value = []
            for item in listvals:
              if item != '-':
                value.append(item)
              else:
                if not " ".join(value).isdigit():
                  lists.get(listname).append(" ".join(value))
                else:
                  lists.get(listname).append(int(value[0]))
                value = []
            if not " ".join(value).isdigit():
              lists.get(listname).append(" ".join(value))
            else:
              lists.get(listname).append(int(value[0]))
            value = []
          else:
            if shell != 1:
              error("List name is the same as another data type's name", code.index(line))
            else:
              error("List name is the same as another data type's name", "<stdin>")
        # Dictionaries
        elif lexeme == append_keyword:
          ignore = 1
          listname = lexemes[lexemes.index(lexeme) + 1]
          value = lexemes[lexemes.index(lexeme) + 2:]
          textval = " ".join(value)
          if textval.isdigit():
            textval = int(textval)
          if listname in lists:
            lists.get(listname).append(textval)
          else:
            if shell != 1:
              error("List not found", code.index(line))
            else:
              error("List not found", "<stdin>")
        elif lexeme == dict_keyword:
          ignore = 1
          dictname = lexemes[lexemes.index(lexeme) + 1]
          if dictname not in (vars, ints, macros, lists, dicts):
            value = lexemes[lexemes.index(lexeme) + 2:]
            dicts[dictname] = {}
            textval = []
            keyname = 1
            key_name = ""
            for item in value:
              if keyname == 1:
                key_name = item
                keyname = 0
              else:
                if item != '-':
                  textval.append(item)
                else:
                  dicts.get(dictname)[key_name] = " ".join(textval)
                  textval = []
                  key_name = ""
                  keyname = 1
            dicts.get(dictname)[key_name] = " ".join(textval)
            textval = []
            key_name = ""
            keyname = 1
          else:
            if shell != 1:
              error("Dictionary name is the same as another data type's name", code.index(line))
            else:
              error("Dictionary name is the same as another data type's name", "<stdin>")
        elif lexeme == httpPost_keyword:
          ignore = 1
          url = lexemes[lexemes.index(lexeme) + 1]
          data = lexemes[lexemes.index(lexeme) + 2]
          if data in dicts:
            data = dicts.get(data)
            response = requests.post(url, json=data)
            if debug:
              print("[HTTP Post request made. Data recieved:")
              print("(TEXT):")
              print(response.text)
              print("(HEADERS):")
              print(response.headers)
              print(f"(STATUS CODE):\n{response.status_code}")
              try:
                print("(JSONIFIED):")
                print(response.json())
              except:
                print("(Could not retrieve JSON data for reasons)")
              finally:
                print("]")
          else:
            if shell != 1:
              error("Dictionary not found", code.index(line))
            else:
              error("Dictionary not found", "<stdin>")
        # Clear Screen
        elif lexeme == cls_keyword:
          cls()
          ignore = 1
        # Wait
        elif lexeme == wait_keyword:
          ignore = 1
          time_to_wait = lexemes[lexemes.index(lexeme) + 1]
          if isinstance(time_to_wait, str) and not time_to_wait.isdigit():
            try:
              time_to_wait = ints.get(time_to_wait)
            except:
              if shell != 1:
                error("Could not find int variable to wait", code.index(line))
              else:
                error("Could not find int variable to wait", "<stdin>")
          else:
            time_to_wait = int(time_to_wait)
          time.sleep(time_to_wait)
      elif ignore == 1 and (lexeme.startswith(comment_end)
                            or lexeme == comment_end):
        ignore = 0
    elif do_c == 0 and lexeme == end_keyword:
      do_c = 1
    elif do_c == 0 and lexeme == elif_keyword:
      ignore = 1
      var = lexemes[lexemes.index(lexeme) + 1]
      op = lexemes[lexemes.index(lexeme) + 2]
      var_val = " ".join(lexemes[lexemes.index(lexeme) + 3:])
      if var_val.startswith(varDelimiter) and var_val.endswith(varDelimiter):
        rvv = var_val.replace(varDelimiter, "")
        if rvv in vars or rvv in ints or rvv in macros:
          if rvv in vars:
            var_val = vars.get(rvv)
          elif rvv in ints:
            var_val = ints.get(rvv)
          elif rvv in macros:
            var_val = macros.get(rvv)
      if var in vars or var in ints or var in macros:
        pass
      else:
        if shell != 1:
          error("Variable not found", code.index(line))
        else:
          error("Variable not found", "<stdin>")
      if var in vars:
        if op == '=':
          do_c = 1 if vars.get(var) == var_val else 0
        elif op == '!':
          do_c = 1 if vars.get(var) != var_val else 0
      elif var in ints:
        try:
          if op == '=':
            do_c = 1 if ints.get(var) == int(var_val) else 0
          elif op == '<':
            do_c = 1 if ints.get(var) <= int(var_val) else 0
          elif op == '>':
            do_c = 1 if ints.get(var) >= int(var_val) else 0
          elif op == '!':
            do_c = 1 if ints.get(var) != int(var_val) else 0
        except ValueError:
          if shell != 1:
            error("Invalid value", code.index(line))
          else:
            error("Invalid value", "<stdin>")
      elif var in macros:
        if op == '=':
          do_c = 1 if macros.get(var) == var_val else 0
        elif op == '!':
          do_c = 1 if macros.get(var) != var_val else 0
      else:
        if shell != 1:
          error("Variable not found", code.index(line))
        else:
          error("Variable not found", "<stdin>")
    elif do_c == 0 and lexeme == else_keyword:
      do_c = 1 - do_c
    elif procedure == 1 and lexeme == endp_keyword:
      procedure = 0
    elif procedure == 1:
      proc_codes[0].append(line.replace("\n", ""))
      break
    elif rep == 1 and lexeme == endr_keyword:
      rep = 0
      repeat_statement()
      break
    elif rep == 1:
      repeat_code.append(line.replace("\n", ""))
      break
  return tokens, do_c, procedure, rep


def parse(tokens):
  to_parse = []
  for tok in tokens:
    if tok.startswith('STR:'):
      to_parse.append(tok)
    elif tok.startswith('INT:'):
      to_parse.append(tok.replace('INT:', ''))
    elif tok.startswith(('OP:', 'VAR:', 'MACRO:', 'LIST:', 'DICT:')):
      to_parse.append(tok)
    elif tok.startswith('PROCESS:'):
      to_parse.append(f'PROCESS {" ".join(tokens).replace("PROCESS:", "")}')
  for item in to_parse:
    if item.startswith('OP:'):
      if item.endswith('print'):
        to_print = to_parse[1]
        to_print = to_print.replace('STR:', '').replace("-nl-", "\n")
        if to_print.isdigit():
          to_print = int(to_print)
        elif to_print == 'NEWLINE':
          to_print = "\n"
        elif to_print.startswith('VAR:'):
          to_print = to_print.replace('VAR:', '')
          if to_print in vars:
            to_print = vars.get(to_print)
          elif to_print in ints:
            to_print = ints.get(to_print)
        elif to_print.startswith('LIST:'):
          to_print = to_print.replace(":", " ").replace('LIST', '').split()
          if to_print[1].replace(listDelimiter, "").isdigit():
            idx = int(to_print[1])
          else:
            if to_print[1].replace(listDelimiter, "") in ints:
              idx = ints.get(to_print[1].replace(listDelimiter, ""))
            else:
              if shell != 1:
                error("Variable not found", code.index(line))
              else:
               error("Variable not found", "<stdin>")
          listname = to_print[0]
          to_print = lists.get(listname)[idx]
        elif to_print.startswith('DICT:'):
          to_print = to_print.replace(":", " ").replace('DICT', '').split()
          key = to_print[1].replace(dictDelimiter, '')
          dict = to_print[0]
          to_print = dicts.get(dict).get(key)
        elif to_print.startswith('MACRO:'):
          to_print = to_print.replace('MACRO:', '')
          if to_print in macros:
            to_print = macros.get(to_print)
        elif 'NEWLINE' in to_print:
          to_print = to_print.replace('NEWLINE', '\n')
        print(to_print)
    elif item.startswith('PROCESS'):
      process = item.replace('PROCESS ', '')
      if process.startswith(varDelimiter) and process.endswith(varDelimiter):
        process_name = process.replace(varDelimiter, '')
        if process_name in vars:
          process = vars[process_name]
          lexed_process, ntal, ntal2, ntal3 = lex(process, 0, 0, 0)
          parse(lexed_process)
        else:
          if shell != 1:
            error("Invalid process", code.index(line))
          else:
            error("Invalid process", "<stdin>")
      else:
        lexed_process, not_to_agitate_lex, ntal2, ntal3 = lex(process, 0, 0, 0)
        parse(lexed_process)

if shell != 1:
  for line in code:
    lexed, do_code, proc, repeat_st = lex(line, do_code, proc, repeat_st)
    if do_code == 1 and proc == 0 and repeat_st == 0:
      parse(lexed)
else:
  while True:
    inp = input(f"{shell_name} > ")
    lexed, do_code, proc, repeat_st = lex(inp, do_code, proc, repeat_st)
    if do_code == 1 and proc == 0 and repeat_st == 0:
      parse(lexed)