import random
from flask import Flask, request

app = Flask(__name__)


#This is just a toy
#That does nothing as of now.

@app.route('/')
def get_vol():
    print(request.args)
    
    #vol_c = int(request.args['vol_chance'])

    
    if request.args.get('vol_chance') == None:
        vol_c = 32#int(request.args['vol_chance'])
    else: 
        vol_c = int(request.args.get('vol_chance'))
    
    if not vol_c:
        vol_c = 23

    precip_type = "rain"

    is_cold = vol_c < 0
    is_warm = vol_c > 25

    if is_cold:
        print('low val env detected')
        precip_type = "snow"

    if is_warm:
        print('high vol env detected')
        precip_type = "storms"

    percent_chance = round(random.uniform(0, 1) * 100)

    return {
        'vol_chance': percent_chance,
        'type': precip_type
    }



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5003')
