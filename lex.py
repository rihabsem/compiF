from googletrans import Translator
import ply.lex as lex
import ply.yacc as yacc
import json
import os 
import re
import tkinter as tk
import difflib
import pygame
import time
from lyrics import song_lyrics
from PIL import Image, ImageTk


#-----------------------------constants-----------------------------
#Rihab
path = r'C:\Users\DELL\Desktop\S7\compilation\songCompiler\errorLog.json'
#Mohcine
#path = r'C:\Users\HP\Documents\compilation\projetCompilation\errorLog.json'
#dictionary
dataDic = {
    "lexical_error": [],
    "syntactic_error": [],
    "semantic_error": []
}
dataTemplate = {
        "Type": "",
        "Description": "",
        "Position": "",
        "Line":""
   
}
done = True

def play_song():
    pygame.mixer.init()
    pygame.mixer.music.load("oneLove.wav")
    pygame.mixer.music.play(loops=0, start=0.0)

#error log
#creating a json file :

def writeJson(data, filename=path):
    # Check if the file exists in our file system using the library "os"
    if os.path.exists(filename): 
        # Read existing data
        with open(filename, 'r') as f:
            try:
                existing_data = json.load(f) #storing the existing data in the json file in a list called existing_data
            except json.JSONDecodeError:
                existing_data = {"lexical_error": [], "syntactic_error": [], "semantic_error": []}
    else:
        existing_data = {"lexical_error": [], "syntactic_error": [], "semantic_error": []}
    
    # Merge new data with existing data
    for key in data:
        existing_data[key].extend(data[key]) #appending the new error in the existing_data list
    
    # Write the merged data back to the file
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4) #updating the json file

#function for storing the errors in the dictionaries defined before
def errorLog(error_type, description, line=None, position=None):
    errorEntry = dataTemplate.copy()
    errorEntry["Type"] = error_type
    errorEntry["Description"] = description
    errorEntry["Line"] = line
    errorEntry["Position"] = position

    if error_type == "lexical":
        dataDic["lexical_error"].append(errorEntry)
    elif error_type == "syntactic":
        dataDic["syntactic_error"].append(errorEntry)
    elif error_type == "semantic":
        dataDic["semantic_error"].append(errorEntry)


# Define the tokens and grammar rules
tokens = (
    "NOUNS",
    "VERBS",
    "ADVERBS",
    "ADJECTIVES",
    "ARTICLES",
    "PREPOSITIONS",
    "PRONOUNS",
    "DETERMINANT",
    "CONJUNCTIONS",
    "INTERJECTIONS",
    "PUNCTUATION",
    "LPAREN",
    "RPAREN"
)

# Define the token patterns
t_ignore = " \t"
t_NOUNS = r"\b(?:soul|love|heart|thanks|lord|place|sinner|mankind|beliefs|song|chance|doom|father|creation|thing|remarks|question|man|pity|chances|plea|battle|kingdoms|house)\b"
t_VERBS = r"\b(?:beginning|get|feel|hear|crying|saying|give|ask|is|has|hurt|save|comes|singing|pass|was|be|fight|have|grows|ain't|hiding|pleading|will|let's|let|praise|i'd|'m|am|like|join|tell|pray|would|trust)\b"
t_ADVERBS = r"\b(?:together|really|one|more|alright|just|all|there)\b"
t_ADJECTIVES = r"\b(?:my|mercy|own|holy|thinner|dirty|hopeless)\b"
t_ARTICLES = r"\b(?:a|the)\b"
t_PREPOSITIONS = r"\b(?:to|from|in|about|for|of|at|on|among)\b"
t_PRONOUNS = r"\b(?:you|us|i|them|who|it|shall|those|this|what|whose)\b"
t_DETERMINANT = r"\b(?:his|their|no|yes)\b"
t_CONJUNCTIONS = r"\b(?:and|or|so|when|as)\b"
t_INTERJECTIONS = r"\b(?:oh|woah)\b"
t_PUNCTUATION = r"[!?.,;:\"—-]"
t_LPAREN = r"\("
t_RPAREN = r"\)"

