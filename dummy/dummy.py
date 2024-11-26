import reflex as rx
import random
import json
import re
from reflex import State
from rxconfig import config
# words ruleset
with open('dummy-rules.json', 'r') as file:
    rules = json.load(file)
# phrases ruleset
with open('phrases.json', 'r') as file:
    phrases = json.load(file)
# emojis
with open('emoji.json', 'r', encoding='utf-8') as file:
    emojis = json.load(file)


def dummify_text(user_input):
    global rules, phrases, emojis

    # Randomization chances
    parentheses_chance = 0.95
    period_chance = 0.05
    whitespace_chance = 0.01
    w_chance = 0.01
    missing_period_chance = 0.2
    missing_space_chance = 0.2
    wrong_letter_chance = 0.1
    no_comma_chance = 0.8

    # Step 1: Lowercase input
    user_input = user_input.lower()

    # Step 2: Separate paragraph into sentences
    sentences = re.split(r'(?<=\.) ', user_input)

    # Step 3: Detect and replace phrases
    for i, sentence in enumerate(sentences):
        for key, phrase_list in phrases.items():
            for phrase in phrase_list:
                if phrase in sentence:
                    sentences[i] = sentence.replace(phrase, key)

    # Step 4: Replace words with typos based on rules
    def replace_words(text, rules):
        words = text.split()
        output = []

        for word in words:
            # Handle punctuation
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

    sentences = [replace_words(sentence, rules) for sentence in sentences]

    # Step 5: Capitalize sentences
    sentences = [sentence.capitalize() for sentence in sentences]

    # Step 6: Remove a period from the final sentence
    if random.random() < missing_period_chance and sentences:
        sentences[-1] = sentences[-1].rstrip('.')

    # Step 7: Remove a space between two words in the paragraph
    output_words = ' '.join(sentences).split()
    if random.random() < missing_space_chance:
        for i in range(len(output_words) - 1):
            if random.random() < 0.5:
                output_words[i] += output_words[i + 1]
                del output_words[i + 1]
                break

    # Step 8: Add random effects to each word
    final_output = []
    for word in output_words:
        if '(' in word and random.random() < parentheses_chance:
            word = word.replace('(', '( ')
        if '.' in word and random.random() < period_chance:
            word = word.replace('.', '..')
        if '\'' in word:
            word = word.replace("'", "")
        if ',' in word and random.random() < no_comma_chance:
            word = word.replace(",", "")
        if random.random() < whitespace_chance:
            final_output.append(word + ' ')
            continue
        if random.random() < w_chance:
            final_output.append(word + ' w')
            continue
        if 'i' in word and random.random() < wrong_letter_chance:
            word = word.replace('i', 'j')
        final_output.append(word)

    # Step 9: Combine the final output
    return ' '.join(final_output)


# state class for managing app state
class DummyState(State):
    user_input: str = ""  # store user input
    output: str = ""  # store processed output

    def set_user_input(self, value):
        self.user_input = value  # Update state with new user input
    
    def process_text(self):
        print(f"User input before processing: {self.user_input}")
        # Process and update output
        self.output = dummify_text(self.user_input)
        print(f"Output after processing: {self.output}")
        # Automatically trigger a UI update by setting the state
        self.set_output(self.output)  


# define the global style
style = {
    "background": "#f6e0b6"
}

# define a function for the main page content
def index():
    return rx.stack(
        rx.box(
            height="2vh",
            bg="#f6a040",
            width="100%",
        ),
        rx.flex(
            "dummy generator",
            bg="#96331a",
            width="100%",
            color="#f6e0b6",
            height="30vh",
            font_family="Smokum, serif",
            align="center",
            justify="center",
            font_size="7em"
        ),
        rx.input(
            placeholder="Type something",
            value=DummyState.user_input,
            on_change=DummyState.set_user_input,  # Correct method for state update
            width="40%",
            height="16vh",
            margin="8em auto 1em auto",
            color="#8b3a23",
            border="dashed #96331a 2px",
            bg="None",
            word_wrap="break-word"
        ),
        rx.button(
            "dummify",
            on_click=DummyState.process_text,  # Properly link to state method
            width="20%",
            height="3vh",
            bg="#96331a",
            color="#f6e0b6",
            margin="0 auto 4em auto"
        ),
        rx.flex(
            rx.text(DummyState.output),  # Correct state access for display
            width="40%",
            height="16vh",
            margin="0.2em auto",
            align="center",
            justify="center",
            bg="None",
            border="dashed #96331a 2px",
            border_radius="2%",
            color="#96331a",
        ),
        rx.box(
            "dummify your text, following the writing patterns of a certain celebrity i'm not gonna disclose. iykyk..",
            bg="#96331a",
            width="100%",
            position="fixed",
            bottom="0",
            font_size="0.8em"
        ),
        flex_direction="column",
        width="100%",
        spacing="0"
    )

# create the app instance
app = rx.App(
    style=style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Smokum&display=swap"
    ],
    state=DummyState
)

# add the main page to the app
app.add_page(index)
