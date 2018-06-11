How to get started:

Dependencies:

* PyCrypto >= 2.6.1
* Requests >= 2.11.0


1. Download our sample client from https://github.com/Fairlay.
2. Create your Private RSA Key. The sample clients allow you to generate one.
3. Retrieve your Public RSA Key and use it to create a new API Account on https://www.fairlay.com/account/. You will also learn your UserID
4. Provide details like your User ID, API Account ID, Private Key and the Server you like to connect to. You find a sample config file in the repository.



Please note the following rules regarding the order matching: 
 
1. When two open orders are matched, a Matched Order is created in the PENDING state.  
2. If the maker of the bet cancels his bet within a certain time period the bet goes into the state MAKERVOIDED and is void.  The said time period is defined in each unmatched order  and matched order as "makerCancelTime" or "makerCT". The maximum allowed time is also given for each runner (which is usually 0, 3000 or 6000 milliseconds).
3. Every time the maker of a bet exerts his right to (maker)void a bet, a fee is deducted from his account. This fee is currently 300 requests or 0.003mBTC but will be increased if needed. 
4. When a market is settled the orders go to one of the settled states VOID, WON, HALFWON, LOST or HALFLOST.  
5. Decimal market go into the state DECIMALRESULT while the settlement value DecResult will be set.
6. Regarding Binary Markets, please note that if you place a lay (bid , 0) bet with stake 100 and odds 2.50 your liability will be 150mBTC. This is different to the Fairlay website, where the stake is always the liablity.



The public key of the server is:

-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC52cTT4XaVIUsmzfDJBP/ZbneO
6qHWFb01oTBYx95+RXwUdQlOAlAg0Gu+Nr8iLqLVbam0GE2OKfrcrSy0mYUCt2Lv
hNMvQqhOUGlnfHSvhJBkZf5mivI7k0VrhQHs1ti8onFkeeOcUmI22d/Tys6aB20N
u6QedpWbubTrtX53KQIDAQAB
-----END PUBLIC KEY-----

or in XML format:


<RSAKeyValue><Modulus>udnE0+F2lSFLJs3wyQT/2W53juqh1hW9NaEwWMfefkV8FHUJTgJQINBrvja/Ii6i1W2ptBhNjin63K0stJmFArdi74TTL0KoTlBpZ3x0r4SQZGX+ZoryO5NFa4UB7NbYvKJxZHnjnFJiNtnf08rOmgdtDbukHnaVm7m067V+dyk=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>
