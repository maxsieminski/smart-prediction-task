from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer

WH_WORDS = ["WRB", "WDT", "WP", "WP$"]
WH_NUMERICAL_WORDS = ["many", "much", "short", "big", "deep", "long", "old"]
WH_PERSONAL_WORDS = ["which, what"]


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def get_wh_words(lemmatized_pos_tagged_question, pos_tags):
    wh_words_list = []

    for pos in pos_tags:
        if pos in WH_WORDS:
            pos_tag_index = pos_tags.index(pos)
            wh_word = lemmatized_pos_tagged_question[pos_tag_index]
            if wh_word == "how":
                if lemmatized_pos_tagged_question[pos_tag_index + 1] in WH_NUMERICAL_WORDS:
                    wh_word += f" {lemmatized_pos_tagged_question[pos_tag_index + 1]}"
                    wh_word += " - numerical"
            elif wh_word in WH_PERSONAL_WORDS or lemmatized_pos_tagged_question[pos_tag_index + 1 == "be"]:
                wh_word += " - whatwho"
            wh_words_list.append(wh_word)
    return wh_words_list


def lemmatize(tagged_tokens):
    lemmatizer = WordNetLemmatizer()

    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), tagged_tokens))

    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return lemmatized_sentence


def tag_pos(tokenized_question):
    return pos_tag(tokenized_question)


def tokenize(question):
    return word_tokenize(question)


def parse_question(question):
    tokenized_question = tokenize(question)
    pos_tagged_question = tag_pos(tokenized_question)
    pos_tags = [word[1] for word in pos_tagged_question]
    lemmatized_pos_tagged_question = lemmatize(pos_tagged_question)
    print(lemmatized_pos_tagged_question)
    wh_words = get_wh_words(lemmatized_pos_tagged_question, pos_tags)
    print(wh_words)