# Error handling for illegal characters
def t_error(t):
    error_message = f"Illegal character '{t.value[0]}' at line {t.lineno}"+"\n"
    print(error_message)
    widgets['labelRLEX'].config(text=widgets['labelRLEX'].cget("text") + error_message)
    lines = widgets['labelRLEX'].cget("text").split("\n")
    widgets['labelRLEX'].config(height=len(lines))
    errorLog("lexical", error_message, t.lineno, t.lexpos)
    writeJson(dataDic)
    t.lexer.skip(1)
    done = False




# Newline handling to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    
# Grammar rule for "S" (sentence)
def p_S(p):
    '''
    S : ADVP PUNCTUATION ADVP PUNCTUATION
      | VP CP PUNCTUATION
      | ADVP LPAREN INTERJECTIONS NP RPAREN PUNCTUATION
      | ADVP LPAREN VP RPAREN PUNCTUATION
      | ADVP PUNCTUATION
      | VP LPAREN PP RPAREN PUNCTUATION
      | CP LPAREN CP RPAREN PUNCTUATION
      | VP VP ADJP LPAREN ADVP RPAREN PUNCTUATION
      | ADVP VP PP LPAREN ADVP RPAREN PUNCTUATION
      | VP NP PP PUNCTUATION
      | VP ADVP ADJP PUNCTUATION 
      | VP LPAREN VP PP RPAREN PUNCTUATION
      | VP PP ADJP PUNCTUATION
      | CP VP NP PUNCTUATION
      | VP VP PUNCTUATION
      | ADVP PP PUNCTUATION 
      | ADVP LPAREN INTERJECTIONS RPAREN PUNCTUATION
      | VP LPAREN VP RPAREN PUNCTUATION
      | ADVP LPAREN INTERJECTIONS NOUNS RPAREN PUNCTUATION
      | VP VP VP ADJP LPAREN ADVP RPAREN PUNCTUATION
      | VP CP LPAREN CONJUNCTIONS VP RPAREN PUNCTUATION
      | VP LPAREN VERBS VERBS PP RPAREN PUNCTUATION
      | VP LPAREN PP RPAREN 
    '''
    print(f"Rule matched: S → {p[1:]}")
    if p[1] ==("one", "love") and p[2] == "," and p[3] == ("one", "heart"):
        pass
    elif p[1] == ("one", "heart"):
        pass
    elif p[1] == ("let's","join","together") and p[2] == ("and",("feel","alright")):
        pass
    elif p[1] == ("one","love") and p[2] == "(" and p[3] == "oh" and p[4] == ("lord","of","mercy") and p[5] == ")":
        pass
    elif p[1] == ("one","heart") and p[2] == "(" and p[3] == ("i","tell","you") and p[4] == ")":
        pass
    elif p[1] == ("let's","join","together") and p[2] == "(" and p[3] == ("at",("this","house"),("i","pray")) and p[4] == ")":
        pass
    elif p[1] == ("and",("feel","alright")) and p[2] == "(" and p[3] == ("and",("i","will","feel","alright")) and p[4] == ")":
        pass
    elif p[1] == ("let","them","all") and p[2] == ("pass","all") and p[3] == ("their","dirty","remarks") and p[4] == "(" and p[5] == ("one","love") and p[6] == ")":
        pass
    elif p[1] == ("there","is","one","question") and p[2] == ("i'd","really","like") and p[3] == ("to","ask") and p[4] == "(" and p[5] == ("one","soul") and p[6] == ")":
        pass
    elif p[1] == ("is","there") and p[2] == ("a","place") and p[3] == ("for",("the","hopeless","sinner")) :
        pass
    elif p[1] == ("who","has","hurt","all","mankind") and p[2] == ("just",("to","save")) and p[3] == ("his","own") :
        pass
    elif p[1] == ("one","love") and p[2] == "(" and p[3] == ("hear","my","plea") and p[4] == ")":
        pass
    elif p[1] == ("let's","join","together") and p[2] == "(" and p[3] == ("let's","just","trust") and p[4] == ("in",("the","lord")) and p[5] == ")":
        pass
    elif p[1] == ("let's","join","together") and p[2] == ("to","fight") and p[3] == ("this","holy","battle"):
        pass
    elif p[1] == ("so","when") and p[2] == ("the","man","comes","there","will","be","no") and p[3] == ("no","doom"):
        pass
    elif p[1] == ('have','pity',('on','those','whose','chances')) and p[2] == ('grows','thinner'):
        pass
    elif p[1] == ('there',"ain't",'no',"hiding","place") and p[2] == ("among","the","kingdoms","of","love","yes"):
        pass
    elif p[1] == ("one","heart") and p[2] == "(" and p[3] == "oh" and p[4] == ")":
        pass
    elif p[1] == ("let's","join","together") and p[2] == "(" and p[3] == ("let","this","house","a","pray") and p[4] == ")":
        pass
    elif p[1] ==("one", "love") and p[2] == "(" and p[3] == "oh" and p[4] == "lord" and p[5] == ")":
        pass
    elif p[1] == ("one","heart") and p[2] == "(" and p[3] == "oh" and p[4] == "lord" and p[5] == ")":
        pass
    elif p[1] == ("let's", 'join', 'together') and p[2] == '(' and p[3] == ("let's", 'all', 'pray') and p[4] == ('to', ('the', 'lord')) and p[5] == ')':
        pass
    elif p[1] == ('i', 'tell', 'you') and p[2] == ('let', 'them', 'all') and p[3] == ('pass', 'all') and p[4] == ('their', 'dirty', 'remarks') and p[5] == '(' and p[6] == ('one', 'love') and p[7] == ")":
        pass
    elif p[1] == ("let's", 'join', 'together') and p[2] == "(" and p[3] == ('at', ('this', 'house'), 'a', 'pray') and p[4] == ")":
        pass
    elif p[1] == ('one', 'heart') and p[2] == "(" and p[3] == ('hear', 'my', 'plea') and p[4] == ")":
        pass
    elif p[1] == ("let's","join","together") and p[2] == "(" and p[3] == "let's" and p[4] == "pray" and p[5] == ('to', ('the', 'lord')) and p[6] == ")":
        pass
    else:
        error_message = f"Semantic error S: check out the structure of your phrase."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)

