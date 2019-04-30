#-------------------------------------------------------------------------------
# Name:
# Purpose: 
# 
#
# Author: J
#
# Created: 30-04-2019
# Copyright: (c) J 2019
# Licence: <your licence>
#-------------------------------------------------------------------------------

import urllib
import requests
from functools import wraps
import argparse
def retry(exceptions, tries=4, delay=3, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = '{}, Retrying in {} seconds...'.format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


@retry(urllib.error, tries=4, delay=3, backoff=2)
def getwebpage(url,hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}): 
    #req = urllib2.Request(url, headers=hdr)
    return requests.get(url).text


_URL = "https://www.moneycontrol.com/stocks/company_info/print_financials.php"
Type = ('balance','profit','cashflow', 'keyfinratio','balance_cons', 'yearly', 'balance_VI', 'capstru', 'cashflow_VI', 'cons_cashflow_VI', 'cons_halfyearly', 'cons_keyfinratio', 'fingoods', 'halfyearly', 'keyfinratio_VI', 'ninemths', 'ons_keyfinratio_VI', 'profit_cons', 'profit_cons_VI', 'profit_VI', 'quarterly', 'rawmat')
params = {'sc_did': 'IE07', 'type': 'balance','start_year':'','end_year':'','max_year':'','nav':'next'}


def buildurl(url,param):
    return requests.get(url, params=param).url

def GetFileName(page):
    from lxml.html.soupparser import fromstring
    tree = fromstring(page)
    return tree.xpath('//title/text()')[0].split(' >')[0].replace('|','').replace('  ',' ')    

def Download(Url):
    print('Downloading ' + Url + '....')
    page = getwebpage(url)
    FileName = GetFileName(page)
    f = open(FileName + '.html','w')
    f.write(page)
    f.close()
    print('wrote ' + FileName + '.  ok')
 


if __name__ == "__main__":
    path = "C:\\Users\\J\\Desktop\\"
    parser = argparse.ArgumentParser(description='Moneycontrol Fundamentals Downloader')
    parser.add_argument('security',help='security you want to get')
    parser.add_argument('-s','--start-year',help='Starting year of the report')
    parser.add_argument('-e','--end-year',help='End year of the report')
    parser.add_argument('-m','--max-year',help='Maximum report year')
    parser.add_argument('-d','--debug',help='Debug Script',action="store_true")
    args = parser.parse_args()
    
    
    if args.security:
        params['sc_did'] = args.security
        
    if args.start_year:
        params['start_year'] = args.start_year + '03'
   
    if args.end_year:
        params['end_year'] = args.end_year + '03'
        
    if args.max_year:
        params['max_year'] = args.end_year + '03'
    
    if args.debug:
        print(params)
    
    
    url = buildurl(_URL,params)      
    Download(url)
        

