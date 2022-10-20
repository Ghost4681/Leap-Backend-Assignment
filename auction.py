from datetime import datetime as dt, timedelta as td
from flask import Flask, jsonify, request


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gfdtrhd'


#sample dataset
upcoming_auctions = [
    {
        'prod_id' : 1566,
        'seller_id': 1952,
        'product': 'Airpods',
        'start_time': '23:00',
        'start_date' : '23/10/22',
        'start_price': 12000,
    },
    {
        'prod_id' : 1456,
        'seller_id': 1562,
        'product': 'car',
        'start_time': '13:00',
        'start_date' : '13/10/22',
        'start_price': 124000,
    },
    
]

live_auctions = [
    {
        'prod_id' : 1786,
        'product': 'bag',
        'seller_id': 1782,
        'start_time': '23:00',
        'start_date' : '19/10/22',
        'times_delayed' :0,
        'start_price': 500,
        'current_price': 700,
        'highest_bidder_id': 1234
    },
    {
        'prod_id' : 1234,
        'product': 'bottle',
        'seller_id': 1756,
        'start_time': '16:40',
        'start_date' : '20/10/22',
        'times_delayed' : 99,
        'start_price': 400,
        'current_price': 1000,
        'highest_bidder_id': 1274
    },
    
]

past_auctions = [
    {
        'prod_id' : 4524,
        'product': 'Keyboard',
        'seller_id': 1458,
        'start_time': '09:00',
        'start_date' : '10/10/22',
        'times_delayed' : 1,
        'start_price': 2000,
        'sold_price': 4000,
        'highest_bidder_id': 7896,
        'status' : 'paid'
    },
    {
        'prod_id' : 7845,
        'product': 'Mouse',
        'seller_id': 1489,
        'start_time': '19:00',
        'start_date' : '04/10/22',
        'times_delayed' : 2,
        'start_price': 400,
        'sold_price': 1000,
        'highest_bidder_id': 1898,
        'status' : 'unpaid'
    },
]

all_auctions = upcoming_auctions + live_auctions + past_auctions


#SELLER
#_________________________________#

#Since there is no requirement to authorise different sellers, 
# I have decided to simply differentiate different sellers by having separate url's for each sellers

#filter auctions with seller id
def auctions_filtered(seller_id, auction_type):
    filtered_auctions=[]
    for auction in auction_type:
        if auction['seller_id'] == seller_id:
            filtered_auctions.append(auction)
    return filtered_auctions

#sign in
@app.route('/seller/<int:sellerid>')
def sign_in_seller(sellerid):
    return jsonify({'message':'Hey '+str(sellerid)+', you are now signed in!'})

#show upcoming auctions
@app.route('/seller/<int:sellerid>/upcoming_auctions')
def show_upcoming_auctions(sellerid):
    return jsonify({'auctions':auctions_filtered(sellerid , upcoming_auctions)})

#create auction
@app.route('/seller/<int:sellerid>/create_new_auction', methods=["POST"])
def create_auction(sellerid):
    request_data = request.get_json()
    new_auction={}
    new_auction['product'] = request_data['product']
    new_auction['start_time'] = request_data['start_time']
    new_auction['start_date'] = request_data['start_date']
    new_auction['start_price'] = request_data['start_price']
    new_auction['prod_id'] = request_data['prod_id']
    new_auction['seller_id'] = sellerid
    upcoming_auctions.append(new_auction)

    return jsonify({'message': 'Auction Created', 'New Auction': new_auction})

#revoke auction
@app.route('/seller/<int:sellerid>/<int:prodid>/revoke_auction')
def delete_auction(sellerid, prodid):
    for auction in auctions_filtered(sellerid, upcoming_auctions):
        if auction['prod_id'] == prodid:
            upcoming_auctions.remove(auction)
            return jsonify(auctions_filtered(sellerid, upcoming_auctions))
    return jsonify({'message':"There is no such product being auctioned"})

#check status of live auction
@app.route('/seller/<int:sellerid>/show_live_auctions')
def show_live_auctions(sellerid):
    return jsonify({'Live Auctions': auctions_filtered(sellerid, live_auctions)})

#view past auctions
@app.route('/seller/<int:sellerid>/show_past_auctions')
def show_past_auctions(sellerid):
    return jsonify({'Past Auctions': auctions_filtered(sellerid, past_auctions)})

#end live auction
@app.route('/seller/<int:sellerid>/end_auction', methods=["POST"])
def end_auction(sellerid):
    request_data = request.get_json()
    for auction in live_auctions:
        if sellerid == auction['seller_id']:
            if request_data['prod_id'] == auction['prod_id']:
                live_auctions.remove(auction)
                past_auctions.append(auction)
                return jsonify({'message':'Auction ended!','live_auctions':live_auctions,'past_auctions':past_auctions})
    return jsonify({'message':'You do not have any live auctions at present'})
    

