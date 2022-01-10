import json
import sys
from prediction import TypePrediction


def main():
    print(
        "===============================\n"
        "1 - Ask a question\n"
        "2 - Validate JSON\n"
        "0 - Exit\n"
        "===============================\n"
    )
    while True:
        choice = int(input("Input choice: "))

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
        elif choice == 0:
            break


if __name__ == "__main__":
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('maxent_ne_chunker')
    # nltk.download('words')
    main()
