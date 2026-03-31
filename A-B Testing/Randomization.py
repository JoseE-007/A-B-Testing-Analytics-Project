import pandas as pd 
import graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from graphviz import Source 
from scipy import stats
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 350)

data = pd.read_csv('randomization.csv')
data = data.copy()

#print(data.head())

#let's group by source and estimate relative frequencies
counts = (
    data.groupby(["source", "test"])
        .size()
        .unstack(fill_value=0)
)

# convert to column-wise proportions (normalize within each test group)
data_grouped_source = (
    counts.div(counts.sum(axis=0), axis=1)
          .rename(columns={0: "frequency_test_0", 1: "frequency_test_1"})
          .round(6)
)

print(data_grouped_source) 

# drop user_id, not needed
data = data.drop(['user_id'], axis=1)

# make dummy vars. Don't drop one level here, keep them all. 
# You don't want to risk dropping the one level that actually creates problems with the randomization
data_dummy = pd.get_dummies(data)
# model features, test is the label and conversion is not needed here
train_cols = data_dummy.drop(['test', 'conversion'], axis=1)

tree=DecisionTreeClassifier(
    # change weights. Our data set is now perfectly balanced. It makes easier to look at tree output
    class_weight="balanced",
    # only split if if it's worthwhile. The default value of 0 means always split no matter what if you can increase overall performance,
    # which creates tons of noisy and irrelevant splits
    min_impurity_decrease = 0.001
    )
tree.fit(train_cols,data_dummy['test'])
  
export_graphviz(tree, out_file="tree_test.dot", feature_names=train_cols.columns, proportion=True, rotate=True)
s = Source.from_file("tree_test.dot")

# s.view()

print(data_dummy.groupby("test")[["country_Argentina", "country_Uruguay"]].mean()) 

''''' Suggested Query:
original_data = stats.ttest_ind(data_dummy.loc[data['test'] == 1]['conversion'],
                                data_dummy.loc[data['test'] == 0]['conversion'],
                                equal_var=False)
#this is after removing Argentina and Uruguay
data_no_AR_UR = stats.ttest_ind(data_dummy.loc[(data['test'] == 1) & (data_dummy['country_Argentina'] ==  0) & (data_dummy['country_Uruguay'] ==  0)]['conversion'],

                                data_dummy.loc[(data['test'] == 0) & (data_dummy['country_Argentina'] ==  0) & (data_dummy['country_Uruguay'] ==  0)]['conversion'],

                                equal_var=False)
print(pd.DataFrame( {"data_type" : ["Full", "Removed_Argentina_Uruguay"],
                         "p_value" : [original_data.pvalue, data_no_AR_UR.pvalue],
                         "t_statistic" : [original_data.statistic, data_no_AR_UR.statistic]
                         })) '''

#Friendly Query:

# 1. Create a "Clean" slice of the data first (much easier to read!) Just one time. 
is_not_biased = (data_dummy['country_Argentina'] == 0) & (data_dummy['country_Uruguay'] == 0)
data_clean = data_dummy[is_not_biased]


# 2. Run the tests using the simple variables
res_full  = stats.ttest_ind(data_dummy[data_dummy['test']==1]['conversion'], 
                            data_dummy[data_dummy['test']==0]['conversion'], equal_var=False)

res_clean = stats.ttest_ind(data_clean[data_clean['test']==1]['conversion'], 
                            data_clean[data_clean['test']==0]['conversion'], equal_var=False)

# 3. Create the summary table
summary = pd.DataFrame({
    "Dataset": ["Full (Biased)", "Clean (No AR/UR)"],
    "T-Statistic": [res_full.statistic, res_clean.statistic],
    "P-Value": [res_full.pvalue, res_clean.pvalue]
})

print(summary)