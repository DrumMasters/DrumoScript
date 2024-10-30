# DRUMOSCRIPT
  DrumoScript is a *new, revised, and improved* version of DrumLang,
with similar syntax.

```java
//////////////////////////////
//////////////////////////////
//////////////////////////////
////////////#######////######/
////////////#//////#//#///////
////////////#//////#//#///////
////////////#//////#///######/
////////////#//////#/////////#
////////////#//////#/////////#
////////////#######////######/
//////////////////////////////
```

## TABLE OF CONTENTS

- [Features](FEATURES)
- [Examples](EXAMPLES)
- [DrumoForm](DRUMOFORM)
- [DrumoThon](DRUMOTHON)
- [DrumAI](DRUMAI)
- [DrumByte](DRUMBYTE)
- [Contributing](CONTRIBUTING)
- [License](LICENSE)

## FEATURES

| Basics           | Variables                      | Comments        |
| ---------------- | ------------------------------ | --------------- |
| Printing         | Strings                        | Normal Comments |
| Escape Sequences | Integers                       | Inline Comments |
| Input            | Incrementation/decrementation  |                 |
| CLS Function     | String Concatenation           |                 |
| Wait command     | Randomness                     |                 |
|                  | HTTP Requests                  |                 |
|                  | Lists                          |                 |
|                  | Dictionaries                   |                 |

### ADVANCED FEATURES

#### VARIABLE-RELATED:

| Macros             |
| ---------------------------------------------------------------- |
| Permanent variables that can't be changed (basically, constants) |

#### LOOPS:

| Repeat Statements                         |
| ----------------------------------------- |
| Repeat some code a certain amount of time |

#### EXECUTE CODE:

| Processes                                  |
| ------------------------------------------ |
| Execute DrumoScript Code in DrumoScript    |
| Execute DrumoScript Code from Variables    |
| Create processes inside processes          |

#### FILE RELATED:

| File I/O                             |
| ------------------------------------ |
| Creating files                       |
| Writing to files                     |
| Resetting files                      |
| Creating folders                     |
| Deleting every file in folders       |
| Deleting files                       |
| Deleting folders                     |
| Reading from files                   |

| File Inclusion                       |
| ------------------------------------ |
| Include custom .dms files from std   |

#### CONDITIONAL STATEMENTS:

| If Statements                        |
| ------------------------------------ |
| If statement (if)                    |
| Elif statement (elif)                |
| Else statement                       |
| '=' operator                         |
| '<' operator                         |
| '>' operator                         |

#### WEB-RELATED:

| HTTP Post requests                   |
| ------------------------------------ |
| Post data to websites                |
| Get received data (debug only)       |

## EXAMPLES

### PRINT

To print a simple message, use the 'print' keyword followed by the message enclosed in double-quotes:

```drumoscript
print "Hello, World!"
```

You can also print variables:
```drumoscript
str name Drum
print "Hello,"
print -name-
```

You could also print Macros (mentioned later):

```drumoscript
define Macro Hello!
print ~Macro~
```

There are also escape sequences:
```drumoscript
print "Hello, World! -nl-"
```
This example is a newline. More escape sequences will be added soon.

### INPUT

To create an input prompt, use the 'stdin' keyword followed by the message:

```drumoscript
stdin Hey there! How are you?
```

You can also set variables to input:
```drumoscript
str input stdin Enter a word
print -input-
```

### CLS

Clearing the screen can be quite useful when you're making a cutscene for games.

To clear the screen (CLS), you'd use the "cls" keyword (pretty straightforward):

```drumoscript
cls
```

### WAIT COMMAND

Waiting a certain amount of time can be good if you need it.

To wait a certain amount of time, you'd use the "wait" keyword followed by the amount of time to wait (in seconds):

```drumoscript
wait [seconds, can be a variable too]
```

### VARIABLES

Variables hold values that can be of different types.

#### STRINGS
You can declare string variables using the 'str' keyword, followed by the name and the value:

```drumoscript
str String Hello, World!
```

#### INTEGERS
You can declare integer variables using the 'int' keyword, followed by the name and the value:

```drumoscript
int Integer 5
```

#### INCREMENTATION/DECREMENTATION
You can also increment/decrement integer variables. To increment a variable, you'd use the '++' keyword followed by the variable's name:

```drumoscript
int Integer 5
++ Integer
```
In this example, we increment an integer by 1.

To decrement a variable, you'd use the '--' keyword followed by the variable's name:

```drumoscript
int Integer 5
-- Integer
```

In this example, we decrement an integer by 1.

Optionally, you can also increment/decrement by a certain amount:

```drumoscript
int Integer 5
++ Integer 5
```

In this example we increment "Integer" by 5.

```drumoscript
int Integer 5
-- Integer 5
```

In this example we decrement "Integer" by 5.

#### STRING CONCATENATION
You can also concatenate (and remove parts from) strings.

To concatenate a string to a string variable, you'd use the variable name, followed by '+=' and the text you want to concatenate:

```drumoscript
str Text This is some
Text += Testing text
print -Text-
```
In this example, we create a variable named 'Text', we assign it a value of 'This is some', concatenate 'Testing text' to it and then print Text.

