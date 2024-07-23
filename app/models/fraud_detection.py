import nltk
import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, classification_report

nltk.download('stopwords')
nltk.download('wordnet')

ps = WordNetLemmatizer()
cv = TfidfVectorizer(max_features=2000)

def load_data(file_path):
    return pd.read_csv(file_path, sep='\t', names=['label', 'content'])

def preprocess_data(data):
    stop_words = set(stopwords.words('english'))
    corpos = []
    for content in data['content']:
        review = re.sub('[^a-zA-Z]', ' ', content)
        review = review.lower()
        words = review.split()
        words = [ps.lemmatize(word) for word in words if word not in stop_words]
        review = ' '.join(words)
        corpos.append(review)
    return corpos

def train_model(corpus, labels):
    x = cv.fit_transform(corpus).toarray()
    x_train, x_test, y_train, y_test = train_test_split(x, labels, test_size=0.20, random_state=0)
    model = MultinomialNB().fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Model has trained.")
    print("Evaluation metrics:")
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("Accuracy score:", accuracy_score(y_test, y_pred))
    print("Recall score:", recall_score(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred))
    return model

def preprocess_input(input_text):
    stop_words = set(stopwords.words('english'))
    review = re.sub('[^a-zA-Z]', ' ', input_text)
    review = review.lower()
    words = review.split()
    words = [ps.lemmatize(word) for word in words if word not in stop_words]
    review = ' '.join(words)
    x_input = cv.transform([review]).toarray()
    return x_input

def predict_label(input_text, model):
    x_input = preprocess_input(input_text)
    prediction = model.predict(x_input)[0]
    return 'normal call' if prediction == 1 else 'fraud'
