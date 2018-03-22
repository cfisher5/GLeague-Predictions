import pandas as pd
from sklearn import neighbors, naive_bayes, preprocessing
from sklearn.svm import SVC

clusters = {
    '0': 'Low Usage Defender',
    '1': 'Inside Scoring Big',
    '2': 'Facilitator',
    '3': 'Swiss Army Knife',
    '4': 'Sweet-Shooting Bucket Getter',
    '5': 'High Usage Scoring Big'
}


def get_cluster_name(num):
    return clusters[num]


def format_data(test, hw_flag):
    data = pd.read_csv("data/training_data.csv", sep=",")
    if hw_flag:
        data = data[['Gl 3Pmpg', 'Gl Astpg', 'Gl Fgapg', 'Gl Ptspg', 'Gl Rebpg', 'GLeague Clusters', 'Height', 'Weight']]
    else:
        data = data[['Gl 3Pmpg', 'Gl Astpg', 'Gl Fgapg', 'Gl Ptspg', 'Gl Rebpg', 'GLeague Clusters']]

    data['GLeague Clusters'] = data['GLeague Clusters'].map(
        {'Low Usage Defenders': 0, 'Inside Scoring Bigs ': 1, 'Facilitators': 2,
         'Swiss Army Knives': 3, 'Sweet-Shooting Bucket Getters': 4, 'High Usage Scoring Bigs': 5})

    X = data.drop('GLeague Clusters', axis=1)
    std_scale = preprocessing.StandardScaler().fit(X)
    X_train = std_scale.transform(X)
    X_test = std_scale.transform(test)
    y = data['GLeague Clusters']
    return X_train, y, X_test


def svm(X_train, y_train, test, ):
    print("********************************************************************")
    print("SVM")
    model = SVC()
    model.fit(X_train, y_train)
    preds = model.predict(test)
    print(preds)


def knn(X_train, y_train, test):
    neigh = neighbors.KNeighborsClassifier(n_neighbors=5)
    neigh.fit(X_train, y_train)
    comps = None
    for player in test:
        comps = neigh.kneighbors([player], 3)
    y_predict = neigh.predict(test)
    return get_cluster_name(str(y_predict[0])), comps[1][0]


def gaussian_nb(X_train, y_train, test):
    gnb = naive_bayes.GaussianNB()
    gnb.fit(X_train, y_train)
    preds = gnb.predict(test)
    return get_cluster_name(str(preds[0]))