To remove a part from a string variable, you'd use the variable name, followed by '-=' and the text you want to remove:

```drumoscript
str Text This is some testing text
Text -= testing text
print -Text-
```

In this example, we create a variable named 'Text', we assign it a value of 'This is some testing text', remove 'testing text' from it and then print Text.

#### RANDOMNESS
Randomness only works with integer variables, it can give you any random amount.
To declare a random integer variable, you use the "rand" keyword followed by 2 numbers:
```drumoscript
int Random rand 1 10
print -Random-
```

In this example, we create an int variable named "Random", assign it a random value between 1 to 10, and then print it.

#### HTTP REQUESTS
HTTP requests are a way to get/post data to websites. Currently, you can only get data to set variables to.
 
To get data from a site, you'd use the "httpget" keyword, followed by the type of data you want to get, and the site you want to get it from:

```drumoscript
str HTTPReq httpget text https://example.com/data
print -HTTPReq- << Print the text of the HTTP request >>
set HTTPReq httpget headers https://example.com/data
print -HTTPReq- << Print the HEADERS of the HTTP request >>
set HTTPReq httpget statusCode https://example.com/data
print -HTTPReq- << Print the status code of the HTTP request >>
```

In this example we get the text, headers and status code of a website, and then print all of it.

#### LISTS
Lists are a type of variable that can store multiple items in it.

To declare a list, you'd use the "list" keyword, followed by the list name and list values (separated by a -):
```drumoscript
list List Hello, - World!
print |0| List
print |1| List
```
In this example, we declare a list and name it "List", and we give it 2 values, "Hello," and "World!". Then we print the 2 items.

#### DICTIONARIES
Dictionaries (or hashmaps) are another type of lists which have a key-value pair.
To declare a dictionary, you'd use the "dict" keyword followed by the dictionary name and its values (separated by a -):
```drumoscript
dict Dict key1 Hello, - key2 World!
print %key1% Dict
print %key2% Dict
```
In this example, we declare a dictionary named "Dict" and assign it 2 key-avlue pairs, key1 is "Hello," and key2 is "World!". Then we print key1 and key2.

### COMMENTS

Comments are programmer-readable lines which explain how the code works.

#### NORMAL COMMENTS
You can create comments by doing this:

```drumoscript
<< Comment! >>
```

#### INLINE COMMENTS
You can create inline comments like this (for example):

```drumoscript
<< Inline >> print << Comments! >> "Comments"
```

And it won't interrupt the statement at all.
It only works with print statements, though!

### INCLUDE

You can also include DrumoScript files, which allows making large programs.
To include a file, you'd use the "include" keyword, followed by the file's name (excluding .dms):

```drumoscript
include fileToInclude

<< For example, if you had a "HelloWorld" procedure in it: >>
exec HelloWorld
```
In this example, we include "fileToInclude.dms", and then execute the "HelloWorld" procedure.

### MACRO
Macros are permanent variables (basically, constants).

To define a macro, you'd use the "define" keyword followed by the macro name and macro value:

```drumoscript
define Macro Hey I'm a macro!
print ~Macro~
if Macro = Hey I'm a macro!
print "A macro is a macro."
end
```
In this example, we define a macro "Macro" and assign it a value of "Hey I'm a macro!". Then we print the macro's value. We also check if the macro's set to "Hey I'm a macro!" and if it is, we print "A macro is a macro."

### REPEAT STATEMENTS
Repeat statements are statements that allow you to repeat some code a certain amount of times. To declare one, you'd use the 'repeat' keyword followed by the amount of times you want to repeat it, the code (on a new line) and 'endr':

```drumoscript
int i 0

repeat 10
print "Hello!"
print -i-
++ i
endr
```

In this example, we declare an integer "i", assign it a value of 0, and we print "Hello!", we print i and we increment i by 1 (10 times).

### PROCESS

The 'process' keyword is used to execute DrumoScript code in DrumoScript.
You can use the 'process' keyword like this:

```drumoscript
process print "Hello"
```

which is the DrumoScript alternative to:
```python
exec('print("Hello")')
```

In this example, it prints "Hello". You can also do that normally, but then there's also the alternative option, executing code from variables:

```drumoscript
str HelloProcess print "Hello"
process -HelloProcess-
```

which is the DrumoScript alternative to:
```python
HelloProcess = 'print("Hello")'
exec(HelloProcess)
```

In this exmaple, it does the same thing.

### FILE I/O

File I/O (file input/output) is a way of interacting with external data sources.

To create a file, you would use the 'create' keyword followed by the file name:

```drumoscript
create file.extension
```

To write to a file, you'd use the 'write' keyword followed by the file name and the text you'd like to write to the file:

```drumoscript
write file.extension text you'd like to write
```

To reset a file's contents to nothing, you'd use the 'reset' keyword, followed by the file's name:

```drumoscript
reset file.extension
```
This can be pretty dangerous, though.

To delete a file, you'd use the 'delete' keyword, followed by the file's name:

```drumoscript
delete file.extension
```

To create a folder, you'd use the 'mkdir' keyword, followed by the folder name:

