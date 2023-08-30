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
    'some input phrase' : 'the response'
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
        print(f"word is {word}")
        if word[1] !='NNP' and word[0]==str(namesearch.group()).strip():
            name_text.append((word[0],'NNP'))
        else:
            name_text.append(word)

    

    name = [word[0] for word in name_text if word[1] in ['NNS','NNP','NN'] and re.match(r'[A-Z][a-z]*',word[0])]
    
    print(f"name is {name}")


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

    

    return response

#TODO: This is where the actual logic flow will go
# Pre-processing & Response Generation
def preprocess(userinput):

    confused = False # using True for now to test

    response = "Tell me about something else?"
    
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
    
    cleaned_words = [word for word in pos_user_words if word[0].lower() not in stop_words]
    

    # Perform Word Spotting
    name, adjective, verb,adverb, noun = '','','','',''

    if re.search(r'.[A-Z][a-z]*',userinput):
        print('name found')        
        # This will handle the case where end users enter a name 
        # TODO: Bug - "My name is Probably Devin" returns name as "Probably"
        name, non_name_text = get_names(cleaned_words, userinput)
        
        # This will handle verbs
        verb = [word[0] for word in non_name_text if word[1] in ['VBG','VBZ','VBD','VBN','VBP','VB']]

        # This will handle adverbs
        adverb = [word[0] for word in non_name_text if word[1] in['RBR','RBS','RB','RP']]

        # This will handle adjectives
        adjective = [word[0] for word in non_name_text if word[1] in ['JJ','JJR','JJS']]

    else:
        print('name not found')
        # This will handle nouns
        noun = [word[0] for word in cleaned_words if word[1] in ['NNS','NN']]

        # This will handle verbs
        verb = [word[0] for word in cleaned_words if word[1] in ['VBG','VBZ','VBD','VBN','VBP','VB']]

        # This will handle adverbs
        adverb = [word[0] for word in cleaned_words if word[1] in['RBR','RBS','RB','RP']]

        # This will handle adjectives
        adjective = [word[0] for word in cleaned_words if word[1] in ['JJ','JJR','JJS']]

    
    if name:
        
        response=[f"Hello {name[0]}! It's great to see you. How are you?"]
    
    if adjective:
        response = get_response(userinput,adjective[0])

    else:
        response = eliza_confused(confused=True)



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