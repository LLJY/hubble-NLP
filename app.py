from flask import Flask, request, jsonify
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
# get the stopwords
stop_words = set(stopwords.words('english'))
punctuation = string.punctuation
# create instance of stemmer so accessing it will be faster
ps = PorterStemmer()
app = Flask(__name__)

@app.route('/hello-flask')
def hello_world():
    return 'Hello World!'

@app.route('/grade-test', methods=['POST'])
def grade_test():
    content = request.get_json()
    # this is a list of keywords
    keywords = content["Keywords"]
    # remove all words that are stopwords
    filtered_keywords = [w for w in keywords if not w in stop_words]
    stemmed_keywords = [ps.stem(w) for w in filtered_keywords]
    answer = content["Answer"]
    # remove punctuations using the translate function
    answer = answer.translate(str.maketrans('', '', string.punctuation))
    # split the answer into a list of words
    answers = answer.split()
    # remove all words that are stop words
    filtered_answers = [w for w in answers if not w in stop_words]
    stemmed_answers = [ps.stem(w) for w in filtered_answers]
    # count the number of stemmed keywords that the student got correct
    correct = 0
    for i in stemmed_keywords:
        if i in stemmed_answers:
            correct += 1
    return {"NumberCorrect": correct}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8100)


