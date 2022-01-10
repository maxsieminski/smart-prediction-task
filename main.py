import json
from prediction import TypePrediction


def main():
    choice = 1

    if choice == 1:
        question = input("Ask me a question: ")
        type_prediction = TypePrediction(question)
        prediction = type_prediction.get_prediction()
        type_prediction.print_question_statistics()
        print(prediction)
    elif choice == 2:
        file = open("resources/dbpedia/task1_dbpedia_test.json")
        data = json.load(file)
        file.close()


if __name__ == "__main__":
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('maxent_ne_chunker')
    # nltk.download('words')
    main()
