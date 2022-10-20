# Auction Website Backend API
This API is made primarily using Flask and with the help of datetime module. 

### Overview
Since setting up a User Interface is unnecessary, the given API currently recieves input and produces a pretty-printed output, both in JSON format. Further, the API does not have any form of security or authorisation of the users. The API follows all the rules of the auction.
The API takes into account two kinds of Users: Buyers and Sellers.
- Sellers are able to:
  - **Sign in as a unique seller**: Since authorisation of sellers' identity was unnecessary, the current API just differentiates different sellers by assigning a unique seller_id for each seller, and is present in the URL, in order to provide personalised output. 
  - **Create auctions of one product per auction**: This is done by the create_auction() function.
  - **Set auction start timings and minimum bid price**: This can also be done by the create_auction() function which accepts a POST request containing the required details, again, in JSON format.
  - **Revoke an auction**: This is done by the delete_auction() function. It takes in the argument of seller_id and prod_id (Seller ID and Product ID respectively), both of which is provided in the URL itself.
  - **Check status of live auctions**: This is done using the show_live_auctions() function. It filters and shows only those auctions that are conducted by that particular seller.
  - **View their auction history**: The show_past_auctions() functions does this task. It also works in a similar fashion to how show_live_auctions() function work.
  - **End a live auction**: Since the seller must have the option to be able to close the auction any time one wants, the end_auction() function was created. This functions accepts the Product ID in a POST request.

- Buyers are able to:
  - **View all auctions**: Further, the user may choose to apply a filter on the Product name and the date of the auction.
  - **Place a bid**: The bidding system checks that the bid being placed is valid by verifying that the bidder is not already the highest bidder, and that the bid amount is greater than at least 2% of the previous highest bid. Further, in order to prevent bidding in last seconds, if a new valid bid is received less than 5 minutes from the end of auction, then the auction end time is extended for 10 more minutes. This can be extended by a maximum of 100 times.
  - **View history of auctions where the buyer has been the highest bidder**: This is done by the previous_bids() function


### Setting Up
It is advised to create a virtual environment before installing the modules required to run the API. This can be done by
```
pipenv shell
```

Next, the following lines of code are to be executed in CMD:
```
pipenv install Flask
```

