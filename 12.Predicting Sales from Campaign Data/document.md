Problem statement:

Marketing teams often invest heavily in influencer campaigns — paying creators to promote products on social media platforms like Instagram. But understanding which factors actually drive product sales is critical to making better decisions about who to work with, how much to spend, and how to design content.

The goal is to build a predictive model that can estimate how many units of a product will be sold based on key influencer campaign attributes.

Dataset link: https://drive.google.com/drive/folders/1BCTayfVYwapGcGl3Mizik1E6-zPcQ_DT?usp=sharing

Dataset Overview: The dataset contains historical data from multiple influencer campaigns. It includes features like:

Followers: Number of Instagram followers the influencer had at the time of the campaign
EngagementRate (%): Engagement rate on posts (likes/comments per follower)
AdSpend (GBP): Total money spent on the campaign
ContentQuality: Subjective score (1–10) reflecting the quality of the influencer's content
Sales (Units): The number of product units sold as a result of the campaign (target variable)
Timestamp: the day the compaign had ended
Additional columns like "Timestamp" and "Notes" were additionally included.

Approach document: https://docs.google.com/document/d/1BG9fACg-wZtZCimqDR-O7Fdw0P525JXHRb6y45UFBW8/edit?usp=sharing

Note: The dataset is messy and contains:

Missing values
Inconsistent formats (e.g., "£5000", "3.2%")
Outliers (e.g., billions of followers, negative spend)
Mixed scales (some follower counts are in thousands)
This reflects a realistic scenario where the data was pulled together quickly from different sources.
Datasets:

messy_train_data.csv - the training set you will have to clean and fit a model
messy_test_data.csv - the testing set you will have to clean and predict on
Suggested Steps:

Clean the data
Explore and visualize relationships
Engineer better features (e.g., log transforms, interactions)
Train regression model
Perform Hyperparameter tuning and cross validation to build robust model
Evaluate using metrics like RMSE and R²
Success Criteria

A model with good predictive accuracy (high R², low RMSE)
Clear insights into which factors matter most for driving sales
A pipeline(a simple function) that can handle future messy campaign data reliably