#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf8

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import transformers
import tiktoken


class OpenAIToken:
    def __init__(self):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2")
        self.unit_price = {}
        self.unit_price["Chat"] = {"Input": 0.0015, "Output": 0.002}

    def cal_price_chat(self, input, output):
        input_tokens = self.get_transformers_tokens(input)
        input_price = input_tokens * self.unit_price["Chat"]["Input"] / 1000
        output_tokens = self.get_transformers_tokens(output)
        output_price = output_tokens * self.unit_price["Chat"]["Output"] / 1000
        return input_price + output_price  # US$

    def get_transformers_tokens(self, text: str) -> int:
        # 用tokenizer将文本转换为tokens
        tokens = self.tokenizer.tokenize(text)
        num_tokens = len(tokens)

        return num_tokens

    def get_tiktoken_tokens(self, text: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(text))
        return num_tokens


def show_tokens(text):
    print("text length:[%d]" % (len(text)))
    ai_token = OpenAIToken()

    tokens = ai_token.get_transformers_tokens(text)
    print("transformers tokens:", tokens)

    tokens = ai_token.get_tiktoken_tokens(text, "gpt2")
    print("tiktoken tokens:", tokens)

    price = ai_token.cal_price_chat('', text)
    print("price:%f$, 5$ = %d" % (price, 5/price))


def case1():
    text = "Multiple models, each with different capabilities and price points. Prices are per 1,000 tokens. You can think of tokens as pieces of words, where 1,000 tokens is about 750 words. This paragraph is 35 tokens."
    show_tokens(text)


def case2():
    text = """How to calculate tokens for chatGPT？
To calculate the number of tokens for a text sequence in ChatGPT, you can follow these steps:

    Tokenization: In ChatGPT, the text needs to be segmented into a sequence of words or subword units, called tokens. You can use a tokenizer to convert the text into tokens. The tokenizer used in ChatGPT is based on Byte-Pair Encoding (BPE) algorithm, which can convert the text into a decodable sequence of subword units.

    Counting tokens: Once the text has been segmented into tokens, you can count the number of tokens. In ChatGPT, the number of tokens is equal to the number of tokens contained in the text. You can use the len() function to count the number of tokens.

Here is an example code that can calculate the number of ChatGPT tokens for a given text sequence:
python

import transformers

# Load the ChatGPT tokenizer
tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")

# Convert the text into tokens using the tokenizer
text = "Hello, how are you?"
tokens = tokenizer.tokenize(text)

# Count the number of tokens
num_tokens = len(tokens)

# Print the number of tokens
print("Number of tokens:", num_tokens)

Note that punctuation marks and spaces in the text are also converted into tokens. Therefore, the number of tokens may be higher than the number of words in the text."""
    show_tokens(text)


if __name__ == '__main__':
    case1()
    case2()
