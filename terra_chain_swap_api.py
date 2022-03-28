import requests
import base64
import json

def amount_to_ucoin (value):
    return value*(10**6)

def astroport_simulation(asset, uquantity=0, quantity=0):
    '''simulates astroport market UST<>LUNA'''
    contract_query = {"simulation":{"offer_asset":{"amount":str(int(amount_to_ucoin(quantity))+int(uquantity)),"info":{"native_token":{"denom":asset}}}}}
    astro_query = requests.get(
    'https://lcd.terra.dev/terra/wasm/v1beta1/contracts/terra1m6ywlgn6wrjuagcmmezzz2a029gtldhey5k552/store',
    params={'query_msg':base64.b64encode(json.dumps(contract_query).encode("ascii")).decode("ascii")})
    return (astro_query.status_code, astro_query.json()) if astro_query.ok else astro_query.status_code

def terraswap_simulation(asset, uquantity=0, quantity=0):
    '''simulates astroport market UST<>LUNA'''
    contract_query = {"simulation":{"offer_asset":{"amount":str(int(amount_to_ucoin(quantity))+int(uquantity)),"info":{"native_token":{"denom":asset}}}}}
    tswap_query = requests.get(
    'https://lcd.terra.dev/terra/wasm/v1beta1/contracts/terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6/store',
    params={'query_msg':base64.b64encode(json.dumps(contract_query).encode("ascii")).decode("ascii")})
    return (tswap_query.status_code, tswap_query.json()) if tswap_query.ok else tswap_query.status_code

def market_simulation(asset_offer, asset_ask, uquantity=0, quantity=0):
    '''simulates terra assets market'''
    mkt_query = requests.get(
    'https://lcd.terra.dev/terra/market/v1beta1/swap',
    params={'offer_coin':f'{str(int(amount_to_ucoin(quantity))+int(uquantity))}{asset_offer}','ask_denom':asset_ask})
    return (mkt_query.status_code, mkt_query.json()) if mkt_query.ok else mkt_query.status_code

def terra_chain_simulation(asset_offer, asset_ask, uquantity=0, quantity=0):
    '''simulates for the best market to trade atm UST(uust)<>LUNA(uluna). Can use uunits of value (uquantity) and/or units (quantity)'''
    astroport = astroport_simulation(asset_offer, uquantity, quantity)
    terraswap = terraswap_simulation(asset_offer, uquantity, quantity)
    market = market_simulation(asset_offer, asset_ask, uquantity, quantity)
    print(f'astroport: {astroport} \nterraswap: {terraswap} \nmarket: {market}')
    try:
        returned_amount = (
            int(astroport[1]['query_result']['return_amount']),
            int(terraswap[1]['query_result']['return_amount']),
            int(market[1]['return_coin']['amount'])
            )
        prefered_swap = ('astroport', 'terraswap', 'market')[returned_amount.index(max(returned_amount))]
        prefered_amount = max(returned_amount)
        print(f'prefered {prefered_swap}: returns {prefered_amount} {asset_ask}')
    except:
        print('error lcd requests')
        terra_chain_simulation(asset_offer, asset_ask, uquantity, quantity)
    else:
        return prefered_swap, prefered_amount


