# Context
- Goal : bet on the right crypto currency at the right time.
- Asset : react when a news is published, as of now they all come from [binance website](https://binance.zendesk.com/hc/en-us).

## Architecture
We fetch the news every minute on binance. If the news is new, we extract all of its information (time, title, content), then run an **extractor** to find on which symbol to bet on.

Then, for each of these symbols (like [BTCUSDT](https://www.binance.com/en/trade/BTC_USDT)), we buy a certain amount of the base asset, like 500$ of BTC (~0.057 BTC). 

We then listen to the price change (through a WebSocket), once a **strategy** asserts that it is the right moment to sell, we sell.

Here is a sequence diagram of the process : 
![Kapochamo Invest Diagram](https://www.plantuml.com/plantuml/img/bLJ1Rjim3BthAuYU6Y19xy6mTLs7eXYm5ck07WjPOX8XiXH8L5n_s_vXtpHATjtOImypOC0Y7_d8zmHVHvA1Kcq56R88F-J1gvsi_UBU7J4Io4I-beGQA4Xjt1PaK3j3g2W5549vHy5R-6PzqeqajGCPGJK27NTiuU8vnp30dzyNETDqHr7vvBGC3BWnJZg5uB291L9rWPSSEC7zv2FStXH8JhteQY1Pyspl75HEPoY-FjwF6EJ1226izmV08pAoDYuH2k17DR3u_3RkYgjQfy2uez_ZvQmW-bo6dOwyWhllQwXbs2DTIMj7s4-BnGHiMLpMkImxwTflkO9RZztEWA-6mLyAKjgk34m4oNOmLvi39JbfDUo1hwoE8eXjNNaROHDy_Kx-qG36HGmzssMvANF8phF-SqZ1pc6vNCw65fsYakz2HpCa9lqxeoRYTYMpKKrfcDXi2v6B2BSj7AKrEei73x-0J8q-4Q-d43NgKNL-EggH_kp-2fwnUlAAhO8jltjh7CQFYa-CBhMF3qzhg5BRRzbfkJ617IAZzl-qOOqQQMYw2Dltjejco7-nHxJsdCZeT15Dd0sWZGWRQMml52V50BZch_n3-0i0)

## Terminology
 - **news** : data constructed of:
   - `url` is the unique identifier of the news
   - `time` in UTC format representing the _creation time_ of the news. Note than the _publishing time_ is usually ~5minutes after that, but lets use only this time for now.
   - `title`
   - `content` the body of the news (raw text)
 - **symbol** : tradable quote asset against a base asset. For instance `BTCUSDT` is a symbol representing the evolution of `BTC` expressed `USDT`. We then call `BTC` the **base asset** and USDT the **quote asset**. You can find all symbols [here](https://www.binance.com/en/markets). 
 - **extractor** : function that analyze a news and extract all the relevant symbols that should be traded. For instance the extractor `onlyBnb` will take any news and return `BNBUSDT`.
 ```javascript
 type Extractor = (news: News) => Array<Symbol>
 ```
 - **strategy** : function that listens to asset variation, if the strategy decides it is the right moment to sell `shouldSell` return `true`. For instance a simple strategy could be `WaitFor(5)` that wait for 5 min before selling.
 ```javascript
 type Strategy  = {
  name: string;
  init: (time: Date, baseAssetPrice: number) => void;
  shouldSell : (time: Date, baseAssetPrice: number) => boolean;
 }
 ```
 
# Challenges
 - Find excellent extractors
 - Find excellent strategies