from boa.code.builtins import concat

class ad():
    """
    Object for getting storage keys for ad
    """

    # Initialize keys
    ad_id = None
    creator_key = None
    title_key = None
    description_key = None
    price_per_person_key = None
    expiration_key = None
    
    purchased_count_key = None


def get_Ad_storage_keys(ad_id) -> ad:
    ad = ad()

    creator_key = concat(ad_id, 'creator')
    title_key = concat(ad_id, 'title')
    description_key = concat(ad_id, 'description')
    price_per_person_key = concat(ad_id, 'price_per_person')
    expiration_key = concat(ad_id, 'expiration')
    

    ad.creator_key = creator_key
    ad.title_key = title_key
    ad.description_key = description_key
    ad.price_per_person_key = price_per_person_key
    ad.expiration_key = expiration_key
    

    return ad