def p_ADVP(p):
    '''
    ADVP : ADVERBS NOUNS
         | ADVERBS VERBS
         | ADVERBS VERBS ADJP
         | ADVERBS VERBS ADVERBS
         | ADVERBS VERBS ADVERBS NOUNS
         | ADVERBS PP
         | ADVERBS VERBS DETERMINANT VERBS NOUNS  
    '''
    print(f"Rule matched: ADVP → {p[1:]}")
    if p[1] == "one" and p[2] == "love" or p[1] == "one" and p[2] == "heart" or p[1] == "one" and p[2] == "soul":
        p[0] = (p[1],p[2])
    elif p[1] == "there" and p[2] == "is" and p[3] == "one" and p[4] == "question":
        p[0] = (p[1],p[2],p[3],p[4])
    elif p[1] == "just" and p[2] == ("to","save"):
        p[0] = (p[1],p[2])
    elif p[1] == 'there' and p[2] == "ain't" and p[3] == 'no' and p[4] == "hiding" and p[5] == "place":
        p[0] = (p[1],p[2],p[3],p[4],p[5])
    else :
        error_message = f"Semantic error ADVP: please check the structure of your phrase."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)

def p_VP(p):
    '''
    VP : VERBS VERBS ADVERBS
       | VERBS ADVERBS 
       | PRONOUNS VERBS PRONOUNS
       | PRONOUNS VERBS
       | PRONOUNS VERBS VERBS ADVERBS
       | VERBS PRONOUNS ADVERBS
       | VERBS ADVERBS VERBS 
       | PRONOUNS VERBS VERBS ADVERBS NOUNS
       | VERBS ADJECTIVES NOUNS
       | ARTICLES NOUNS VERBS ADVERBS VERBS  VERBS DETERMINANT  
       | VERBS NOUNS PP
       | VERBS ADJECTIVES
       | VERBS PRONOUNS NOUNS ARTICLES VERBS 
        
    '''
    
    print(f"Rule matched: VP → {p[1:]}")
    if p[1] == "let's" and p[2] == "join" and p[3] == "together":
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "feel" and p[2] == "alright" :
        p[0] = (p[1],p[2])
    elif p[1] == "i" and p[2] == "tell" and p[3] == "you":
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "i" and p[2] == "pray":
        p[0] = ("i","pray")
    elif p[1] == "i" and p[2] == "will" and p[3] == "feel" and p[4] == "alright":
        p[0] = (p[1],p[2],p[3],p[4])
    elif p[1] == "let" and p[2] == "them" and p[3] == "all" :
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "pass" and p[2] == "all" :
        p[0] = (p[1],p[2])
    elif p[1] == "i'd" and p[2] == "really" and p[3] == "like" :
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "is" and p[2] == "there":
        p[0] = (p[1],p[2])
    elif p[1] == 'who'and p[2] == 'has' and p[3] == 'hurt' and p[4] == 'all' and p[5] == 'mankind':
        p[0] = (p[1],p[2],p[3],p[4],p[5])
    elif p[1] == "hear" and p[2] == "my" and p[3] == "plea" :
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "let's" and p[2] == "just" and p[3] == "trust" :
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "the" and p[2] == "man" and p[3] == "comes" and p[4] == "there" and p[5] == "will" and p[6] == "be" and p[7] == "no" :
        p[0] = (p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    elif p[1] == "have" and p[2] == "pity" and p[3] == ("on","those","whose","chances"):
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "grows" and p[2] == "thinner":
        p[0] = (p[1],p[2])
    elif p[1] == 'let'and p[2] == 'this' and p[3] == 'house' and p[4] == 'a' and p[5] == "pray":
        p[0] = (p[1],p[2],p[3],p[4],p[5])
    elif p[1] == "let's" and p[2] == "all" and p[3] == "pray":
        p[0] = (p[1],p[2],p[3])
    else:
        error_message = f"Semantic error VP: check out the structure of your phrase please."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)

