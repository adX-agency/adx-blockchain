from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Storage import GetContext, Put, Delete, Get
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness,Notify
from serialize import serialize_array, serialize_var_length_item,deserialize_bytearray
from boa.builtins import list, concat


ctx = GetContext()


def register_ad(senderhash,ad_id,ad_description,lat_lng,ad_exp,ad_views, ad_sell,ad_price):
	

	ad_exists = Get(ctx, ad_id)
	Notify("Ad exists works ")
	ad_data = list(length=8)

	#senderhash
	ad_data[0] = senderhash
	ad_data[1] = ad_id

	#ad description
	ad_data[2] = ad_description

	
	#lat and long
	ad_data[3] = lat_lng

	
	# ad expiration
	ad_data[4] = ad_exp


	# total views
	ad_data[5] = ad_views

	#auto sell
	ad_data[6] = ad_sell

	#price in gas
	ad_data[7] = ad_price

	if not ad_exists:
		Notify("Ad does not exist")
		serialized_ad_data = serialize_array(ad_data)
		Notify("Data Serialized ")
		Put(ctx, ad_id,serialized_ad_data)
		Notify("ad registered")
		Notify (serialized_ad_data)

	else:
		Notify ("Ad Exists")
		return False

def register_user(user_hash,userid,user_id,user_name,user_gas,user_views):
	
	
	

	user_data = list(length=5)
	user_data[0] = user_hash
	user_data[1]= userid
	user_id = concat(user_hash,userid)
	user_exists = Get(ctx, user_id)
	#user name
	user_data[2] = user_name

	#user gas amount
	user_data[3] = user_gas
	# user views 
	user_data[4] = user_views
	
	
	if not user_exists:

		serialized_ad_data = serialize_array(user_data)
		Put(ctx, user_id,serialized_ad_data)
		Notify("user registered")
		return True
	else:
		Notify("user already exists")
		return False



	
def update_views (ad_id,ad_views):

	data = list(length = 8)
	ad_exists = Get(ctx,ad_id) 
	
	if ad_exists:
		ad_exists = deserialize_bytearray(ad_exists)
		ad_exists[5] = ad_views
		data_serialized = serialize_array(ad_exists)
		Delete(ctx, ad_id)
		Put(ctx,ad_id,data_serialized)
		Notify("Updated ad views ")

		return True
	return False

def update_gas (ad_id,ad_gas_amount):

	data = list(length = 8 )
	data = Get(ctx,ad_id)
	data = deserialize_bytearray(Get(ctx,ad_id))
	data[7] = ad_gas_amount
	Delete(ctx, ad_id)
	data_serialized = serialize_array(data)
	Put(ctx,ad_id,data_serialized)
	Notify("Ad gas amount updated to " , ad_gas_amount)
	return True


def give_user_gas(ad_id,reciever_id,reciever_ad_count):

	reciever_info = list(length = 5)
	ad_data = list(length = 8)

	ad_id = args[0]
	reciever_id = args[1]
	reciever_ad_count = args[2]
	if reciever_ad_count< 1:
		return 'User did not view any ads'

		ad_data = deserialize_bytearray(Get(ctx,ad_id))
		ad_gas_amount = ad_data[7]
		reciever_info = Get(ctx,reciever_id)
		ad_gas_amount = ad_gas_amount / 2
		reciever_info[3] = ad_gas_amount
		reciever_info[4] = reciever_info[4] +1
		Delete(ctx, reciever_id)
		data_serialized = serialize_array(reciever_info)

		Put(ctx,reciever_id,data_serialized)
		if transfer:
			Notify (' Transaction approved')
			update_gas = update_gas(ad_id,ad_gas_amount)
			if update_gas:
				Notify("Gas amount on acc updated ")
				return True 
	return False
	
def GetAdInfo(ad_id):

	ad_data = list(length = 8)
	
	ad_data = Get(ctx,ad_id)

	if ad_data: 
	 	ad_data = deserialize_bytearray(ad_data)
	 	Notify("Here is the ad data")
	 	Notify((ad_data))
	 	return True
	else:
	 	Notify ('ad does not exist')
	 	return False



def Main(operation, args):
	


	

	if operation == "RegisterAd":
		if len(args) == 7:	
			Notify("Length is good ")
			ad_id = args[1]
			#senderhash
			senderhash = args[0] 
			#ad description
			ad_description = args[2]
			#lat and long
			lat_lng = args[3]
			# ad expiration
			ad_exp = args[4]
			# total views
			ad_views = 0
			#auto sell
			ad_sell = args[5]
			#price in gas
			ad_price  = args[6]
			Notify("All vars good ")
			register = register_ad(senderhash,ad_id,ad_description,lat_lng,ad_exp,ad_views, ad_sell,ad_price)

			Notify("Register confirmed in Main")
			return register

	elif operation == "RegisterUser":
		if len(args) == 3:	
			user_hash = args[0]
			userid = args[1]

			user_id = concat(user_hash,userid)
			#user name
			user_name = args[2]
			#user gas amount
			user_gas = 0
			# user views 
			user_views = 0
			return register_user(user_hash,userid,user_id,user_name,user_gas,user_views)

	elif operation == "update_views":
		ad_id = args[0]
		ad_sender = args[1]
		ad_views = args[2]

		updated_views = update_views (ad_id,ad_sender,ad_views)
		return update_views
	

	elif operation == "give_user_gas":
		if len(args) == 3:	
			ad_id = args[0]
			reciever_id = args[1]
			reciever_ad_count = args[2]
			gas_to_user = give_user_gas(ad_id,reciever_id,reciever_ad_count)
			return gas_to_user
	
	
	elif operation == "GetAdInfo":
		if len(args) == 1:	
			ad_id = args[0]
			ad_info =  GetAdInfo(ad_id)
			return ad_info
			
	Notify("Invalid operation")
	return False
