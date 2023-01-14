import pandas
import json
import os
import threading

from datetime import datetime

start = datetime.now()


excel_data_df = pandas.read_excel('NSG.xls', sheet_name='list')

#NSG Rules JSON
json_str = excel_data_df.to_json(orient='records')

#Ingress Rule JSON Append

netData = json.loads(json_str)

ary = []
for x in netData:
    try: 
        netJSON = {}
        netJSON["description"] = x["Description"]
        netJSON["is-stateless"] = "false"

        if ((x["Protocol"] == "tcp") and (x["Direction"] == "ingress")):
        
            netJSON["icmp-options"] = None
            netJSON["udp-options"] = None
            netJSON["direction"] = "INGRESS"
            netJSON["source-type"] = "CIDR_BLOCK"
            netJSON["protocol"] = "6"
            netJSON["source"] = x["Network"]
            netJSON["tcp-options"] = {"destinationPortRange":{"min":x["portl"],"max":x["portm"]}}
            

        elif ((x["Protocol"] == "udp") and (x["Direction"] == "ingress")):
            
            netJSON["icmp-options"] = None
            netJSON["tcp-options"] = None
            netJSON["direction"] = "INGRESS"
            netJSON["source-type"] = "CIDR_BLOCK"
            netJSON["protocol"] = "17"
            netJSON["source"] = x["Network"]
            netJSON["udp-options"] = {"destinationPortRange":{"min":x["portl"],"max":x["portm"]}}
            

        elif ((x["Protocol"] == "icmp") and (x["Direction"] == "ingress")):
            
            netJSON["icmp-options"] = None
            netJSON["direction"] = "INGRESS"
            netJSON["protocol"] = "1"
            netJSON["source"] = x["Network"]
            netJSON["tcp-options"] = None
            netJSON["udp-options"] = None

        elif ((x["Protocol"] == "all") and (x["Direction"] == "ingress")):
            
            netJSON["icmp-options"] = None
            netJSON["direction"] = "EGRESS"
            netJSON["source"] = x["Network"]
            netJSON["protocol"] = "all"
            netJSON["tcp-options"] = None
            netJSON["udp-options"] = None
        
        elif ((x["Protocol"] == "tcp") and (x["Direction"] == "egress")):
        
            netJSON["icmp-options"] = None
            netJSON["udp-options"] = None
            netJSON["direction"] = "EGRESS"
            netJSON["destination-type"] = "CIDR_BLOCK"
            netJSON["protocol"] = "6"
            netJSON["destination"] = x["Network"]
            netJSON["tcp-options"] = {"destinationPortRange":{"min":x["portl"],"max":x["portm"]}}
            

        elif ((x["Protocol"] == "udp") and (x["Direction"] == "egress")):
            
            netJSON["icmp-options"] = None
            netJSON["tcp-options"] = None
            netJSON["direction"] = "EGRESS"
            netJSON["destination-type"] = "CIDR_BLOCK"
            netJSON["protocol"] = "17"
            netJSON["destination"] = x["Network"]
            netJSON["udp-options"] = {"destinationPortRange":{"min":x["portl"],"max":x["portm"]}}
            

        elif ((x["Protocol"] == "icmp") and (x["Direction"] == "egress")):
            
            netJSON["icmp-options"] = None
            netJSON["direction"] = "EGRESS"
            netJSON["protocol"] = "1"
            netJSON["destination"] = x["Network"]
            netJSON["tcp-options"] = None
            netJSON["udp-options"] = None

        elif ((x["Protocol"] == "all") and (x["Direction"] == "egress")):
            
            netJSON["icmp-options"] = None
            netJSON["direction"] = "EGRESS"
            netJSON["destination"] = x["Network"]
            netJSON["protocol"] = "all"
            netJSON["tcp-options"] = None
            netJSON["udp-options"] = None

        else:
            raise "Error processing the excel sheet."
    except:
        print ("Error processing the excel sheet.")

    ary.append(netJSON)

# Serializing json 
json_object = json.dumps(ary, indent = 4)

with open("NSG.json", "w") as outfile:
    outfile.write(json_object)

with open('NSG.json') as f1:
    ll = json.load(f1)

    #this is the total length size of the json file
    print(len(ll))

    #in here 25 means we getting splits of 25 lines
    #you can define your own size of split according to your need
    size_of_the_split=25
    total = len(ll) // size_of_the_split

    #in here you will get the Number of splits
    print(total+1)

    for i in range(total+1):
        json.dump(ll[i * size_of_the_split:(i + 1) * size_of_the_split], open(
           "NSG_Split" + str(i+1) + ".json", 'w', encoding='utf8'), ensure_ascii=False, indent=True)

# Writing to sample.json

end = datetime.now()
print("The time of execution of above program is :",
      str(end-start)[5:])