def p_NP(p):
    '''
    NP : NOUNS PREPOSITIONS ADJECTIVES
       | PRONOUNS NOUNS
       | ARTICLES NOUNS
       | DETERMINANT NOUNS 
       
    '''
    print(f"Rule matched: NP → {p[1:]}")
    if p[1] == "lord" and p[2] == "of" and p[3] == "mercy":
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "this" and p[2] == "house":
        p [0] = ("this","house")
    elif p[1] == "a" and p[2] == "place" :
        p[0] = (p[1],p[2])
    elif p[1] == "the" and p[2] == "lord":
        p [0] = ("the","lord")
    elif p[1] == "no" and p[2] == "doom":
        p [0] = ("no","doom")
    else:
        error_message = f"Semantic error NP: check out the structure of your phrase please."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)


def p_PP(p):
    '''
    PP : PREPOSITIONS NP VP 
       | PREPOSITIONS VERBS 
       | PREPOSITIONS ADJP
       | PREPOSITIONS NP
       | PREPOSITIONS NOUNS
       | PREPOSITIONS PRONOUNS PRONOUNS NOUNS
       | PREPOSITIONS ARTICLES NOUNS PREPOSITIONS NOUNS DETERMINANT
       | PREPOSITIONS ARTICLES NOUNS
       | PREPOSITIONS NP ARTICLES VERBS
    '''
    #i added the last one 
    print(f"Rule matched: PP → {p[1:]}")
    if p[1] == 'at' and p[2] == ("this","house") and p[3] == ("i","pray"):
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "to" and p[2] == "ask" or  p[1] == "for" and p[2] == ("the","hopeless","sinner") or p[1] == "to" and p[2] == "save" or p[1] == "in" and p[2] == ("the","lord") or p[1] == "to" and p[2] == "fight":
        p[0] = (p[1],p[2])
    elif p[1]=='on' and p[2] == 'those' and p[3] == 'whose' and p[4] == 'chances':
        p[0] = (p[1],p[2],p[3],p[4])
    elif p[1] == "among" and p[2] == "the" and p[3] == "kingdoms" and p[4] == "of" and p[5] == "love" and p[6] == "yes":
        p[0] = (p[1],p[2],p[3],p[4],p[5],p[6])
    elif p[1] == "to" and p[2] == ("the","lord"):
        p[0] = (p[1],p[2])
    elif p[1] == 'at' and p[2] == ("this","house") and p[3] == "a" and p[4] == "pray":
        p[0] = (p[1],p[2],p[3],p[4])
    else:
        error_message = f"Semantic error PP: check out the structure of your phrase please."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)
