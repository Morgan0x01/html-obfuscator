import re
import sys
import string
import random
import base64 
import hashlib
from bs4 import BeautifulSoup

alphanum = string.ascii_lowercase + string.digits


# #-------------------------- Inputs --------------------------
# html_file_name = input("Enter name of HTML file to be Obfuscated: ")

#-------------------------- Regex --------------------------
pattern = re.compile(r">([^<>].*?)<")  # Compile RegEx pattern(To match HTML Text nodes)
html_entity = re.compile(r"&[a-zA-Z0-9#]{1,};")
non_white = re.compile("([^\s]){1,}")

#-------------------------- Comment Inject --------------------------
def insertComment(letter):
    mod = "<!--" + str(random.sample(alphanum, 3)) + "-->"
    comm = "<!--" + str(random.sample(alphanum, 3)) + "-->"
    mod += letter + comm
    return mod

#-------------------------- Zerofont Inject --------------------------
def insertTransparentfont(word):
    mod = ""
    for i in word:
        comm = '<span style="display:none !important;font-size:0px;line-height:0;color:#ffffff;visibility:hidden;opacity:0;height:0;width:0;mso-hide:all">' + str(random.sample(alphanum, 3)) + '</span>'
        mod += i + comm

#-------------------------- Transparent Font Inject --------------------------
def insertZeroFont(word):
    mod = ""
    for i in word:
        comm = '<span style="font-size:0px;line-height:0;color:#ffffff;visibility:hidden;opacity:0;height:0;width:0;mso-hide:all">' + str(random.sample(alphanum, 3)) + '</span>'
        mod += i + comm
    
#-------------------------- Invisible Tags Inject --------------------------
def insertDisplayNone(word):
    mod = ""
    for i in word:
        comm = '<span style="display:none !important;">' + str(random.sample(alphanum, 3)) + '</span>'
        mod += i + comm

#-------------------------- Convert string to HTML Decimal entity --------------------------
def convertToDecimalEntity(word):
    decimal_entities = ""
    
    for char in word:
        decimal_entities += f"&#{ord(char)};"

#-------------------------- Convert string to HTML HexaDecimal entity --------------------------
def convertToHexadecimalEntity(word):
    hexadadecimal_entities = ""
    
    for char in word:
        hexadadecimal_entities += f"&#x{format(ord(char),'x')}"

#-------------------------- Handler --------------------------
def handler(matches, iterables, content):
    #for match in matches:
    new_length = 0
    for x in iterables:
        #print(match)
        #if match.isspace():
        match = content[x[0]+new_length:x[1]+new_length]
        print(match)
        match_length = len(match)
        if match.isspace():
            continue
        else:
            new = ""
            #if re.search("&[a-zA-Z0-9#]{1,};", match) is not None: #Match HTML entities
            if re.search("&[a-zA-Z0-9#]{1,};", match) is not None: #Match HTML entities
                #indexes = re.finditer("&[a-zA-Z0-9#]{1,};", match) # Array  of matched HTML entitiy indexes(tuples)
                indexes = re.finditer("&[a-zA-Z0-9#]{1,};", match) # Array  of matched HTML entitiy indexes(tuples)
                expanded = [] #List of expanded tuples of HTML entity indexes

                for i in indexes:
                    for r in range(i.start(), i.end()):
                        expanded.append(r)
                print(f"Expanded: {expanded}") #FOR Test, REMOVE Later

                for spot in range(len(match)):
                    if spot in expanded:
                        new += match[spot]
                        continue
                    else:
                        new += insertComment(match[spot])
                expanded.clear()
            else:
                for g in match:
                    new += insertComment(g)
        #content = content.replace(match, new)
        #content = content[:x[0]-1] + new + content[x[1]+1:]
        content = content[:x[0]+new_length] + new + content[x[1]+new_length:]
        new_length = new_length + len(new)

    with open("output.html", 'w', encoding="utf-8") as out:
        out.write(content)
    
#-------------------------- Create HTML Injection --------------------------
with open(html_file_name, 'r', encoding="utf-8") as html_file:
    content = html_file.read()
    #match = re.search(r">([^<>].*?)<", content, re.DOTALL) # Matches pattern including newlines
    matches = re.findall(r">([^<>].*?)<", content, re.DOTALL) # Matches all instances of pattern
    iterables_object = re.finditer(r">([^<>].*?)<", content, re.DOTALL)
    iterables = []
    for it in iterables_object:
        iterables.append([it.start(), it.end()])
    # print(matches)
    # print(iterables)
    handler(matches, iterables, content)
    #print(len(matches))
    #print(matches)
    

def main() -> None:
    html_file_name = input("Enter name of HTML file to be Obfuscated: ")
    
    with open(html_file_name, 'r', encoding='utf-8', errors='ignore') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'html.parser')
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)