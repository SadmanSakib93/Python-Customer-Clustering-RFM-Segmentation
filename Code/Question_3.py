from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from utility_functions import *

def unsupervised_clustering(X):
    """ Removed specified columns from a DataFrame

        Args:
            X: Numpy array
                Array containing the featuers which will be used to perform the clustering
                
        Returns: 
            cluster_labels: list
                List of cluster labels obtained after the clustering is completed
    """
    
    #Bring the data on same scale by stndardization
    scale = StandardScaler()
    buyer_df_for_clustering = scale.fit_transform(X)
    
    # Number of clusters
    best_k=3
    
    # Perform the clustering via unsupervised machine learning-based K-means method
    cluster_labels = KMeans(n_clusters=best_k, n_init=100, max_iter=5000, random_state=124).fit_predict(X)
    print(cluster_labels)
    
    # Check if the clustering is good or not by calculating the silhoutte score
    silhouette_val = silhouette_score(buyer_df_for_clustering, cluster_labels)
    print("For n_clusters =", best_k,
          "The best silhouette_score is :", silhouette_val)
    
    return cluster_labels

# Read purchase data
purchase_df=read_data("Purchases.xlsx")

# Remove unused columns
purchase_df=remove_columns(purchase_df, ['Item ID', 'Auction ID', 'bid_count'])

# Removing null values with no bidder
purchase_df=purchase_df.dropna()
purchase_df = purchase_df[(purchase_df['Price Sold'] != 0.0) & (purchase_df['high_bidder'] != 0.0)]

# Read buyer data
buyer_df=read_data("Buyer Profile - Assignment.xlsx")

# Extract number of purchase for each buyer
bid_count_by_buyer=purchase_df['high_bidder'].value_counts().to_dict()

# Removing null values with no information
buyer_df=buyer_df.dropna()

# Add a new column to buyer dataframe indicating the number of purchase made by the buyer
buyer_df['Frequency']=buyer_df['Buyer ID'].apply(lambda buyer_id: bid_count_by_buyer[int(buyer_id)])

# List total spent groupped by bidder id
purchase_by_bidder=dict(purchase_df.groupby(['high_bidder'])['Price Sold'].sum().reset_index().values)

# Add a new column to buyer dataframe indicating the total purchase amount by the buyer
buyer_df['Monetary']=buyer_df['Buyer ID'].apply(lambda buyer_id: purchase_by_bidder[int(buyer_id)])

# Find each buyer's latest transaction
latest_purchase_by_bidder=dict(purchase_df.groupby(['high_bidder'])['Auction Close Date'].max().reset_index().values)

# Add a new column to buyer dataframe indicating the recency of the buyer
buyer_df['Recency_days']=buyer_df['Buyer ID'].apply(lambda buyer_id: datetime.strptime('2021-09-01 00:00:01', '%Y-%m-%d %H:%M:%S')-latest_purchase_by_bidder[int(buyer_id)])
buyer_df['Recency']=buyer_df['Recency_days'].apply(lambda days: int(round(days.total_seconds() / 60)))
buyer_df=remove_columns(buyer_df, ['Recency_days'])

# Perform unsupervised clustering on buyer (0=high value, 2=low value)
buyer_df['cluster_value']=unsupervised_clustering(buyer_df[['Recency','Frequency','Monetary']])

# Filter out buyers with cluser_value 0 (meaning high value buyers)
high_value_buyer_df=buyer_df.query('cluster_value == 0')

# Read country and state mapping data
state_df=read_data("State Mapping.xlsx")
country_df=read_data("Country Mapping.xlsx")

# Get Country and State name from the mapping data
high_value_buyer_df['Country'] = high_value_buyer_df['country_id'].map(country_df.set_index('Id')['Country'])
high_value_buyer_df['State'] = high_value_buyer_df['state'].map(state_df.set_index('Id')['State'])
high_value_buyer_df=remove_columns(high_value_buyer_df, ['state', 'country_id'])

# Save the high value buyers' information
high_value_buyer_df.to_csv("../Results/high_value_buyers.csv", index=False)