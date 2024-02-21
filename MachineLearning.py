import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score,recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.inspection import permutation_importance

#training n testing data
data=pd.read_csv("features.csv")
data=data.drop(index=0)
data = data[data['AverageWordLength'] >= 1]

data.to_csv('filtered_data.csv', index=False)
X=data.drop('tag',axis=1)

y= data["tag"]
print(len(X)) # prints how many emails it is using for training after any filters



#new data
new_data = pd.read_csv("newphishingfeatures.csv")
new_data = new_data[new_data['AverageWordLength'] >= 1]
X_new = new_data.drop('tag', axis=1)


#split emaildata into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=67)
print("KNeighborsClassifier")

NearN = KNeighborsClassifier(n_neighbors=7)

NearN.fit(X_train, y_train)

y_pred = NearN.predict(X_test)
y_pred_probs_new = NearN.predict(X_new)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='phishing')
f1 = f1_score(y_test, y_pred, pos_label='phishing')
recall = recall_score(y_test, y_pred, pos_label='phishing')
print("Accuracy:", accuracy)
print("Precision:", precision)
print("F1 Score:", f1)
print("recall:", recall)
print(y_pred_probs_new)





print("Random Forest")
rf = RandomForestClassifier(class_weight='balanced',max_depth=2)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
y_pred_probs_new = rf.predict(X_new)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='phishing')
f1 = f1_score(y_test, y_pred, pos_label='phishing')
recall = recall_score(y_test, y_pred, pos_label='phishing')
print("Accuracy:", accuracy)
print("Precision:", precision)
print("F1 Score:", f1)
print("recall:", recall)
print(y_pred_probs_new)
feature_importances = pd.DataFrame(rf.feature_importances_, index=X_train.columns, columns=['importance']).sort_values('importance', ascending=False)
print(feature_importances)

print("GaussianNB")
NaB = GaussianNB()
NaB.fit(X_train,y_train)

y_pred = NaB.predict(X_test)
y_pred_probs_new = NaB.predict(X_new)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='phishing')
f1 = f1_score(y_test, y_pred, pos_label='phishing')
recall = recall_score(y_test, y_pred, pos_label='phishing')
print("Accuracy:", accuracy)
print("Precision:", precision)
print("F1 Score:", f1)
print("recall:", recall)
print(y_pred_probs_new)

