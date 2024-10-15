class Token:
    def __init__(self, category, value = None):
        self.category = category
        self.value = value
    def __repr__(self):
        if self.value is None:
            return self.category + " token"
        else:
            return self.category + " token: " + str(self.value)
def parse(tokens):
    mods = {}
    simple = {}
    tabs = [0]
    state = ""
    substate = ""
    keywords = ["complex","from","man","opt","mod","to","to_if_alone","to_if_held_down","to_after_key_up",
                "conditions","metadata"]
    secondaries = ["man", "opt", "mod"]
    
    for line in tokens:
        for i, token in enumerate(line):
            if state == "":
                if line[0].category == "keyword":
                    #determine if keyword is complex and set state
                    pass
                elif line[0].category == "var":
                    #get simple modification
                    pass
                else:
                    raise SyntaxError(f"Cannot start line with {line[0].category}")
            elif state == "complex":
                pass
            
def tokenize(lines):
    tokens = []
    wordchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    digits = "1234567890"
    keywords = ["complex","from","man","opt","mod","to","to_if_alone","to_if_held_down","to_after_key_up",
                "conditions","metadata"]
    for line in lines:
        state = "start"
        substate = ""
        current = ""
        tokens.append([])
        for i, char in enumerate(line):
            if state == "start":
                if char == " ":
                    continue
                if i != 0:
                    tokens[-1].append(Token("tab",i))
                if char in wordchars:
                    state = "name"
                    current = char
                elif char == "\n":
                    ipass
                    tokens[-1].append(Token("newline"))
                elif char == "'" or char == '"':
                    state = "string"
                    substate = char
                elif char == "[":
                    tokens[-1].append(Token("open bracket"))
                    state = "list"
                    current = char
                elif char in digits:
                    state = "int"
                    current = char
                elif char == ":":
                    tokens[-1].append(Token("colon"))
                else:
                    raise SyntaxError(f"Invalid character '{char}' in line {i}:\n{line}")
            elif state == "":
                if char == " ":
                    pass
                elif char == "'" or char == '"':
                    state = "string"
                    substate = char
                elif char == "[":
                    tokens[-1].append(Token("open bracket"))
                    state = "list"
                elif char in wordchars:
                    state = "name"
                    current = char
                elif char in digits:
                    state = "int"
                    current = char
                elif char == ":":
                    tokens[-1].append(Token("colon"))
                elif char == "\n":
                    tokens[-1].append(Token("newline"))
                else:
                    raise SyntaxError(f"Invalid character '{char}' in line {i}:\n{line}")
            elif state == "name":
                if char in wordchars:
                    current += char
                elif char == ":":
                    if current in keywords:
                        tokens[-1].append(Token("keyword",current))
                    else:
                        tokens[-1].append(Token("var",current))
                    tokens[-1].append(Token("colon"))
                    substate = ""
                    current = ""
                    state = ""
                elif char == " ":
                    if current in keywords:
                        tokens[-1].append(Token("keyword",current))
                    else:
                        tokens[-1].append(Token("var",current))
                    current = ""
                    state = ""
                    substate = ""
                elif char == "\n":
                    if current != "":
                        if current in keywords:
                            tokens[-1].append(Token("keyword",current))
                        else:
                            tokens[-1].append(Token("var",current))
                    tokens[-1].append(Token("newline"))
                else:
                    raise SyntaxError(f"Invalid character '{char}' for keyword in line {i}:\n{line}")

            elif state == "string":
                if char != substate:
                    current += char
                    if char == "\n":
                        raise SyntaxError(f"String literal unterminated in line {i}:\n{line}")
                elif char == substate:
                    tokens[-1].append(Token("string",current))
                    current = ""
                    state = ""
                    substate = ""
            elif state == "int":
                if char in digits:
                    current += char
                elif char == " " or char == "\n":
                    tokens[-1].append(Token("int",current))
                    tokens[-1].append(Token("newline"))
                    state = ""
                else:
                    raise SyntaxError(f"Invalid character '{char}' for int in line {i}:\n{line}")
            elif state == "list":
                if substate == "":
                    if char == "'" or char == '"':
                        substate = char
                    elif char == ",":
                        tokens[-1].append(Token("comma"))
                    elif char == "]":
                        tokens[-1].append(Token("close bracket"))
                        state = ""
                    elif char == "\n":
                        raise SyntaxError(f"No close bracket in line {i}:\n{line}")
                    else:
                        raise SyntaxError(f"Invalid character '{char}' for a list in line {i}:\n{line})")
                elif substate == '"' or substate == "'":
                    if char == substate:
                        tokens[-1].append(Token("string",current))
                        substate = ""
                    else:
                        current += char
    return tokens

if __name__ == "__main__":                        
    lines = open("code.kb","r").readlines()
    tokens = tokenize(lines)
    for i in tokens:
        print(i)
    parse(tokens)
