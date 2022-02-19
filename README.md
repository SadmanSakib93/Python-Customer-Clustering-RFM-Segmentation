# Customer segmentation using K-means clustering and RFM analysis in Python

- Using the given dataset, please answer the three questions relating the purchasing habits of customers/buyers.

## Data Sources:
There are three main tables in this data source. The data tables are extracted by using SQL quries and stored in Excel spreadsheets.
- Purchases: This table consists of all the Items sold in auctions
  ![image](https://user-images.githubusercontent.com/27827295/154782102-4de7c5fd-8d17-4ce6-8558-a5f0cb8e1f6f.png)
  
- Buyer Profile - Assignment: This table consists of information related to the buyers/customers
  ![image](https://user-images.githubusercontent.com/27827295/154782146-ea3e0594-52fe-4224-93f7-f91862d149c3.png)

- State Mapping: This table is for mapping the state ID to a given state/province
  ![image](https://user-images.githubusercontent.com/27827295/154782167-9b31f358-761b-45ee-a716-ae4adeae5e8c.png)

- Country Mapping: This table can be used to map the country ID to a given country
  ![image](https://user-images.githubusercontent.com/27827295/154782214-7658518a-ff34-43bb-af17-9ae06bb4d55f.png)
  
## Questions/Tasks:
1) Find the buyers who are in the top 5 percentile?
2) Conduct a cohort analysis of the customers to understand how much each customer cohort contributes to auctions and which cohort contributes the most.
3) Identify the sources from where our HIGH VALUE buyers are coming (geographically and by source) for the auctions that closed within a specific date range (i.e., July and August 2021)

The python programs to solve the aforementioned analytics problems can be found in the Code folder. The task/question 3 is solved using Unsupervised K-Mean clustering and RFM analysis of the customer data.
