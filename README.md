# A-B-Testing-Analytics-Project

This project demonstrates an end-to-end A/B testing analysis workflow using Python, statistical testing, and data-driven decision-making.

# The analysis covers:
Conversion rate comparison between control and test groups
Statistical significance testing using hypothesis testing
Detection and correction of randomization bias
Novelty effect analysis (new vs returning users)
Sample size estimation for experiment design

The goal is to simulate real-world experimentation scenarios and apply best practices in experimentation and analytics.

# Tech Stack
  Python
  Pandas
  NumPy
  SciPy
  Statsmodels
  Matplotlib
  Scikit-learn (Decision Tree for bias detection

# Project Structure
  ├── AB test.py
├── Overview.py
├── Randomization.py
├── Randomization Exercise.py
├── Novelty Effect.py
├── Sample Size.py
├── test_basic.csv
├── novelty_effect.csv

# 1. Basic A/B Test Analysis
Calculates conversion rates for control vs test groups
Performs independent t-test to evaluate statistical significance
Interprets results based on p-value and test 

# 2. Dataset Exploration
Loads and inspects dataset structure
Validates data before analysis

# 3. Randomization Bias Detection
Identifies imbalance across test/control groups (e.g., country distribution)
Uses:
Grouped proportions
Decision Tree classifier to detect bias drivers
Compares biased vs cleaned datasets

# 4. Randomization Correction (Advanced)
Adjusts dataset to rebalance distributions
Uses oversampling to align group proportions
Re-runs statistical test after correction

# 5. Novelty Effect Analysis
Evaluates whether new users behave differently from returning users
Splits users into:
New users (signup_date == test_date)
Returning users
Applies Bonferroni correction for multiple testing

# 6. Sample Size Estimation
Calculates required sample size for detecting meaningful changes
Uses:
Statistical power (80%)
Significance level (5%)
Visualizes relationship between effect size and sample size







  


