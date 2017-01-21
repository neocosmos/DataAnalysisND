"""
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "London.osm"
#OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
phone_format  = re.compile(r'^\+44\s\d{2}\s\d{8}$') #unified phone format 


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]


mapping = { "St": "Street",
            "St.": "Street",
            "st" : "Street",
            "street": "Street",
            "Steet": "Street",
            "Sreet": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "road": "Road",
            "gate": "Gate",
            "way": "Way",
            "row": "Row",
            "passage":"Passage",
            "parade": "Parade",
            "wharf": "Wharf",
            "broadway":"BroadWay",
            "W.": "West",
            "N.": "North",
            "S.": "South",
            "E": "East"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")
    
def is_phone_number(elem):
    return (elem.attrib['k'] == "contact:phone" or elem.attrib['k'] == "phone" )   

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postal_codes = set()
    phones = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
             for tag in elem.iter("tag"):   
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postal_code(tag):
                    postal_codes.add(tag.attrib['v'])
                if is_phone_number(tag):
                    phones.add(tag.attrib['v'])    
    #pprint.pprint(dict(street_types))                
    pprint.pprint(phones)
    osm_file.close()
    return street_types

# Split the name and check each part against the keys in the mapping
# If exists in the mapping key, overwrite that part with the corrected value.
def update_name(name):
    parts = []
    for name_split in name.split(" "):
        if name_split in mapping.keys():
            name_split = mapping[name_split]
        parts.append(name_split)
    name_updated = " ".join(parts)
    return name_updated 
    
    
def update_phone(phone):
    m =  phone_format.search(phone)
    if not m:
        if isinstance(phone, str):   # phone is string
            bits = filter(str.isdigit, phone)
            if(len(bits)==12):       				# origin string has 12 digits, but extra '( - ' or differ in empty space           
                phone_updated = "+"+bits[0:2]+" "+bits[2:4]+" "+bits[4:12]
            elif(len(bits)==13 and bits[2]=='0'):   # cases like 44 020 **** **** 
                phone_updated = "+"+bits[0:2]+" "+bits[3:5]+" "+bits[5:13]   
            elif(len(bits)==11):                    # case without country code
                phone_updated = "+44"+" "+bits[1:3]+" "+bits[3:11]    
            else:
                return phone
        else: 
             return phone       
    else:
        return phone
    return phone_updated

#The function will be called when writing to .csv in data.py
def update_all(tag):
    if(is_street_name(tag)): 
        return update_name(tag.attrib['v'])
    elif(is_phone_number(tag)):
        return update_phone(tag.attrib['v'])
    else:
        return tag.attrib['v']

if __name__ == '__main__':
    audit(OSMFILE)