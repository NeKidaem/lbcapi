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


Disclaim of Warranties and limitations of liability
============
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
