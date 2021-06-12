from joblib import dump, load
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


class CovidClf:
    def __init__(self):
        self.clf = MLPClassifier(   
                                    solver='lbfgs',
                                    activation='relu',
                                    alpha=1e-3,
                                    hidden_layer_sizes=(10, 10, 10),
                                    max_iter = 10000,
                                    tol = 1e-8,
                                    n_iter_no_change = 100
                                )
        self.prediction = []

    def save_to_file(self):
        dump(self.clf, 'prediction/covidModel.joblib')

    def load_from_file(self):
        self.clf = load('prediction/covidModel.joblib')

    def fit_clf(self, x, y):
        sc3 = StandardScaler()
        x = sc3.fit_transform(x)
        self.clf.fit(x, y)
    
    def predict_clf(self, x):
        sc3 = StandardScaler()
        x = sc3.fit_transform(x)
        self.predicition = self.clf.predict(x)
        return self.predicition