def p_CP(p):
    '''
    CP : CONJUNCTIONS VP 
       | CONJUNCTIONS CONJUNCTIONS
       
    '''
    print(f"Rule matched: CP → {p[1:]}")
    if p[1] == "and" and p[2] == ("feel","alright"):
        p[0] = (p[1],p[2])
    elif p[1] == "and" and p[2] == ("i","will","feel","alright"):
        p[0] = (p[1],p[2])
    elif p[1] == "so" and p[2] == "when":
        p[0] = (p[1],p[2])
    else:
        error_message = f"Semantic error CP: did you mean and feel alright."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)

def p_ADJP(p):
    '''
    ADJP : DETERMINANT ADJECTIVES NOUNS 
         | ARTICLES ADJECTIVES NOUNS
         | DETERMINANT ADJECTIVES
         | PRONOUNS ADJECTIVES NOUNS
         | NOUNS ADJECTIVES 
    '''
    print(f"Rule matched: ADJP → {p[1:]}")
    if p[1] == "their" and p[2] == "dirty" and p[3] == "remarks":
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "the" and p[2] == "hopeless" and p[3] == "sinner":
        p[0] = (p[1],p[2],p[3])
    elif p[1] == "his" and p[2] == "own":
        p[0] = (p[1],p[2])
    elif p[1] == "this" and p[2] == "holy" and p[3] == "battle" :
        p[0] = (p[1],p[2],p[3])
    else:
        error_message = f"Semantic error ADJP: check out the structure of your phrase please."+"\n"
        widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + error_message)
        lines = widgets['labelRSEM'].cget("text").split("\n")
        widgets['labelRSEM'].config(height=len(lines))
        errorLog("semantic", error_message)
        writeJson(dataDic)



# Error handling for parsing
def p_error(p):
    if p:
        error_message = f"Syntax error at token '{p.type}' with value '{p.value}'"
        errorLog("syntactic", error_message, p.lineno, p.lexpos)
        writeJson(dataDic)
        raise Exception(error_message)
    else:
        error_message = "Syntax error at EOF (end of file)"
        errorLog("syntactic", error_message)
        writeJson(dataDic)
        raise Exception(error_message)

# translation function
def translate_texts(text, target_languages=['it', 'fr', 'es']):
    translator = Translator()
    translations = {}
    for lang in target_languages:
        try:
            translation = translator.translate(text, dest=lang)
            translations[lang] = translation.text
        except Exception as e:
            print(f"Translation error for {lang}: {e}")
            translations[lang] = None
    return translations

# data processing function
def process_data(data):
    processed_lines = []
    pattern = r"\.$|!$|\?$"  # Matches sentences ending with '.', '!', or '?'
    Pdatas = data.splitlines()  
    for Pdata in Pdatas:
        match = re.search(pattern, Pdata)
        if match is None:
            Pdata = Pdata + "."
        processed_lines.append(Pdata)
    return "\n".join(processed_lines)

# Lexical analysis function
def lexicalAnalysis():
    
        print("-----------------------------Lexical analysis-----------------------------")
        lexer = lex.lex()  # Create the lexer

        # Récupération du texte depuis le widget Text
        try:
            text = widgets["textbox"].get("1.0", "end-1c")
        except tk.TclError as e:
            print(f"Error accessing Text widget: {e}")
            widgets['labelRLEX'].config(text="\nError: Unable to access the text widget.")
            return

        # Traitement des données pour l'analyse
        data = process_data(text)
        lexer.input(data.lower())
        tokens_list = []

        
            # Collect tokens and handle lexical errors
        for tok in lexer:
            tokens_list.append(tok)
            print(tok)
        if tokens_list:
            msg = "Lexical analysis completed successfully!"
            widgets['labelRLEX'].config(text=widgets['labelRLEX'].cget("text") + msg)
            lines = widgets['labelRLEX'].cget("text").split("\n")
            widgets['labelRLEX'].config(height=len(lines))
            print("")
            synthaxique_analyse(tokens_list)
        else:
            return None
        
        

