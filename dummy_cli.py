# import random, json and re module
import random
import json
import re

# words ruleset
with open('dummy-rules.json', 'r') as file:
    rules = json.load(file)
# phrases ruleset
with open('phrases.json', 'r') as file:
    phrases = json.load(file)
# emojis
with open('emoji.json', 'r', encoding='utf-8') as file:
    emojis = json.load(file)

# set randomization chances
parentheses_chance = 0.95
period_chance = 0.05
whitespace_chance = 0.01
w_chance = 0.01
missing_period_chance = 0.2
missing_space_chance = 0.2
wrong_letter_chance = 0.1
no_comma_chance = 0.8

# get user input
print("*-*-**-*-**-*-**-*-**-*-**-*-**-*-*")
user_input = input("\nWhat do you wanna dummify?\n\n")

# make input lowercase
def lowercase_input(text):
    return text.lower()

# separate paragraph into sentences (using positive look behind with re)
def separate_sentences(text):
    return re.split(r'(?<=\.) ', text)

# check input for phrases 
def detect_phrase(sentences):
    for i, sentence in enumerate(sentences):
        for key, phrase_list in phrases.items():
            for phrase in phrase_list:
                if phrase in sentence:
                    sentences[i] = sentence.replace(phrase, key)
    return sentences

# replace words with typos based on the ruleset
def replace_words(text, rules):
    words = text.split()
    output = []

    for word in words:
        # handle punctuation
        if word.endswith('.'):
            clean_word = word[:-1]
            punctuation = '.'
        else:
            clean_word = word
            punctuation = ''

        if clean_word in rules:
            replacements = rules[clean_word][:-1]
            probability = rules[clean_word][-1]

            if random.random() < probability:
                replacement = random.choice(replacements)
                output.append(replacement + punctuation)
            else:
                output.append(word)
        else:
            output.append(word)

    return ' '.join(output) 

# capitalize sentences
def capitalize_sentences(sentences):
    return [sentence.capitalize() for sentence in sentences]

# UNFINISHED add hashtags at the end of a sentence
def add_hashtags(sentences):
    pass

#create and return output
def finish_output(sentences):
    return ' '.join(sentences)

# main processing
user_input = lowercase_input(user_input)
sentences = separate_sentences(user_input)

# detect and replace phrases
sentences = detect_phrase(sentences)

# replace words based on the rules
sentences = [replace_words(sentence, rules) for sentence in sentences]

# apply capitalization
processed_sentences = capitalize_sentences(sentences)

# final output formatting
output = finish_output(processed_sentences)

# add random effects to the final output
output_words = output.split()
final_output = []

# remove a period from the final sentence
if random.random() < missing_period_chance and sentences:
    sentences[-1] = sentences[-1].rstrip('.') # rstrip removes any trailing characters

# remove a space between two words in the paragraph
if random.random() < missing_space_chance:
    for i in range(len(output_words) - 1): #loop through all the words except the last one
        if random.random() < 0.5: #randomly choose a position to remove the space
            output_words[i] += output_words[i + 1] # merge current word with previous
            del output_words[i + 1] # delete next word (it's now part of the previous)
            break # ensure only one whitespace removal happens

for word in output_words:
    # detect '(' and react to it
    if '(' in word and random.random() < parentheses_chance:
        word = word.replace('(', '( ')
    # detect '.' and react to it
    if '.' in word and random.random() < period_chance:
        word = word.replace('.', '..')
    # remove apostrophe
    if '\'' in word:
        word = word.replace("'", "")
    # remove commas
    if ',' in word and random.random() < no_comma_chance:
        word = word.replace(",", "")
    # add random whitespace
    if random.random() < whitespace_chance:
        final_output.append(word + ' ')
        continue
    # add random 'w'
    if random.random() < w_chance:
        final_output.append(word + ' w')
        continue
    # i to j typo
    if 'i' in word and random.random() < wrong_letter_chance:
        word = word.replace('i', 'j')  
    # otherwise just add the word
    final_output.append(word)

# combine final output
final_output = ' '.join(final_output)



# display the results
print("\n*-*-**-*-**-*-**-*-**-*-**-*-**-*-*")
print("\nHere's the dummified version:\n")
print(final_output)
print("\n*-*-**-*-**-*-**-*-**-*-**-*-**-*-*")
