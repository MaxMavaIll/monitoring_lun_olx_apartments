

import toml

from function import Helper
from Lun import monitoring as lun
from OLX import monitoring as olx

config_toml = toml.load('config.toml')


TOKEN = config_toml['tb_bot']['token']
CHAIN_ID = config_toml['tb_bot']['chain-id']

def main():
    helper = Helper()
    data = helper.get_json()

    lun.check_flat_with_filter(TOKEN, CHAIN_ID, data)
    olx.check_flat_with_filter(TOKEN, CHAIN_ID, data)

    helper.set_json(data)



    
    
    
if __name__ == "__main__":
    main()