def process_lines(tokens_list):
    """Processes tokens and returns a list of raw input strings for syntactic analysis."""
    current_line = []
    raw_inputs = []  # Liste pour stocker toutes les phrases traitées
    
    for tok in tokens_list:
        current_line.append(tok.value)
        
        # Vérifier si le token est une ponctuation de fin de phrase
        if tok.type == 'PUNCTUATION' and tok.value in ['.', '!', '?']:
            # Construire une phrase complète à partir des tokens collectés
            raw_input = " ".join(current_line)
            print(f"\nProcessing line: {raw_input}")  # Afficher la phrase pour debug
            raw_inputs.append(raw_input)  # Ajouter la phrase à la liste
            current_line = []  # Réinitialiser la ligne pour la prochaine phrase
    
    # Si la liste des phrases est vide, retourner None
    if not raw_inputs:
        return None
    
    return raw_inputs  # Retourner toutes les phrases traitées

def suggest_lyric(user_input):
    # Use difflib to find the closest match
    closest_match = difflib.get_close_matches(user_input, song_lyrics, n=1, cutoff=0.6)
    if closest_match:
        message = "Closest match found:"+closest_match[0]
        return message  # Return the closest matching lyric
    else:
        message = "No match found"
        return message

def synthaxique_analyse(tokens_list):
    """Performs syntactic analysis on the tokens."""
    # Get the processed lines from process_lines
    raw_inputs = process_lines(tokens_list)
    
    if raw_inputs is None:
        print("No valid sentence found.")
        return
    for tok in tokens_list:
        if not isinstance(tok.value, (str, int, float)):  # Add valid types as needed
            print(f"Invalid token value: {tok.value}")
            return
    parser = yacc.yacc(debug=True, write_tables=False, optimize=False)  # Create the parser
    all_translations = []  # List to accumulate all translations
    
    # Iterate through each sentence in raw_inputs
    for raw_input in raw_inputs:
        try:
            # Parse the sentence
            parser.parse(raw_input)
            
            # Success message after syntactic analysis
            success_message1 = f"Syntaxic analysis successfully performed for: {raw_input}\n"
            widgets['labelRSYN'].config(text=widgets['labelRSYN'].cget("text") + success_message1)
            lines = widgets['labelRSYN'].cget("text").split("\n")
            widgets['labelRSYN'].config(height=len(lines))
            
            # Success message for semantic analysis
            success_message2 = f"Sementic analysis performed for: {raw_input}\n"
            widgets['labelRSEM'].config(text=widgets['labelRSEM'].cget("text") + success_message2)
            lines = widgets['labelRSEM'].cget("text").split("\n")
            widgets['labelRSEM'].config(height=len(lines))
            
            # Translate the success messages
            translations = translate_texts(raw_input)
            if translations:
                translation_msg = "\n".join([f"{lang.upper()}: {text}" for lang, text in translations.items() if text])
                all_translations.append(translation_msg)  # Accumulate translations for all sentences
        except Exception as e:
            # Display the error message if there is a syntax issue
            error_message = f"{e} at the sentence {raw_input}"
            error_message = error_message + " " + suggest_lyric(raw_input)
            widgets['labelRSYN'].config(text=widgets['labelRSYN'].cget("text") + error_message+"\n")
            lines = widgets['labelRSYN'].cget("text").split("\n")
            widgets['labelRSYN'].config(height=len(lines))
    
    # Once all sentences are processed, update the translation label
    if all_translations:
        widgets['translation_label'].config(text="\n".join(all_translations))
        lines = widgets['translation_label'].cget("text").split("\n")
        widgets['translation_label'].config(height=len(lines))


    


