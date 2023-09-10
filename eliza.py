# Assignment: Eliza Chatbot
# Course: AIT 526
# Names: Devin Schechter, Stuti Tandon, Jeffrey Stejskal, Syeda Abhia Abbas
# Date: 8/29/2023

# Purpose Statement:

# Usage Example:

# Usage Instructions:


# ------------------- CODE STARTS HERE ----------------------------- #


# --------- Import Libraries
import re
import nltk
#nltk.download('words')
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk import pos_tag, ne_chunk
from nltk.probability import FreqDist
from nltk.corpus import words 
from nltk.tree import Tree
import random 


# --------- Helpful Lists & Dictionaries

# List of Stop Words
stop_words = stopwords.words('english')

# pre-made list of user-input ending statements
ending_statements = ['end','bye','goodbye','good bye','thank you', 'see you next time', 'go away eliza', 'bye eliza','good bye eliza',' goodbye eliza']

# Pre-made responses for when Eliza is confused
confused_responses = ["Why don't you elaborate on that to help me understand?",
                           "Let's pull the thread on that - can you please elaborate?",
                           "I didn't catch that. Try explaining this to me like I'm 5.",
                           "What do you mean by that?",
                           "I don't quite follow, could you please explain?",
                           "Could you break that down for me?",
                           "I'm sorry, could you please rephrase that?",
                           "I'd like to understand, could you please elaborate?",
                           "That was a lot of information, could you please run that by me again?"]

#TODO: List of responses needed in order for the code to function
# Pre-made dictionary of responses
responses = {
    # These are responses are general responses to introductions/greetings
    r'.* ?(hi|Hi|hello|Hello) ?(?P<keywords>.*)?': ["Hey there, how are you?",
                                                    "Hi. It is a pleasure to meet you. What would you like to talk about today?"],

    # Answer Yes/No Questions
    r'Yes|yes':
    ["Tell me more about it.","How often do you find yourself feeling this way?","Why are you sure about this?"],

    r'.* ?(No|no)':
    ["Why don't you believe it?", "What makes you say no?"],
    r'.*? (I am not| I do not) (?P<keywords>.+)':['Why do you not think so?','Why do you not text?'],

    r'.*Because|because (?P<keywords>.+)':
    ["What makes you state that reason?","What other reasons influence you?","I don't think that is the only reason, can you tell me more about it?"],
    
    #Generic responses
    r'(why|when|how|what) .*': 
    ["Why did you ask me that?",
     "Does this topic bother you?",
     "Would you like to talk about this more?"],
    
    # These responses are for when the user is talking about how they feel
    r'I am|feel|I think (?P<keywords>.+)':
    ["Is feeling text why you wanted to talk today?",
     "How long have you been feeling text?",
     "How does feeling text make you feel?"],

    # These responses are for when the user is not sure about something
    r'.* ?(Inconsistent|Confuse|Unclear|Undecide|Perhaps|Maybe|I am not sure|I do not know).*':
      ["Do you have any ideas for how you will address this uncertainity?",
       "Why do you think you are so unsure about this?"],

    # These responses are for responding to when the user is talking about something they want
    r'I want (?P<keywords>.+)':
      ["Why do you want text",
        "What makes you think you need text?",
       "What will you do if you get text?",
       "How would you feel if you get text?",
       "Why do you want text?"],

    # These responses are meant for regurgitating inputs into questions
    r'.* ?am I (?P<keywords>.+)': 
    ["Do you think that you are text?",
     "Why do you feel text",
     "Are you hoping that I can help you understand why you are feeling text"],

    r'.* ?would like (?P<keywords>.+)':
    ["Why would you like text ?", "Why is text important to you?"],

     # Asking for elaboration
     r'Were you (?P<keywords>.*)':
       [ "Do you think that I was text ?",
        "If I had been text how would that make you feel?"],

     r'I was |I have (?P<keywords>.*)':
       ["What made you text ?",
        "Are you willing to tell me more about your text now?"],

    
}

# --------- Define Functions

# Eliza Doesn't Understand
# If Eliza doesn't understand, prompt the user for clarification using one of the pre-coded possible responses.
def eliza_confused(confused):
    if confused:
        #If Eliza is confused - randomly select one of the premade confused responses
        #print(len(confused_responses))
        action = confused_responses[random.randint(0,len(confused_responses)-1)]
        return action



# Explode Contractions
# This function searches for contractions and "explodes" them into their root words
def explode_contractions(input_phrase):

    # Specific Rules (handles words that don't cleanly follow the generalized rules below)
    input_phrase = re.sub(r"can\'t","can not", input_phrase)
    input_phrase = re.sub(r"won\'t","will not", input_phrase)
    
    # Generalized Rules
    input_phrase = re.sub(r"\'m"," am", input_phrase) #ex: I'm -> I am
    input_phrase = re.sub(r"\'ve"," have", input_phrase) #ex: I've -> I have
    input_phrase = re.sub(r"\'ll"," will", input_phrase) #ex: I'll -> I will
    input_phrase = re.sub(r"\'d"," would", input_phrase) #ex: I'd -> I would
    input_phrase = re.sub(r"\'re"," are", input_phrase) #ex: you're -> you are
    input_phrase = re.sub(r"\'s"," is", input_phrase) #ex: she's -> She is
    input_phrase = re.sub(r"n\'t"," not", input_phrase) #ex: wouldn't -> would not
    input_phrase = re.sub(r"\'ll"," will", input_phrase) #ex: I'll -> I will

    return input_phrase



