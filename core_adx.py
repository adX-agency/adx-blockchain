from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.Blockchain import GetHeight, GetHeader
from boa.blockchain.vm.Neo.Runtime import Log, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Storage import Get, GetContext, Put, Delete
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.System.ExecutionEngine import GetCallingScriptHash
from boa.code.builtins import concat

from txio import get_asset_attachments
from Ad import get_Ad_storage_keys


OWNER = b'\x01\xc0\x68\xab\x9c\x67\x57\x91\x12\xb9\xe4\x9f\xcb\x38\xf9\xc1\x02\x94\xaa\xdb\x40\x72\x60\x59\xb4\x60'

OnTransfer = RegisterAction('transfer', 'Addr_from', 'Addr_to', 'amount')
OnRefund = RegisterAction('refund', 'Addr_to', 'amount')
OnClaim = RegisterAction('claim', 'Addr_to', 'amount')


def Main(operation, args):
    trigger = GetTrigger()

    if trigger == Verification():
        is_owner = CheckWitness(OWNER)
        if is_owner:
            return True
        return False

    elif trigger == Application():
        # seller action
        if operation == 'create':
            if len(args) == 8:
                creator = args[0]  # public key
                coupon_id = args[1]
                title = args[2]
                description = args[3]
                price = args[4]  # price in GAS
                expiration = args[5]
                
                success = CreateAd(creator, coupon_id, title, description, price, expiration, )

                if success:
                    Log('Ad created successfully')
                    return True
                else:
                    Log('Error in creating Ad')
                    return False
            else:
                Log('incorrect number of arguments')
                return False

        
        

      
        # vendor action
        elif operation == 'details':
            if len(args) == 1:
                coupon_id = args[0]
                Details(coupon_id)
                return True
            else:
                Log('incorrect number of arguments')
                return False

        else:
            Log('operation not found')
            return False

    return False
@staticmethod
def now():
    height = GetHeight()
    current_block = GetHeader(height)
    current_time = current_block.Timestamp
    return current_time

def CreateAd(creator, coupon_id, title, description, price, expiration ):
    """
    Create an Ad and "register" the details onto the blockchain/storage.

    Args:
        creator (str): public key
        coupon_id (str): Ad unique id
        title (str): can not contain spaces
        description (str): can not contain spaces
        price (int): floats not supported in VM, price in GAS
        expiration (int): use unix GMT time
          (int): minimum number of tickets to be sold
           (int): maximum number of tickets that can be sold

    Returns:
        (bool): True if Ad created successfully
    """

    #
    # Checks for if args are valid and create conditions are met
    #

    if price < 0:
        Log('price must be positive')
        return False

    
    current_time = now()

    if current_time > expiration:
        Log('expiration must be greater than current time. '
            'Note: use unix GMT time')
        return False

    Ad_exists = IsAdExist(coupon_id)
    if Ad_exists:
        Log('coupon_id is alreAdy taken')
        return False

    #
    # Create Ad
    #

    Ad = get_Ad_storage_keys(coupon_id)

    context = GetContext()
    Put(context, coupon_id, True)  # Ad_exists
    Put(context, Ad.creator_key, creator)
    Put(context, Ad.title_key, title)
    Put(context, Ad.description_key, description)
    Put(context, Ad.price_key, price)
    Put(context, Ad.expiration_key, expiration)

    return True



def DeleteAd(coupon_id):
    """
    Delete Ad identified by coupon_id

    Args:
        coupon_id (str): Ad unique id

    Returns:
        (bool): True if Ad deleted successfully
    """

    expired = IsAdExpired(coupon_id)
    if expired:
        Log('Ad has alreAdy finished, can no longer delete it!')
        return False

    context = GetContext()
    Delete(context, coupon_id)  # delete Ad_exists

    return True


def ClaimFunds(coupon_id):
    """
    USER of Ad can claim funds from coupon_id if the   and
    expiration conditions are met. Funds can only be claimed if wallet's public
    key used to invoke matches the public key used in create.

    NOT IMPLEMENTED YET

    Args:
        coupon_id (str): Ad unique id

    Returns:
        (bool): True if Ad claimed successfully
    """

    #
    # Checks for if args are valid and claim conditions are met
    #

    Ad_exists = IsAdExist(coupon_id)
    if not Ad_exists:
        Log('Ad not found')
        return False

    expired = IsAdExpired(coupon_id)
    if not expired:
        Log('Ad not over yet! Cannot claim funds yet')
        return False

    Ad = get_Ad_storage_keys(coupon_id)

    context = GetContext()

    

    #
    # Claim funds
    #

    price = Get(context, Ad.price_key)

    # Funds get split by two after every single claim
    price = price / 2 
    Put(context, Ad.price_key, price)
    funds_amount =  price/2
    claim_Address = GetCallingScriptHash()
    OnClaim(claim_Address, funds_amount)

    return True




def Details(coupon_id):
    """
    Prints details of specified Ad:
    Creator, Title, Description, Price/person, Expiration date, Min count,
    Max count, Purchased count

    Args:
        coupon_id (str): Ad unique id

    Returns:
        (bool): True if Ad found and details successfully printed
    """
    
    Ad_exists = IsAdExist(coupon_id)
    if not Ad_exists:
        Log('Ad not found')
        return False

    Ad = get_Ad_storage_keys(coupon_id)

    context = GetContext()
    creator = Get(context, Ad.creator_key)
    title = Get(context, Ad.title_key)
    description = Get(context, Ad.description_key)
    price = Get(context, Ad.price_key)
    expiration = Get(context, Ad.expiration_key)
    
    Log('Creator public key')
    Log(creator)
    Log('Title')
    Log(title)
    Log('Description')
    Log(description)
    Log(price)
    Log('Expiration date')
    Log(expiration)
    

    return True


def IsAdCreator(coupon_id):
    """
    Check if smart contract invoker is creator of Ad

    Args:
        coupon_id (str): Ad unique id

    Returns:
        (bool): True if contract invoker is creator of Ad
    """
    Ad_exists = IsAdExist(coupon_id)
    if not Ad_exists:
        Log('Ad not found')
        return False

    context = GetContext()
    creator_key = concat(coupon_id, 'creator')
    creator = Get(context, creator_key)

    return CheckWitness(creator)


def IsAdExpired(coupon_id):
    """
    Check if Ad has expired or not

    Args:
        coupon_id (str): Ad unique id

    Returns:
        (bool): True if Adtion has expired
    """
    context = GetContext()
    expiration_key = concat(coupon_id, 'expiration')
    expiration = Get(context, expiration_key)
    
    current_time = now()

    expired = current_time > expiration
    return expired


def IsAdExist(coupon_id):
    """
    Check if Ad identified by coupon_id alreAdy exists

    Args:
        coupon_id (str): Ad unique id

    Returns:
        (bool): True if coupon_id alreAdy exists in storage
    """
    context = GetContext()
    Ad_exists = Get(context, coupon_id)
    return Ad_exists
