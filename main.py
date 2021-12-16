import nltk
from question import parse_question




def preprocess(question="Which are how many the best writers of the Cavalcade Why of America and Where The United States Steel Hour?"):
    # lemmatizer = WordNetLemmatizer()
    # tokens = word_tokenize(question)
    # tagged_tokens = pos_tag(tokens)
    # wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), tagged_tokens))
    #
    # lemmatized_sentence = []
    # for word, tag in wordnet_tagged:
    #     if tag is None:
    #         # if there is no available tag, append the token as is
    #         lemmatized_sentence.append(word)
    #     else:
    #         # else use the tag to lemmatize the token
    #         lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    # lemmatized_sentence = " ".join(lemmatized_sentence)
    #
    # print(lemmatized_sentence)
    parse_question(question)


def main():
    print("======================")
    print("1. nie zesraj sie prrryk")
    print("======================")
    choice = 1 #int(input("Wpisuj : "))

    if choice == 1:
        preprocess()


if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    main()
