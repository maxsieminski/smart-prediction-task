import spacy
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


# FROM https://www.tutorialexample.com/improve-nltk-word-lemmatization-with-parts-of-speech-nltk-tutorial/
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


QUESTION_POS = ["WDT", "WRB", "WP", "WP$"]
NUMERIC_QUESTIONS = ["many", "much", "short", "long", "old", "young", "big", "small", "high"]


class Question:
    def __init__(self, question):
        self.question: str = question
        self.tokens: list[str] = [token.lower() for token in word_tokenize(question)]
        self.parts_of_speech: list[str] = pos_tag(self.tokens)
        self.lemmatized: list[str] = self.__lemmatize()
        self.named_entities: list[tuple] = self.__tag_entities()
        self.places: list[str] = self.__extract_places()
        self.organizations: list[str] = self.__extract_organizations()
        self.persons: list[str] = self.__extract_persons()
        self.question_words = self.__extract_question_words()
        self.nouns = self.__extract_nouns()

    def print_statistics(self):
        print(f"QUESTION: {self.question}\n"
              f"TOKENS: {self.tokens}\n"
              f"PARTS OF SPEECH: {[pos for word, pos in self.parts_of_speech]}\n"
              f"LEMMATIZED: {self.lemmatized}\n"
              f"NAMED ENTITIES: {self.named_entities}\n"
              f"PLACES: {self.places}\n"
              f"ORGANIZATIONS: {self.organizations}\n"
              f"PERSONS: {self.persons}\n"
              f"QUESTION WORDS: {self.question_words}\n"
              f"NOUNS: {self.nouns}"
              )

    def __lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        lemmatized = []

        for word, pos in self.parts_of_speech:
            wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
            lemmatized.append(lemmatizer.lemmatize(word=word, pos=wordnet_pos))

        return lemmatized

    def __tag_entities(self):
        nlp = spacy.load("en_core_web_md")
        doc = nlp(self.question)
        return [(X, X.ent_iob_, X.ent_type_) for X in doc]

    def __extract_persons(self):
        persons: list[str] = []
        person: list[str] = []

        for word, token, entity in self.named_entities:
            if token == "O":
                if person:
                    persons.append(' '.join(person))
                    person.clear()

            if entity == "PERSON":
                if token == "B" or token == "I":
                    person.append(str(word))
                if word == self.named_entities[-1][0]:
                    persons.append(' '.join(person))

        return persons

    def __extract_organizations(self):
        organizations: list[str] = []
        organization: list[str] = []

        for word, token, entity in self.named_entities:
            if token == "O":
                if organization:
                    organizations.append(' '.join(organization))
                    organization.clear()

            if entity == "ORG":
                if token == "B" or token == "I":
                    organization.append(str(word))
                if word == self.named_entities[-1][0]:
                    organizations.append(' '.join(organization))

        return organizations

    def __extract_places(self):
        places: list[str] = []
        place: list[str] = []

        for word, token, entity in self.named_entities:
            if token == "O":
                if place:
                    places.append(' '.join(place))
                    place.clear()

            if entity == "GPE":
                if token == "B" or token == "I":
                    place.append(str(word))
                if word == self.named_entities[-1][0]:
                    places.append(' '.join(places))

        return places

    def __extract_question_words(self):
        question_words: dict = {}
        temp_words: dict = {}

        for i in range(len(self.parts_of_speech)):
            if self.parts_of_speech[i][1] in QUESTION_POS:
                question_words[self.lemmatized[i]] = i

        for word, index in question_words.items():
            if word.lower() == "how" and self.lemmatized[index + 1] in NUMERIC_QUESTIONS:
                temp_words[word+"num"] = word
            # if word.lower() == "which" or (word.lower() == "what" and self.lemmatized[index + 1] == "be"):
            if word.lower() == "what" and self.lemmatized[index + 1] == "be":
                temp_words[word+"be"] = word

        for word, old_word in temp_words.items():
            question_words[word] = question_words.pop(old_word)

        return [word for word, index in question_words.items()]

    def __extract_nouns(self):
        nouns: list[str] = []

        for i in range(len(self.parts_of_speech)):
            if self.parts_of_speech[i][1] == "NN" or self.parts_of_speech[i][1] == "NNS":
                nouns.append(self.lemmatized[i])

        return nouns
