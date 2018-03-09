<p align="center">
    <img src="logo.png" width="150px">
</p>

<h1 align="center">adX</h1>

<p align="center">
    NEO smart contract for adX platform
</p>

## Overview

adX is a novel tool for vendors (cafes, restaurants, stores, etc) to engage people in collecting ads and coupons. adX is a geolocation based Augmented Reality mobile application on NEO. Vendors post their ads and how much NEO they want to share with users. Users have to go to specific location on map, open the app and click on the floating in augmented reality advertisement. 

Smart contracts are implemented for sharing the tokens with the adX users based fist come first serve.  First user will get 50% of vendors amount, second - 25%, third - 12.5% and so on.

- [Background](#background)
- [Script Hash](#script-hash)
- [Scope](#Scope)
- [Usage](#usage)
- [Documentation](#documentation)
- [Deploy](#deploy)
- [License](#license)
- [Investors](#investors)
- [Future](#future)

## adX consists of 3 parts:

- ### adX Web App:

  <img src="UI.png">

- ### Android app with Augmented Reality, Mapbox and Firebase:

  ​

  ### <img src="android_ui.png">

- ### NEO blockchain:

  <img src="diagramofsmartcontract.png">

  ​

## Background

The primary purpose of adX is to deliver a fun and secure way of collecting ads and distributing money to the winners. Despite the technological progress, advertisements stayed annoying and bothering users. With adX they became fun and engaging. 

#### The problem

In the past years with the growth of the data collection and machine learning, companies have done tremendous work in creating personalized advertisements. However, they are still annoying sitting on the pages of users favorite websites. People simply use Ad Blockers to protect themselves from the annoying personalized pop ups. 

#### The solution

With the sudden popularity of Pokemon Go. @aarora08 and @denisolt have realised that same engaging technology can be applied in the field of advertising as well. adX let's you collect coupons and ads just like pokemon Go. However, you also get paid! Using NEO Blockchain adX distributes the tokens to the users that collected the Ad, making ads fun for the first time!

## Script Hash

City of Zion testnet:

```
N/A : Error Occured
```

## Scope

#### Smart Contract

The Smart Contract will provide a trustless bridge between users and vendors, using blockchain technology built on the NEO Smart Economy to ensure that vendors can not scam the users and vendors ads and coupon stay as digital assets.

- Use a NEO public address as a digital identity
- User authorization
- Registration of users on the network
- Withdrawals of NeoGas during the acceptance of the ad

#### User

The user will be provided with an account with built-in crypto currency wallet. The wallet will hold NeoGas that the user has collected so far

- Web-based Python client
- Android App
- Open-source
- More in https://github.com/adX-agency/adx

#### Vendor

The vendor will have access to set of tools and knowledge to put up their ad on the blockchain.

- NeoGas Wallet with their digital assets (images of ads and coupons) and the amount of NeoGas they have left
- Web application
- Open-source
- More in https://github.com/adX-agency/adX-backend

#### Service

The ecosystem is friendly and engaging. With an Augmented Reality application users will not even think of annoying ads, while they are getting paid in the most fun scavenger hunt they have had so far. Simultaneously, vendors are capable of distributing their ads anywhere in the World for a lot cheaper!

Detailed usage explanation is described in [Documentation](#documentation).

## Usage

There are two types of users: vendors and customers. Vendors are the ones setting up the advertisements and coupons. Customers are the ones discovering them and getting rewarded. Function parameters and examples are explained below in [Documentation](#documentation).

### Seller Functions

* [`create`](#create) - create the ad
* [`delete`](#delete) - delete the ad

### Discover Functions

* [`discover`](#discover) - get rewarded for ad / save it

### Misc Functions

* [`details`](#details) - get all details of the ad

## Documentation

**Attention: functions cannot have spacing if started from neo-python. **

### `register_ad`

* Example:

    > `testinvoke <scripthash> create ['senderhash','ad_id','ad_description','lat_lng', 'ad_exp', 'ad_views', 'ad_sell', 'ad_price']`

* Arguments (in order):

    * **`scripthash`**: The public hash of the smart contract on the NEO blockchain

    * **`user_hash`**: (hash address of the user)

        Owner of the ad's wallet hash (vendor). This hash is used to transfer NeoGas to the users.

    * **`ad_id`**: (str)

        Unique String. Can be timestamp, lat, long.

        **`ad_description`**: (str)

        Description and details of your ads.

    * **`lat_lng`**: (str)

        Location of your ads.

    * **`ad_exp`**: (str)

        Date the ad expires, expressed in unix GMT time. 

    * **`ad_views`**: (int)

        Number of views of the ad.

    * **`ad_sell`**: (int)

        The price of the ad. 

    * **`ad_price`**: (int)

        How much NeoGas is being distributed to the user when he saves the ad. 


### `register_user`

- Example:

  > `testinvoke <scripthash> create ['user_hash','userid','user_id','user_name', 'user_gas', 'user_views']`

- Arguments (in order):

  - **`scripthash`**: The public hash of the smart contract on the NEO blockchain

  - **`user_hash`**:  (hash address of the user)

    Owner of the ad's wallet hash (vendor). This hash is used to transfer NeoGas to the users.

  - **`userid`**: (int)

    int. Can be timestamp, lat, long.

    **`user_id`**: (str)

    ID created out of userID and user_hash

  - **`user_name`**: (str)

    Name of the user.

  - **`user_gas`**: (str)

    Amount of NeoGas user has in the beginning. 

  - **`user_views`**: (int)

    Total number of views accumulated from the ads of the user.

### `update_views`

- Example:

  > `testinvoke <scripthash> create ['ad_id','ad_views']`

- Arguments (in order):

  - **`scripthash`**: The public hash of the smart contract on the NEO blockchain

  - **`ad_id`**: (hash of the ad)

    A hash of the advertisement, since it is a digital asset.

  - **`ad_views`**: (int)

    Total number of views accumulated from the ad.

### `update_gas`

- Example:

  > `testinvoke <scripthash> create ['ad_id','ad_gas_amount']`

- Arguments (in order):

  - **`scripthash`**: The public hash of the smart contract on the NEO blockchain

  - **`ad_id`**: (hash of the ad)

    A hash of the advertisement, since it is a digital asset.

  - **`ad_gas_amount`**: (double)

    Amount of the desirable NeoGas to be changed.

### `give_user_gas`

- Example:

  > `testinvoke <scripthash> create ['ad_id', 'reciever_id', 'reciever_ad_count']`

- Arguments (in order):

  - **`scripthash`**: The public hash of the smart contract on the NEO blockchain

  - **`ad_id`**: (hash of the ad)

    A hash of the advertisement, since it is a digital asset.

  - **`reciever_id`**: (hash address of the user)

    Wallet hash of the regular user. This hash is used to transfer NeoGas from the vendor.

  - **`recivever_ad_count`**: (int)

    The position of the receiver, if he is first he gets 50%, second 25% and so on.

### `getAdInfo`

- Example:

  > `testinvoke <scripthash> create ['ad_id']`

- Arguments (in order):

  - **`scripthash`**: The public hash of the smart contract on the NEO blockchain

  - **`ad_id`**: (hash of the ad)

    A hash of the advertisement, its location in the database



## Deploy

To launch the web side of AdX:

```bash
git clone https://github.com/adX-agency/adX-backend.git
cd adX-backend
cd mysite
python3 manage.py runserver
```

To access the android app:

```bash
git clone https://github.com/adX-agency/adX.git
# open Android Studio and build an apk
# install the apk on your Android device#
```

neo-python commands to 

```
build coreadx.py test 0710 01 True False operation []
import contract contract.avm 0710 01 True False
```

## License

- adX is open-source under [MIT license](https://github.com/adX-agency/adx-blockchain/blob/master/LICENSE)
- Maintained by [Arshit Arora](http://github.com/aarora08),  [Denisolt Shakhbulatov](http://github.com/denisolt),  [Mahmoud Saleh](http://github.com/msdocs)



## Investors

Few advertisements firms already got a sneak peak of adX and they loved it. 

Pioneers of the ad business have given feedback stating that adX can revolutionize their business and bring in a lot more users.

Especially taking in consideration the development of Augmented Reality on the smaller wearable devices. 

## Future

- Implementation of Deep Learning techniques to replace the images of actual billboards in the streets with our elements. 
- Implementation of other functions in the smart contracts:
  - to ensure the coupon can be used once
  - to transfer coupons/ads to other people
  - to setup custom percentage of split to users
