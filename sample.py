import datetime
import threading
import time
from client import FairlayPythonClient


class SampleFairlayMonitoring(object):
    markets = []
    matched_orders = []
    last_markets_fetch_date = datetime.datetime(2016, 01, 01)
    last_orders_fetch_date = datetime.datetime(2016, 01, 01)

    created_order = {'id': None, 'market': None, 'odds': None}
    should_create = True

    def __init__(self):
        super(SampleFairlayMonitoring, self).__init__()
        self.client = FairlayPythonClient()
        self.event = threading.Event()

        threading.Thread(target=self.__update_markets).start()
        threading.Thread(target=self.__update_orders).start()

    def __update_markets(self):
        while not self.event.is_set():
            print 'Fetching markets and odds'
            self.fetch_markets()
            self.last_markets_fetch_date = datetime.datetime.now()
            self.check_order()
            self.event.wait(30)

    def __update_orders(self):
        while not self.event.is_set():
            print 'Fetching matched orders'
            self.fetch_matched_orders()
            self.last_orders_fetch_date = datetime.datetime.now()
            self.event.wait(60)

    def stop(self):
        self.event.set()
        self.cancel_order()

    def check_order(self):
        found = False

        for m in self.markets:
            if self.created_order['market']:
                
                if self.created_order['market'] == m['ID'] and self.should_create and not found:
                    found = True
                else:
                    continue

                if m['OrdBJSON'] and m['OrdBJSON'][0]['Bids']:
                    price = m['OrdBJSON'][0]['Bids'][0][0]

                    if self.created_order['odds'] < price:    
                        print 'Orderbook has changed, updating order Odds={}'.format(price + 0.001)
                        if self.create_order(self.created_order['id'], self.created_order['market'], price + 0.001):
                            break
                    else:
                        print 'Orderbook hasn\'t changed'
                else:
                    print 'Orderbook has gone, canceling order'
                    self.cancel_order()
            else:
                if m['OrdBJSON'] and m['OrdBJSON'][0]['Bids']:
                    price = m['OrdBJSON'][0]['Bids'][0][0]
                    print 'Creating new order Odds={} Market={}'.format(price + 0.001, m['ID'])
                    if self.create_order(-1, m['ID'], price + 0.001):
                        found = True
                        break

        if self.created_order['market'] and not found:
            print 'Market not found, canceling order'
            self.cancel_order()
            
    def cancel_order(self):
        if self.created_order['market']:
            order = {
                'Mid': self.created_order['market'],
                'Rid': 0,
                'Oid': self.created_order['id'],
                'Am': 10,
                'Pri': 0,
                'Sub': '',
                'Type': 0,
                'Boa': 0,
                'Mct': 0
            }

            order = self.client.change_orders([order])[0]
            if order:
                self.created_order = {'id': None, 'market': None, 'odds': None}
                return True

    def create_order(self, idd, market, price):
        if not self.created_order['market']:
            order = {
                'Mid': market,
                'Rid': 0,
                'Oid': idd,
                'Am': 10,
                'Pri': price,
                'Sub': '',
                'Type': 0,
                'Boa': 0,
                'Mct': 0
            }

            order = self.client.change_orders([order])[0]
            if order:
                self.created_order = {'id': order['PrivID'], 'market': market, 'odds': price}
                return True

    def fetch_markets(self):
        from_id = 0
        increment = 100

        new_markets = []
        while True:
            filters = {'Comp': 'England - Premier League', 'FromID': from_id, 'ToID': from_id + increment, 'NoZombie': True}
            new_markets += self.client.get_markets_and_odds(filters, self.last_markets_fetch_date)

            if len(new_markets) < increment or len(new_markets) == 100:
                break
            else:
                from_id += increment
            time.sleep(2)

        now = datetime.datetime.now() - datetime.timedelta(minutes=30)
        for idx, market in enumerate(self.markets):
            closing_date = datetime.datetime.strptime(market['ClosD'][:19], '%Y-%m-%dT%H:%M:%S')
            if closing_date < now:
                del self.markets[idx]

        self.markets += new_markets

    def fetch_matched_orders(self):
        ts = long((self.last_orders_fetch_date.replace(tzinfo=None) - datetime.datetime(1, 1, 1)).total_seconds() * 10000000)
        temp = self.client.get_orders('matched', ts)
        if temp:
            self.matched_orders += temp
        
        if self.possible_losings() > 100:
            print 'Possible losings > 100, disable order creation and cancel existing order'
            self.should_create = False
            self.cancel_order()


    def possible_losings(self):
        losings = 0

        if not self.created_order['market']:
            return 0

        for order in self.matched_orders:
            m_id = order['_UserOrder']['MarketID']
            r_id = order['_UserOrder']['RunnerID']
            is_back = order['_UserOrder']['BidOrAsk'] == 1
            amount = order['_MatchedOrder']['Amount'] / 1000.0
            odds = order['_MatchedOrder']['Price']
            
            if m_id != self.created_order['market']:
                continue
            
            if is_back:
                losings += amount
            else:
                losings += (amount * (1 + (1 / (odds - 1)))) - amount

        return losings

sample = SampleFairlayMonitoring()
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sample.stop()
        break
   
