
from urllib import urlopen
import re
from itertools import chain

javascript = re.compile(r"ibsys.htvClosings.init\(({.*?})\)") #The closings are embeded in a javascript function. This will extract the dictionary to group 1.
wgalAddress = "http://www.wgal.com/weather/closings"
def closings(useCache=True, cache="closings.html"):
    """Returns a dictionary containing information about closed schools and bussinesses.
    Keyword Arguments:
    useCache -- If true function will use cache instead of going online (default True)
    cache    -- The file that a cache of the website will be stored in. If none or the file does not exist, useCache will be changed to True (default \"closing.html\")
    """
    if not cache: useCache = False
    if useCache:
        try:
            with open(cache, 'r') as cacheFile:
                wgalSite = cacheFile.read()
        except IOError:
            return closingDictionary(updateCache=False, cache=cache)
    else:
        wgalSite = urlopen(wgalAddress).read()
        if cache:
            with open(cache, 'w') as cacheFile:
                cacheFile.write(wgalSite)

    rawData = eval(re.search(javascript, wgalSite).group(1)) #The parsed data is a valid python dictionary
    organizedDict = {place.pop('name'): place for place in #Change the name into the key
                     chain(*(letter['institutions'] for letter in rawData.values() if type(letter) == dict))} #The raw data is organized by letter. Extract "institutions" from each and chain them together.
    return organizedDict

if __name__ == '__main__':
    for school, data in closings(False).iteritems():
        print school
        for key, value in data.iteritems():
            print '\t'+key.upper()+': '+value