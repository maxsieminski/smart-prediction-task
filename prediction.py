from SPARQLWrapper import SPARQLWrapper, JSON

from question import Question

"""
All questions are in lemmatized form
"""

STRING_QUESTIONS = ["how", "why"]
DATE_QUESTION = "when"
RESOURCE_PERSON_QUESTIONS = ["who", "whose", "whom"]
RESOURCE_PLACE_QUESTIONS = ["which", "where"]
BOOLEAN_QUESTION = "be"


class TypePrediction:
    def __init__(self, question):
        self.question = Question(question)
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def print_question_statistics(self):
        self.question.print_statistics()

    def get_prediction(self):
        if self.question.question_words:
            if self.question.lemmatized[0].lower() in DATE_QUESTION:
                return ["LITERAL", "date"]
            elif "hownum" in [word.lower() for word in self.question.question_words]:
                return ["LITERAL", "number"]
            elif any(question.lower() in RESOURCE_PLACE_QUESTIONS for question in self.question.question_words) \
                    or any(question.lower() in RESOURCE_PERSON_QUESTIONS for question in self.question.question_words):
                return ["RESOURCE", self.__get_resource_type()]
            elif any(question.lower() in STRING_QUESTIONS for question in self.question.question_words) \
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
                or (first_word_lemmatized in ["what", "which"] and second_word_lemmatized in ["city", "town", "country",
                                                                                              "place", "state",
                                                                                              "states"]):
            return "dbo:Place"

        resource_lookup_word = ""

        if self.question.lemmatized[0].lower() == "which" and not self.question.lemmatized[1].lower() == "be":
            resource_lookup_word = self.question.lemmatized[1]
        else:
            if self.question.nouns:
                resource_lookup_word = self.question.nouns[0]

        if resource_lookup_word:
            self.sparql.setQuery("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" \
                                 "PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>\n" \
                                 "PREFIX dbo:  <http://dbpedia.org/ontology/>\n" \
                                 "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" \
                                 "\n" \
                                 "SELECT DISTINCT ?item\n" \
                                 " WHERE\n" \
                                 "   {  \n" \
                                 "     ?item rdfs:label \"" + resource_lookup_word.lower() + "\"@en. \n" \
                                                                                             "?item rdf:type "
                                                                                             "owl:Class.  \n" \
                                                                                             "   }")

            self.sparql.setReturnFormat(JSON)

            if self.sparql.query().convert()['results']['bindings']:
                return self.sparql.query().convert()['results']['bindings'][0]['item']['value']
            else:
                return None
