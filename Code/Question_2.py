from utility_functions import *
import calendar

# Read purchase data
purchase_df=read_data("Purchases.xlsx")

# Read buyer data
buyer_df=read_data("Buyer Profile - Assignment.xlsx")

# Removing null values with no bidder
purchase_df=purchase_df.dropna()
purchase_df = purchase_df[(purchase_df['Price Sold'] != 0.0) & (purchase_df['high_bidder'] != 0.0)]

# Get Buyer creation date
purchase_df['created'] = purchase_df['high_bidder'].map(buyer_df.set_index('Buyer ID')['created'])
purchase_df['buyer_created_year'] = pd.DatetimeIndex(purchase_df['created']).year
purchase_df['buyer_created_month'] = pd.DatetimeIndex(purchase_df['created']).month

# List auction contribution calculation by month and year cohorts
purchase_by_year_cohort=dict(purchase_df.groupby(['buyer_created_year'])['Price Sold'].sum().reset_index().values)
purchase_by_month_cohort=dict(purchase_df.groupby(['buyer_created_month'])['Price Sold'].sum().reset_index().values)

# Converting series to dataframe
purchase_by_year_cohort=pd.DataFrame(purchase_by_year_cohort.items(), columns=['Year Cohort', 'Contribution to auction'])
purchase_by_month_cohort=pd.DataFrame(purchase_by_month_cohort.items(), columns=['Month Cohort', 'Contribution to auction'])

# Getting month name from month number
purchase_by_month_cohort['Month Cohort']=purchase_by_month_cohort['Month Cohort'].apply(lambda month_no: calendar.month_abbr[int(month_no)])

# Save cohort analysis results to csv files
purchase_by_year_cohort.to_csv("../Results/yearly_cohort_analysis.csv", index=False)
purchase_by_month_cohort.to_csv("../Results/monthly_cohort_analysis.csv", index=False)