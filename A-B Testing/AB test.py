from scipy import stats 
import pandas as pd 
data = pd.read_csv("test_basic.csv")
data = data.copy()
#check conversion rate for both groups

conversion_rate = data.groupby('test')['conversion'].mean()
print("\nConversion rate for both groups ")
print(conversion_rate)

#perform a statistical test between the two groups
test = stats.ttest_ind(data.loc[data['test'] == 1]['conversion'], 
                       data.loc[data['test'] == 0]['conversion'], 
                      equal_var=False)
print(test.statistic)

print("\np-value")
print(test.pvalue)

#print test results

if(test.pvalue>0.05):
  print("Non-significant results")
elif(test.statistic>0):
  print("Statistically better results")
else:
 print("Statistically worse results")