# Define the window close handler
def on_close():
    print("Window is closing... cleaning up!")
    widgets["window"].destroy()

def clear_fields():
    """Function to clear all fields."""
    widgets["textbox"].delete("1.0", tk.END)  # Clear the input text box
    widgets['labelRLEX'].config(text="")  # Clear lexical analysis result
    widgets['labelRSYN'].config(text="")  # Clear syntactic analysis result
    widgets['labelRSEM'].config(text="")  # Clear semantic analysis result
    widgets['translation_label'].config(text="")  # Clear translation results
    widgets['labelRSYN'].config(height=1)
    widgets['labelRSEM'].config(height=1)


def analysis_window():
    global widgets, window
    widgets = {}
    window = tk.Tk()
    window.geometry("900x750")
    window.title("One Love - Bob Marley")

    # Initial view: Image, song, and start button
    def show_start_view():
        # Load and display the background image
        image_path = "exodus.jpg"  # Replace with your image file path
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((900, 750))
        bg_photo = ImageTk.PhotoImage(bg_image, master=window)  # Ensure master is specified

        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection

        # Play the song
        play_song()

        # Add the "Start" button
        start_button = tk.Button(window, text="Start", font=('Ariel', 12), command=show_analysis_view)
        start_button.place(x=430, y=700)

    # Analysis view: Textbox, analysis button, results, and translation
    def show_analysis_view():
        # Clear all widgets
        for widget in window.winfo_children():
            widget.destroy()
        image_path = "background.jpg"  # Replace with your image file path
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((900, 750))
        bg_photo = ImageTk.PhotoImage(bg_image, master=window)  # Ensure master is specified

        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_photo

        # Add the analysis widgets
        label = tk.Label(window, text="Enter the desired lyric:", font={'Ariel', 10})
        widgets["textbox"] = tk.Text(window, height=3, width=50, font=("Arial", 10))
        analyze_button = tk.Button(window, text="Analyze", font=('Ariel', 10), command=lexicalAnalysis)
        clear_button = tk.Button(window, text="Clear", font=('Ariel', 10), command=clear_fields)

        # Labels for results
        widgets['labelLEX'] = tk.Label(window, text="Lexical Analysis Result:", font=('Ariel', 13))
        widgets['labelRLEX'] = tk.Label(window)
        widgets['labelSYN'] = tk.Label(window, text="Syntactic Analysis Result:", font=('Ariel', 13))
        widgets['labelRSYN'] = tk.Label(window)
        widgets['labelSEM'] = tk.Label(window, text="Semantic Analysis Result:", font=('Ariel', 13))
        widgets['labelRSEM'] = tk.Label(window)

        # Translation section
        label_translation = tk.Label(window, text="Translation:", font=('Ariel', 13))
        widgets['translation_label'] = tk.Label(window, text="", justify=tk.LEFT)

        # Layout
        label.place(x=50, y=120)
        widgets["textbox"].place(x=50, y=150)
        analyze_button.place(x=50, y=220)
        clear_button.place(x=150, y=220)
        widgets['labelLEX'].place(x=50, y=260)
        widgets['labelRLEX'].place(x=50, y=280)
        widgets['labelSYN'].place(x=50, y=380)
        widgets['labelRSYN'].place(x=50, y=400)
        widgets['labelSEM'].place(x=50, y=500)
        widgets['labelRSEM'].place(x=50, y=520)
        label_translation.place(x=650, y=255)
        widgets['translation_label'].place(x=650, y=275)

    # Function to clear all fields
    def clear_fields():
        widgets["textbox"].delete("1.0", tk.END)  # Clear the input text box
        widgets['labelRLEX'].config(text="")  # Clear lexical analysis result
        widgets['labelRSYN'].config(text="")  # Clear syntactic analysis result
        widgets['labelRSEM'].config(text="")  # Clear semantic analysis result
        widgets['translation_label'].config(text="")  # Clear translation results

    # Start with the initial view
    show_start_view()
    window.mainloop()


analysis_window()
    






