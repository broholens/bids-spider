from sites import sites
from gov_parser import Bid

for site in sites:
    b = Bid(**site)
    b.get_info()