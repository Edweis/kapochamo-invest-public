# Context
- Goal : Bet on the right crypto currency at the right time.
- Asset : React when a news is published, as of now they all come from [binance website](https://binance.zendesk.com/hc/en-us).
- [Current challenges](#challenges) : Create excellent extractors

## Architecture
We fetch the news every minute on Binance. If the news is new, we extract all of its information (time, title, content), then run an **extractor** to find on which symbol to bet on.

Then, for each of these symbols (like [BTCUSDT](https://www.binance.com/en/trade/BTC_USDT)), we buy a certain amount of the base asset, like 500$ of BTC (~0.057 BTC). 

We then listen to the price change, once a **strategy** asserts that it is the right moment to sell, we sell.

Here is a sequence diagram of the process : 
![Kapochamo Invest Diagram](https://raw.githubusercontent.com/Edweis/kapochamo-invest-public/master/uml.png)

## Terminology
 - **news** : data constructed of:
   - `url` is the unique identifier of the news
   - `time` in UTC format representing the _creation time_ of the news. Note than the _publishing time_ is usually ~5minutes after that, but lets use only this time for now.
   - `title`
   - `content` the body of the news (raw text)
 - **symbol** : tradable quote asset against a base asset. For instance `BTCUSDT` is a symbol representing the evolution of `BTC` expressed `USDT`. We then call `BTC` the **base asset** and USDT the **quote asset**. You can find all symbols [here](https://www.binance.com/en/markets). 
 - **extractor** : function that analyze a piece of news and extract all the relevant symbols that should be traded. For instance, the extractor `onlyBnb` will take any news and return `BNBUSDT`.
 ```javascript
 type Extractor = (news: News) => Array<Symbol>
 ```
 - **strategy** : function that listens to asset variation, if the strategy decides it is the right moment to sell `shouldSell` return `true`. For instance, a simple strategy could be `WaitFor(5)` that wait for 5 min before selling.
 ```javascript
 type Strategy  = {
  name: string;
  init: (time: Date, baseAssetPrice: number) => void;
  shouldSell : (time: Date, baseAssetPrice: number) => boolean;
 }
 ```
 
# Challenges
## Create excellent extractors
Today we have relatively good strategies that sell on the right time. They are highly configurable so it is easy to progress.
However, extractors should be business-specific. Current ones are agnostic of the information contained in the news, here how they work : 
 - **relatedAgainstUsdt** : find the assets (like ETH, USDT, BTC...) present in the news title and content and return the symbol quoted one USDT.
 - **relatedAgainstBnb** : same as `relatedAgainstUsdt` but against quoted BNB.
 - **onlyBnb** : return `BNBUSDT` whatever the news is.

It needs to be smarter and consider business logic such as listing, delisting, launches, outstanding trades...

## Available data
To do so, I have prepared 12k+ computed performances of 200 news from Binance.
You can find in this repository : 
 - [news.csv]() with `time`, `title`, `url`, `content`
 - [performances.csv]() that if the cross product of 12 strategies and 3 extractors with its performance. Note that an extractor can yield several symbols, hence one strategy run with one extractor can return several performances.
 
 For instance the following lines says that if we ran the strategy `highest` with the extractor `onlyBnb` would have make a return on investment of 6.27%, **trading fee included**.
| url         | strategy | symbol  | performance         | extractor |
|-------------|----------|---------|--------------------|----------|
| [https://...](https://binance.zendesk.com/hc/en-us/articles/360041795572-Introducing-the-Cartesi-CTSI-Token-Sale-on-Binance-Launchpad) | highest  | BNBUSDT | 6.273632581267119  | onlyBnb  |

Note than even a return of 0.5% is meaningful. If it is ran on 10 news in a span of a few days, total return would be roughly 5% !

## Strategies
 - waitFor15 : wait for a set amount of minute, here 15 minutes.
 - highest : theoretical best performances, if we sell at the perfect time. Can't happen in reality.
 - follower1 : sell when the the asset went down by a certain perentage (here 1%) compare to its highest peak.
 - relativeFollower_L5_S3 : sell when we lost 3% of our gain, or if we lost 5% (called pure loss appetite).
 - charly_S10W15L5 : combinaision of `waitFor15` and `relativeFollower_L5_S10`, we wait and then do a relative follower.
 
# Contribute
## Why ?
If this works as expected, we can earn a few per cent on every news on any website. Theoretically, we can earn 0.35% per news _without any fancy algorithm_. With 5 news per week, 4 weeks per month, that is roughly a **7% return per month**.
Contribute and get early access to this **cryptocurrency investment fund** without any fee. It is currently running 💸.

## How ?
Get the [performance.csv]() file and find an excellent extractor.
You can start by filtering with _only strategy=highest_ and _extractor not equal to relatedAgainstBnb_.

## Contact me
Feel free to contact me at kapochamo[at]gmail.com
