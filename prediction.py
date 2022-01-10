from question import Question

"""
All questions are in lemmatized form
"""

STRING_QUESTIONS = ["how", "why"]
DATE_QUESTION = "when"
RESOURCE_PERSON_QUESTIONS = ["who", "whose", "whom"]
RESOURCE_PLACE_QUESTIONS = ["which", "what", "where"]
BOOLEAN_QUESTION = "be"


class TypePrediction:
    def __init__(self, question):
        self.question = Question(question)

    def print_question_statistics(self):
        self.question.print_statistics()

    def get_prediction(self):
        if self.question.question_words:
            if self.question.lemmatized[0].lower() in DATE_QUESTION:
                return ["LITERAL", "date"]
            elif "hownum" in [word.lower() for word in self.question.question_words]:
                return ["LITERAL", "number"]
            elif any(question.lower() in RESOURCE_PLACE_QUESTIONS for question in self.question.question_words)\
                    or any(question.lower() in RESOURCE_PERSON_QUESTIONS for question in self.question.question_words):
                return ["RESOURCE", self.__get_resource_type()]
            elif any(question.lower() in STRING_QUESTIONS for question in self.question.question_words)\
                    or "whatbe" in [word.lower() for word in self.question.question_words]:
                return ["LITERAL", "string"]
            elif BOOLEAN_QUESTION in self.question.question_words:
                return ["BOOLEAN", "boolean"]
            else:
                return ["FAILED", None]

    def __get_resource_type(self):
        first_word_lemmatized = self.question.lemmatized[0].lower()
        second_word_lemmatized = self.question.lemmatized[1].lower()

        if first_word_lemmatized in RESOURCE_PERSON_QUESTIONS:
            return "dbo:Person"
        elif first_word_lemmatized == "where" \
                or (first_word_lemmatized == "in" and second_word_lemmatized in RESOURCE_PLACE_QUESTIONS) \
                or (first_word_lemmatized in ["what", "which"] and second_word_lemmatized in ["city", "town", "country", "place", "state", "states"]):
            return "dbo:Place"
