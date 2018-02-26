<p align="center">
    <img src="logo.png" width="150px">
</p>

<h1 align="center">adX</h1>

<p align="center">
    NEO smart contract for adX platform
</p>

## Overview

<img src="UI.png">

adX is a novel tool for vendors (cafes, restaurants, stores, etc) to engage people in collecting ads and coupons. adX is a geolocation based Augmented Reality mobile application on NEO. Vendors post their ads and how much NEO they want to share with users. Users have to go to specific location on map, open the app and click on the floating in augmented reality advertisement. 

Smart contracts are implemented for sharing the tokens with the adX users based fist come first serve.  First user will get 50% of vendors amount, second - 25%, third - 12.5% and so on.

* [Script Hash](#script-hash)
* [Example](#example)
* [Usage](#usage)
* [Documentation](#documentation)
* [Deploy](#deploy)

## Script Hash

City of Zion testnet:

```

```

## Example

Detailed explanation found in [Documentation](#documentation).

adX consists of 3 parts:

- Web app on Django
- Android app with Augmented Reality, Mapbox and Firebase
- NEO blockchain.

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

### `create`

* Example:

    > `testinvoke <contract_hash> create ['<creator_public_key>','McDonaldsAd','Opening-day-Big Mac 30% off!','Discount-for-meal-and-burger-alone',3,1546300800,5,8]`

    Here a new ad identified by `McDonaldsAd` is being created for the BigMac, promo expires on Jan 1, 2019 (1546300800 unix time). A vendor would typically be using this command.

* Parameters (in order):

    * **`creator_public_key`**: (public key)

        Owner of the ad's public key. This public key is checked to determine whether the wallet used to invoke has permission to `delete` or `discover` a promo after it has been created. `creator_public_key` is explicitly stated to give flexibility, eg creating a promo on behalf of the vendor.

    * **`promo_id`**: (str)

        Unique String. Can be timestamp, lat, long.

        **`title`**: (str)

        Title of your ad.

    * **`description`**: (str)

        Description and details of your ads.

    * **`price_per_person`**: (int)

        Price in gas.

    * **`expiration`**: (int)

        Date the ad expires, expressed in unix GMT time. Vendors can only claim funds after the date/time has passed. 


### `discover`

* Example:

    > `testinvoke <contract_hash> claim ['mypromocode']`

    Here a seller can claim funds from promo `McDonaldsAd` if the `min_count` and `expiration` is met. Funds can only be claimed if wallet's public key used to invoke matches the public key used in `create`.

* Parameters:

    * **`promo_id`**: (str)

        Desired ad to save and claim the tokens for.


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
build contract.py test 0710 01 True False operation []
import contract contract.avm 0710 01 True False
```

## Future Work

- Implementation of Deep Learning techniques to replace the images of actual billboards in the streets with our elements. 
- Implementation of other functions in the smart contracts:
  - to ensure the coupon can be used once
  - to transfer coupons/ads to other people
  - to setup custom percentage of split to users