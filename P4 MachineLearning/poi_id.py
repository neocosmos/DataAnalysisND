#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
import numpy as np

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','exercised_stock_options', 'fraction_to_poi', 'shared_receipt_with_poi',
                'restricted_stock', 'fraction_salary', 'total_stock_value', 'from_poi_to_this_person','other'] 
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0 )

financial_features = ['salary', 'bonus', 'long_term_incentive', 'deferred_income','deferral_payments', 
                      'loan_advances', 'other', 'expenses', 'director_fees','total_payments',
                      'exercised_stock_options','restricted_stock', 'restricted_stock_deferred','total_stock_value']
                                                                                                               
BELFER_true = ['NaN', 'NaN', 'NaN', -102500, 'NaN',
              'NaN', 'NaN', 3285, 102500, 3285,
              'NaN', 44093, -44093, 'NaN']
BHATNAGAR_true = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN',
                'NaN','NaN',137864, 'NaN', 137864,
                15456290, 2604490,-2604490, 15456290]           

for idx, i in enumerate(financial_features):
    data_dict['BELFER ROBERT'][i] = BELFER_true[idx]
    data_dict['BHATNAGAR SANJAY'][i] = BHATNAGAR_true[idx]


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
def computeFraction(a, b):
    if a =="NaN" or b == "NaN":
        fraction = 0.
    else:
        fraction = a*1.0/b    
    return fraction

def AddNewFeatures(data_dict):

    for name in data_dict:

        data_point = data_dict[name]
        
        fraction_from_poi = computeFraction( data_point["from_poi_to_this_person"], data_point["to_messages"] )

        fraction_to_poi = computeFraction( data_point["from_this_person_to_poi"], data_point["from_messages"] )

        fraction_salary = computeFraction( data_point["salary"], data_point["total_payments"] )
        #fraction_bonus = computeFraction( data_point["bonus"], data_point["total_payments"] )

        data_dict[name]["fraction_from_poi"] = fraction_from_poi
        data_dict[name]["fraction_to_poi"] = fraction_to_poi
        data_dict[name]["fraction_salary"] = fraction_salary
        #data_dict[name]["fraction_bonus"] = fraction_bonus

		
AddNewFeatures(data_dict)

'''
## feature importance by DT
email_features = ['to_messages', 'fraction_from_poi', 'from_messages', 'from_poi_to_this_person', 'from_this_person_to_poi',
                  'fraction_to_poi','shared_receipt_with_poi'] 
                  
all_features = ["poi"] + financial_features +["fraction_salary"]+ email_features

clf = DecisionTreeClassifier()
test_classifier(clf, data_dict, all_features)

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

for i in range(15):
    print("%d. %s %0.2f" % (i + 1, all_features[indices[i]+1], importances[indices[i]]))
'''

my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
   

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

folds = 1000
cv = StratifiedShuffleSplit(labels, folds, random_state=42)

### Decision Trees
from sklearn.tree import DecisionTreeClassifier

estimators = [('reduce_dim', PCA()), 
              ('clf', DecisionTreeClassifier(criterion='gini',min_samples_split=2,random_state=42))]

params = {
        #'clf__splitter':['best','random'],
        #'clf__max_features':['log','sqrt',None],
        #'clf__min_samples_split':[2,3,4,5,10],
        #'clf__criterion': ['gini', 'entropy'],
        #'clf__min_samples_leaf':[1,2,5]
        }
pipe = Pipeline(estimators)       

clf = GridSearchCV(pipe, param_grid=params, cv=cv, scoring='f1')        
clf.fit(features, labels)
 
clf = clf.best_estimator_      
#test_classifier(clf, my_dataset, features_list)

'''
Pipeline(steps=[('reduce_dim', PCA(copy=True, iterated_power='auto', n_components=None, random_state=None,
  svd_solver='auto', tol=0.0, whiten=False)), ('clf', DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=42, splitter='best'))])
        Accuracy: 0.82779       Precision: 0.39424      Recall: 0.38300 F1: 0.38854     F2: 0.38520
        Total predictions: 14000        True positives:  766    False positives: 1177   False negatives: 1234   True negatives: 10823
'''


### Gauss NB
'''
from sklearn.naive_bayes import GaussianNB

estimators = [('reduce_dim', PCA()), 
              ('clf', GaussianNB())]

params = {
        }
pipe = Pipeline(estimators)       

clf = GridSearchCV(pipe, param_grid=params, cv=cv, scoring='f1')        
clf.fit(features, labels)
      
clf = clf.best_estimator_      
test_classifier(clf, my_dataset, features_list)
'''
'''
Pipeline(steps=[('reduce_dim', PCA(copy=True, iterated_power='auto', n_components=None, random_state=None,
  svd_solver='auto', tol=0.0, whiten=False)), ('clf', GaussianNB(priors=None))])
        Accuracy: 0.83907       Precision: 0.39485      Recall: 0.23750 F1: 0.29660     F2: 0.25807
        Total predictions: 14000        True positives:  475    False positives:  728   False negatives: 1525   True negatives: 11272
'''


### SVM
'''
from sklearn import svm
estimators = [ ('scale', MinMaxScaler()),
               #('reduce_dim', PCA()), 
               ('clf', svm.SVC(C=10000, gamma=0.0001, kernel='linear', random_state=42))]

params = {
         #'clf__C': [10,1000,10000],	
         #'clf__gamma': [0.00001,0.0001,0.1],
        }
pipe = Pipeline(estimators)       

clf = GridSearchCV(pipe, param_grid=params, cv=cv, scoring='f1')        
clf.fit(features, labels)
      
clf = clf.best_estimator_      
test_classifier(clf, my_dataset, features_list)
'''

### Random Forest
'''
from sklearn.ensemble import RandomForestClassifier
estimators = [ #('scale', MinMaxScaler()),
               #('reduce_dim', PCA()), 
               ('clf', RandomForestClassifier(random_state=42))]

params = {
          #'clf__max_depth':[2,5,10],
          'clf__min_samples_split':[2,5,10],
          'clf__n_estimators': [10,50,100]         
        }
pipe = Pipeline(estimators)       

clf = GridSearchCV(pipe, param_grid=params, cv=cv, scoring='f1')        
clf.fit(features, labels)
     
clf = clf.best_estimator_      
test_classifier(clf, my_dataset, features_list)

# Accuracy: 0.86143       Precision: 0.55190      Recall: 0.15950 F1: 0.24748     F2: 0.18594
#        Total predictions: 14000        True positives:  319    False positives:  259   False negatives: 1681   True negatives: 11741
'''

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)