import pandas as pd 
from scipy import stats 
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 350)

data = pd.read_csv("novelty_effect.csv")
data = data.copy()
print(data.head())


#perform a statistical test between the two groups
test = stats.ttest_ind(data.loc[data["test"] == 1] ['pages_visited'],
                       data.loc[data["test"] == 0] ['pages_visited'],
                       equal_var=False)

#t statistics
print("\n T. Statistics")
print(test.statistic)

#p-value
print("\n P. Value")
print(test.pvalue)


#print test results
if (test.pvalue>0.05):
  print ("Non-significant results")
elif (test.statistic>0):
  print ("Statistically better results")
else:
  print ("Statistically worse results")

  # Segment users into new vs old. 
  # We define new as those for which the test/control experience was the same as their sign-up date. 
  # now let's do the test for old users and new users separately

#old users
ab_test_old = stats.ttest_ind(data.loc[(data['test'] == 1) & (data['signup_date']!=data['test_date'])]['pages_visited'], 
                              data.loc[(data['test'] == 0) & (data['signup_date']!=data['test_date'])]['pages_visited'], 
                              equal_var=False)
#t statistics
print("\n Old T Statistics")
print(ab_test_old.statistic)

#p-value
print("\n Old P Value")
print(ab_test_old.pvalue) 

# We divide by 2 p-value significance level because we have run two tests. i.e. we are using the Bonferroni correction
#print test results
if (ab_test_old.pvalue>0.05/2):
  print ("Returning users: Non-significant results")
elif (ab_test_old.statistic>0):
  print ("Returning users: Statistically better results")
else:
  print ("Returning users: Statistically worse results")

  #new users
ab_test_new = stats.ttest_ind(data.loc[(data['test'] == 1) & (data['signup_date']==data['test_date'])]['pages_visited'], 
                              data.loc[(data['test'] == 0) & (data['signup_date']==data['test_date'])]['pages_visited'], 
                              equal_var=False)
# new t statistics
print("\n New T Statistics")
print(ab_test_new.statistic)

#p-value
print("\n New P Value")
print(ab_test_new.pvalue) 


# we divide by 2 p-value significance level because we have run two tests. i.e. we are using the Bonferroni correction
#print test results
if (ab_test_new.pvalue>0.05/2):
  print ("New users: Non-significant results")
elif (ab_test_new.statistic>0):
  print ("New users: Statistically better results")
else:
  print ("New users: Statistically worse results")




