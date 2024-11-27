import reflex as rx
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

class State(rx.State):
    input_text: str = ""  
    output_text: str = ""

    def dummify_input_text(self):
        self.output_text = dummify_text(self.input_text)

    def capitalize_text(self):
        self.output_text = self.input_text.upper()

style = {
    "background": "#f6e0b6",
}

def index():
    return rx.vstack(
        rx.box(
            width="100%",
            bg="#f6a040",
            height="2vh",
        ),
        rx.flex(
            "dummify",
            width="100%",
            bg="#96331a",
            height="15vh",
            font_family="Smokum, serif",
            align="center",
            justify="center",
            font_size="6em",
            color="#f6e0b6",
        ),
        rx.input(
            placeholder="Say something...",
            value=State.input_text,
            on_change=State.set_input_text,
            border="#f6a040 solid 2px",
            margin="10vh auto 5vh auto",
            width="70%",
            height="20vh",
        ),
        rx.button(
            "dummify",
            on_click=State.dummify_input_text,
            bg="#96331a",
            margin="0 auto 5vh auto"
        ),
        rx.box(
            rx.heading(
                State.output_text,
                spacing="0",
                align="center",
                color="#f6a040",
            ),
            padding="20px",
            width="100%",
            text_wrap="wrap",
            margin_x="auto",
            word_break="break-word"
        ),
        spacing="0"
    )

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Smokum&display=swap"
    ],
    style=style
)
app.add_page(index)