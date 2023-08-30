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
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.probability import FreqDist
from nltk.corpus import words 
import random 


# --------- Helpful Lists & Dictionaries

# pre-made list of user-input ending statements
ending_statements = ['bye','goodbye','good bye','thank you', 'see you next time', 'go away eliza', 'bye eliza','good bye eliza',' goodbye eliza']

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


#TODO: This is where the actual logic flow will go
# Pre-processing & Response Generation
def preprocess(userinput):

    confused = True # using True for now to test

    if confused:
        response = eliza_confused(confused)



    return response


# --------- Main Eliza Command

# Run Eliza
def Eliza():

    while True:
        # start off by asking introducting Eliza and asking for your name.
        print("Eliza: Hello - I'm Eliza! Can you tell me your name?")
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