# Retreive Names
def get_names(no_stop_words_text, userinput):
    name_text = []
    
    namesearch = re.search(r'.[A-Z][a-z]*',userinput)

    
    for word in no_stop_words_text:
        
        if word[1] !='NNP' and word[0]==str(namesearch.group()).strip():
            name_text.append((word[0],'NNP'))
        else:
            name_text.append(word)

    

    name = [word[0] for word in name_text if word[1] in ['NNS','NNP','NN'] and re.match(r'[A-Z][a-z]*',word[0]) and word[0].lower() not in ('hi','hello','hey')]

    return name, name_text

# remove nonsense words
def remove_nonsense(userinput):
    nonsense = []
    nonsense = [word for word in userinput]

    sensical_words = []
    for item in nonsense:
        if item[0].lower() in words.words():
            sensical_words.append(item)
    
    return sensical_words

# Generate a Response
def get_response(userinput,postype):

    response = ''
    for key,value in responses.items():
        answer = re.search(r'{}'.format(key),userinput)

    ##Select a response for that key
        if answer is not None:
            response = re.sub('text?', postype,random.choice(value))

    # Check that a response was given
    if response == '':
        response = eliza_confused(True)
            
    return response

#TODO: This is where the actual logic flow will go
# Pre-processing & Response Generation
def preprocess(userinput):

    response = ''

    confused = False # using True for now to test

    #response = "Tell me about something else?"
    
    this_chunk, nounphrases = [], []

    # Explode any contractions
    userinput_exploded = explode_contractions(userinput)

    # Tokenize Words
    user_words = word_tokenize(userinput_exploded)

    # Tag part of speech
    pos_user_words = pos_tag(user_words)
    

    # find noun phrases
    ne_tree = ne_chunk(pos_user_words)
    grammar = 'NP: {<DT>?<JJ>*<NN>}'
    chunkparser = nltk.RegexpParser(grammar)

    user_noun_phrase = chunkparser.parse(pos_user_words)

    # Retreive noun phrases
    for chunk in user_noun_phrase:
        if type(chunk) == Tree:
            this_chunk = f' {[token for token, partofspeech in chunk.leaves()]}'
            nounphrases.append(this_chunk)

    # remove stop words
    print(pos_user_words)
    
    cleaned_words = [word for word in pos_user_words if (word[0].lower() not in stop_words) or ( word[0].lower() in ('no'))]
    print(cleaned_words)
    

    # Perform Word Spotting
    name, adjective, verb, adverb, noun = '','','','',''

    if re.search(r'.[A-Z][a-z]*',userinput):
              
        # This will handle the case where end users enter a name 
        # TODO: Bug - "My name is Probably Devin" returns name as "Probably"
        name, non_name_text = get_names(cleaned_words, userinput)
        
        # This will handle verbs
        verb = [word[0] for word in non_name_text if word[1] in ['VBG','VBZ','VBD','VBN','VBP','VB']]

        # This will handle adverbs
        adverb = [word[0] for word in non_name_text if word[1] in['RBR','RBS','RB','RP']]

        # This will handle adjectives
        adjective = [word[0] for word in non_name_text if word[1] in ['JJ','JJR','JJS']]

        #yes/no
        determiner = [word[0] for word in non_name_text if word[1] in ['DT']]

    else:
        
        # This will handle nouns
        noun = [word[0] for word in cleaned_words if word[1] in ['NNS','NN']]

        # This will handle verbs
        verb = [word[0] for word in cleaned_words if word[1] in ['VBG','VBZ','VBD','VBN','VBP','VB']]

        # This will handle adverbs
        adverb = [word[0] for word in cleaned_words if word[1] in['RBR','RBS','RB','RP']]

        # This will handle adjectives
        adjective = [word[0] for word in cleaned_words if word[1] in ['JJ','JJR','JJS']]

        #yes/no
        determiner = [word[0] for word in cleaned_words if word[1] in ['DT']]

    
    if name:
        
        response=f"Hello {name[0]}! It's great to see you. How are you?"
    
    if adjective:
        response = get_response(userinput, adjective[0])
    
    if noun:
        response = get_response(userinput, noun[0])

    if verb:
       response = get_response(userinput, verb[0])

    if adverb:
       response = get_response(userinput, adverb[0])

    if determiner:
       response = get_response(userinput, determiner[0])
    

    return response


# --------- Main Eliza Command

# Run Eliza
def Eliza():

    start = True

    while True:
        # start off by asking introducting Eliza and asking for your name.
        if start:
            print("Eliza: Hello - I'm Eliza! Can you tell me your name?")
            start = False

        userinput = input("You: ")

        # Check if the user is ending the conversation
        if userinput.lower() in ending_statements:
            print("Eliza: It was good talking with you. I look forward to our next appointment.")
            break
        else:
            response = preprocess(userinput)
            print(f"Eliza: {response}")
            
# -------------- Run Eliza
Eliza()