import pandas as pd
from utility_functions import *

# Read purchase data
purchase_df=read_data("Purchases.xlsx")

# Remove unused columns
purchase_df=remove_columns(purchase_df, ['Item ID', 'Auction ID', 'bid_count', 'Auction Close Date'])

# Removing null values with no bidder
purchase_df=purchase_df.dropna()
purchase_df = purchase_df[(purchase_df['Price Sold'] != 0.0) & (purchase_df['high_bidder'] != 0.0)]

# List total spent groupped by bidder id
purchase_by_bidder_df=purchase_df.groupby(['high_bidder'])['Price Sold'].sum().reset_index()
# Using a more meaningful name to the column
purchase_by_bidder_df=purchase_by_bidder_df.rename(columns={'Price Sold':'total_spent', 'high_bidder':'Buyer ID'})

# Get nth percentile value for total spent
total_spent_threshold=purchase_by_bidder_df['total_spent'].quantile([0.95]).values[0]
top_n_bidders_df = purchase_by_bidder_df[(purchase_by_bidder_df['total_spent'] >= total_spent_threshold)]

# Read buyer data
buyer_df=read_data("Buyer Profile - Assignment.xlsx")
top_n_bidders_merged_df=pd.merge(top_n_bidders_df, buyer_df, on='Buyer ID')

# Read country and state mapping data
state_df=read_data("State Mapping.xlsx")
country_df=read_data("Country Mapping.xlsx")

# Get Country and State name from the mapping data
top_n_bidders_merged_df['Country'] = top_n_bidders_merged_df['country_id'].map(country_df.set_index('Id')['Country'])
top_n_bidders_merged_df['State'] = top_n_bidders_merged_df['state'].map(state_df.set_index('Id')['State'])
top_n_bidders_merged_df=remove_columns(top_n_bidders_merged_df, ['state', 'country_id'])

top_n_bidders_merged_df = top_n_bidders_merged_df.sort_values(by=['total_spent'], ascending=False)

# Save the top n percentile buyers' information
top_n_bidders_merged_df.to_csv("../Results/top_5_percentile.csv", index=False)