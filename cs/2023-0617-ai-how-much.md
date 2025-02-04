# 使用chatGPT聊天到底要花多少钱？

摘要：我们来算算现在的chatGPT价格实际到底是多少

OpenAI在6月13日刚刚进行了大规模降价和升级，text-embedding-ada-002降价95%，GPT-3.5-turbo降价了25%，GPT4最高可支持32K文本。

在OpenAI的官网（ https://openai.com/pricing ）上，对chatGPT的价格计算方式有详细的说明。但是其价格是以token来计算的，我们来算算现在的价格实际到底是多少。

## 官网聊天

官方网页上聊天是不花钱的，收费项目主要针对API用户。API用户默认赠送5美元额度。

## 大语言模型

### 计算方法

测试样本：
Multiple models, each with different capabilities and price points. Prices are per 1,000 tokens. You can think of tokens as pieces of words, where 1,000 tokens is about 750 words. This paragraph is 35 tokens.
官方的样本文字中说明了，这段测试样本的长度为35个tokens。

ChatGPT使用的tokenizer是Byte-Pair Encoding(BPE)算法，有三种方法可以近似计算token值：

1. Transformers
2. OpenAI tiktoken
3. 单词数 / 0.75

使用Transformers方法对测试样本进行tokens计算：
```
def get_transformers_tokens(text: str, encoding_name: str) -> int:
    tokenizer = transformers.AutoTokenizer.from_pretrained(encoding_name)

    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)

    return num_tokens
```
得到tokens值为45。

使用tiktoken的方法对测试样本进行tokens计算：
```
def get_tiktoken_tokens(text: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens
```
得到tokens值也为45。

有趣的是，得出的值是45，和openai官方网页中给出35不同，但使用openai官方计算器（ https://platform.openai.com/tokenizer ）计算的结果，也是45。
又找到一个工具也可以计算tokens值：https://articlefiesta.com/seo-tools/token-calculator
这个工具得出的tokens值却是35。

出现两种不同的值，可能的原因是使用了不同的Tokenizer，不同的Tokenizer会得到不同的计算结果，因为并不知道openai实际使用的Tokenizer是什么，所以这里就使用gpt2分词器近似计算。

tokens的消耗，至少受到以下三个因素的影响：
1. System Prompt：聊天的背景信息，告诉chatGPT聊天的背景是什么，一般会被软件包装掉了，用户看不到；
2. User Prompt：用户的提问；
3. AI's Reply：chatGPT的回答；

用以下样本为例，看下实际的费用：
```
How to calculate tokens for chatGPT？
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

Note that punctuation marks and spaces in the text are also converted into tokens. Therefore, the number of tokens may be higher than the number of words in the text.
```

### Chat

Model	Input	Output
4K context	$0.0015 / 1K tokens	$0.002 / 1K tokens
16K context	$0.003 / 1K tokens	$0.004 / 1K tokens

将上面的样本内容和定价带入，可以计算出，5美元对应的对话次数是6887。也就是账号自带的5美元额度，大约可以聊6、7千句英文对话（中文对话会有所出入）。

通过此方法可以自行计算其他收费项目的具体价格情况：

### GPT-4

Model	Input	Output
8K context	$0.03 / 1K tokens	$0.06 / 1K tokens
32K context	$0.06 / 1K tokens	$0.12 / 1K tokens

### InstructGPT

Ada $0.0004 / 1K tokens
Babbage $0.0005 / 1K tokens
Curie $0.0020 / 1K tokens
Davinci $0.0200 / 1K tokens

### Fine-tuning models

Model	Training	Usage
Ada	$0.0004 / 1K tokens	$0.0016 / 1K tokens
Babbage	$0.0006 / 1K tokens	$0.0024 / 1K tokens
Curie	$0.0030 / 1K tokens	$0.0120 / 1K tokens
Davinci	$0.0300 / 1K tokens	$0.1200 / 1K tokens

### Embedding models

Model	Usage
Ada v2	$0.0001 / 1K tokens
Ada v1	$0.0040 / 1K tokens
Babbage v1	$0.0050 / 1K tokens
Curie v1	$0.0200 / 1K tokens
Davinci v1	$0.2000 / 1K tokens

## Other models

### Image models

Resolution	Price
1024×1024	$0.020 / image
512×512	$0.018 / image
256×256	$0.016 / image

### Audio models

Model	Usage
Whisper	$0.006 / minute (rounded to the nearest second)

# 总结

虽然openai提供了token计算工具，但工具的计算值却和官方网页中的说明不一致。
使用API访问chatGPT3.5的话，账号自带的5美元，大约可以聊6000多句对话。

想深入理解token和分词，需要进一步深度学习如下概念：
- BPE（Byte Pair Encoder，字节对编码）
- BERT（Google的一种预训练语言模型）
- Subword（子词）
- WordPiece（Google提出的一种子词划分算法）
- Tokenize（分词）
- Tokenizer（分词器）
- Tokenization（使用分词的算法模型将句子划分为一个个词）
- Vocabulary（词表）
- 古典分词方法

公众号中回复tokens，获取文中计算tokens的python源代码文件。