```drumoscript
mkdir foldername
```

To delete a folder's contents, you'd use the 'empty' keyword followed by the folder name:

```drumoscript
empty foldername
```

To delete a folder entirely, you'd use the 'rmdir' keyword followed by the folder name:

```drumoscript
rmdir foldername
```

To read from a file, you'd use the 'read' keyword followed by the file name:

```drumoscript
str Hello read file.extension

print -Hello-
```

### IF STATEMENTS

If statements are crucial in programming languages, and we've implemented them.

#### IF

To declare an if statement, you'd use the 'if' keyword, followed by
the variable, the operator and the value:

```drumoscript
str Hello Hello!

if Hello = Hello!
print "Hello is set to 'Hello!'."
end
```

In this example, we declare a variable named "Hello" with a value of "Hello!", and we check if the value is set to "Hello!". If it is, it prints "Hello is set to 'Hello!'."

#### ELIF

To declare an elif statement, you'd use the 'elif' keyword, followed by the variable, the operator and the value:

```drumoscript
str Hello Hello!

if Hello = Hi!
print "Hello is set to 'Hi!'."
elif Hello = Hello!
print "Hello is set to 'Hello!'."
end
```

In this example, we declare a variable named "Hello" with a value of "Hello!", and we check if the value is set to "Hi!". If it is, it prints "Hello is set to 'Hi!'.", otherwise if it is set to "Hello!", we print "Hello is set to 'Hello!'."

#### ELSE

To declare an else statement, you'd use the 'else' keyword:

```drumoscript
str Hello Hello!

if Hello = Hi!
print "Hello is set to 'Hi!'."
elif Hello = Greetings!
print "Hello is set to 'Greetings!'."
else
print "Hello is set to 'Hello!'."
end
```

In this example, we declare a variable named "Hello" with a value of "Hello!", and we check if the value is set to "Hi!". If it is, it prints "Hello is set to 'Hi!'.", otherwise if it is set to "Greetings!", we print "Hello is set to 'Greetings!'.", otherwise we print "Hello is set to 'Hello!'."

### PROCEDURES
Procedures are basically functions.
To make a procedure, you'd use the 'proc' keyword followed by the procedure name:
```drumoscript
proc ProcName
print "Hello!"
end
```

To execute a procedure, you'd use the 'exec' keyword followed by the procedure name:
```drumoscript
proc ProcName
print "Hello!"
end

exec ProcName
```

### HTTP POST REQUESTS
Post requests are types of requests that you use to post something to a site.
To post something to a site, you'd use the 'httppost' keyword followed by the site and a data dictionary:

```drumoscript
dict data message1 Hello, - message2 World!
httppost https://example.site.com data
```
In this example, we post 2 items to a website, "message1" and "message2".

And that's every single example!

## DRUMOFORM
DrumoForm is DrumoScript's new custom formatter program, used to add readability to your code (ONLY USE WHEN CODE IS NOT WRITTEN WITH INDENTATION).

To use it, simply go to the config.json file and set the "formatter" option to "true".
Then, once you run your project, you will see instead of being ran, you'll find a preview of the formatted code.
You will also be able to chose between using spaces and indents.
If you select "Y" after the preview's been displayed, your code should be formatted.

### EXAMPLE

For example, if I have this complex, barely-readable code:

```drumoscript
proc rep
int i 0
repeat 10
++ i
print -i-
if i = 10
print "I is equal to 10"
else
print "I is not equal to 10"
end
endr
endp

exec rep
```

I can simply turn on the formatter option, and wha-bam, the formatter will output this:

```drumoscript
proc rep
  int i 0

  repeat 10

    ++ i
    print -i-


    if i = 10

      print "I is equal to 10"

    else

      print "I is not equal to 10"

    end
  endr
endp

exec rep

```

And that's mostly all there is to it!

## CONTRIBUTING

If you want to contribute to the project in any way, you can suggest features, fork the project (only if you're suggesting features), make your own superset of DrumoScript, etc.

## LICENSE

### This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.

### Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "DrumoScript"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the DrumoScript, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

### The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Definitions:
- "DrumoScript" means the Software.
- "Authors" means the creators of the DrumoScript.
- "License" means this document.
- "Software" means DrumoScript.

### Indemnification:
The user acknowledges that the Authors provide the Software "as is" and without any express or implied warranties. The user agrees that the Authors shall not be liable for any damages arising from the use of the Software.

### Permission:
Permission is hereby granted to any person obtaining a copy of the Software to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

1. The user must include the above copyright notice, this permission notice, and this license in all copies or substantial portions of the Software.

2. The user agrees to indemnify, defend, and hold harmless the Authors from and against any claims or liabilities arising from the use of the Software.

3. The user agrees not to use the names, trademarks, or other identifying marks of the Authors for endorsements or promotions of any derivative works without prior written permission.

### Termination:
This License shall continue in effect unless terminated by the user. Upon termination, the user must cease all use of the Software and destroy all copies of the Software in their possession.

### Contributions:
Contributions to the Software may be made under the terms of this License. By contributing to the Software, the contributor agrees to license their contributions under the terms of this License.