#BUYER
#__________________________________#

#Shows all auctions and has the choice to filter
@app.route('/auctions/all', methods=["POST"])
def show_all_auctions():
    try:#if filter is provided
        request_data = request.get_json()
        if 'product' in request_data and 'date' in request_data: 
            filter_prod_date_auctions = [] 
            for auction in all_auctions:
                if auction['product'] == request_data['product'] and auction['start_date'] == request_data['date']: #if both date and name of product are filtered
                    filter_prod_date_auctions.append(auction)
            if filter_prod_date_auctions:
                return jsonify({"Filtered Auctions": filter_prod_auctions})
            return jsonify({'message': 'No Auctions have sold such product on that date'})

        elif 'product' in request_data:
            filter_prod_auctions = []
            for auction in all_auctions:
                if auction['product'] == request_data['product']: #if Only product is given
                    filter_prod_auctions.append(auction)
            if filter_prod_auctions:
                return jsonify({"Filtered Auctions": filter_prod_auctions})
            return jsonify({'message': 'No Auctions have sold such product'})

        elif 'date' in request_data:
            filter_date_auctions = []
            for auction in all_auctions:
                if auction['start_date'] == request_data['date'] :#if only date is given
                    filter_date_auctions.append(auction)
            if filter_date_auctions:
                return jsonify({"Filtered Auctions": filter_date_auctions})
            return jsonify({'message': 'No Auctions have been held on such date'})
        return jsonify({'Live Auctions':live_auctions, 'Upcoming Auctions':upcoming_auctions, 'Past Auctions':past_auctions})

    except: #if no filter is provided
        return jsonify({'Live Auctions':live_auctions, 'Upcoming Auctions':upcoming_auctions, 'Past Auctions':past_auctions})

#BIDDING SYSTEM
#Since there is no requirement to authorise different bidders, 
# I have decided to simply differentiate different bidders by having separate url's for each bidder

#bidder sign in
@app.route('/buyer/<int:buyer_id>')
def sign_in_bidder(buyer_id):
    return jsonify({'message':'Hey '+str(buyer_id)+', you are now signed in!'})

#place bids
@app.route('/buyer/<int:buyer_id>/<int:prodid>', methods=["POST"])
def place_bid(buyer_id, prodid):
    request_data = request.get_json()

    #finding the index of the required dictionary form the list using a simple linear sort
    index = None
    for i in range(len(live_auctions)):
        if live_auctions[i]['prod_id'] == prodid:
            index = i
            break
    if index!=None:
        if live_auctions[index]['highest_bidder_id'] != buyer_id: #checking if the bidder is not already the highest bidder
            if request_data['bid_value'] > 102/100*live_auctions[index]['current_price']: #checking for valid bid amount
                start_date_time = live_auctions[index]['start_date'] + ' ' + live_auctions[index]['start_time']
                sdt = dt.strptime(start_date_time, "%d/%m/%y %H:%M")
                times_delayed = live_auctions[index]['times_delayed']
                end_time = sdt + td(minutes=60) +td(minutes = times_delayed*10)

                if times_delayed<100:
                    #checking if time of bidding is in last five minutes
                    if end_time-dt.now()<td(minutes=5):
                        live_auctions[index]['times_delayed'] +=1
                    #bid placed 
                    if sdt < dt.now() < end_time:
                        live_auctions[index]['current_price'] = request_data['bid_value']
                        live_auctions[index]['highest_bidder_id'] = buyer_id 

                    return jsonify(live_auctions[index])
                
                elif times_delayed==100:
                    #bid placed 
                    if dt.now()<end_time-td(minutes=5):
                        live_auctions[index]['current_price'] = request_data['bid_value']
                        live_auctions[index]['highest_bidder_id'] = buyer_id 
                    else:
                        return jsonify({'message':"There is only five minutes remaining, you cannot bid anymore"})
                return jsonify(live_auctions[index]) 
            return jsonify({'message':'The bid value is too small/ invalid'})
        return jsonify({'message':'You are alerady the highest bidder'})
    return jsonify({'message':'Invalid Product code'})

#view past bids
@app.route('/buyer/<int:buyer_id>/past_bids')
def previous_bids(buyer_id):
    past_bids=[]
    for auction in past_auctions:
        if auction['highest_bidder_id'] == buyer_id:
            past_bids.append(auction)
    return jsonify({'History of Bids':past_bids})


app.run()