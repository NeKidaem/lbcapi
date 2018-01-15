lbcapi is a simple python wrapper for the LocalBitcoins API to make it easier to develop applications that interface with LocalBitcoins.com.
LocalBitcoin class encompasses the original library, providing the api methods as methods of the object, trying to facilitate the calls in a more usual way..

To install
==========
Download the repository using git or as zip (extract if necessary), go to the folder and type the following command to install

    pip install -U .

Usage example
============
This example uses the Public library

```
from lbcapi import LocalBitcoin

LBTC = LocalBitcoin()

if 'US' in LBTC.country_codes(): print('Country OK!')

cc = LBTC.country_codes()
pm = LBTC.payment_methods()
```

This example Requires Authentication using HMAC
```
hmac_key = "{Your HMAC key here}"
hmac_secret = "{Your HMAC secret here}"

LBTC = LocalBitcoin(hmac_key, hmac_secret)

cr = LBTC.currencies()

cd = LBTC.closed()

ca = LBTC.canceled()

deposit_fee, outgoing_fee = LBTC.fees()

balance, sendable = LBTC.wallet()

```

To find out all the available API calls please see the API documentation on LocalBitcoins.com
https://localbitcoins.com/api-docs/
