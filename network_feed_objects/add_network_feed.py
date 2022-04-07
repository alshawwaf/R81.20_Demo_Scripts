#!/usr/bin/env python3
"""
This scxript will create two network feed objects:
- Object to retreive a JSON list
- Object to retreive a flat list
 
"""
import argparse
import logging

from cpapi import APIClient, APIClientArgs

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", default="admin")
    parser.add_argument("-p", "--password", default="Cpwins!1")
    parser.add_argument("-m", "--management", default="203.0.113.120")
    parser.add_argument("-d", "--domain", default="System Data")
    parser.add_argument("-s", "--server", default="203.0.113.200")  
    parser.add_argument("-t", "--targets", default="gw_r81_20") 

    parsed_args = parser.parse_args()

    client_args = APIClientArgs(server=parsed_args.management)

            
    with APIClient(client_args) as client:
        # login to local domain to create the Network Feed objects
        login = client.login(username=parsed_args.username,
                             password=parsed_args.password)
        if login.success:
            log.info("login succeeded")
        else:
            log.error(login.error_message)
                  
        add_json_feed = client.api_call(
            "add-network-feed", payload={  "name" : "network_feed_json", "feed-url" : f"http://{parsed_args.server}:5000/get-json", "feed-format" : "JSON", "feed-type" : "IP Address", "update-interval" : 60, "json-query" : ".objects[].ranges[]", "use-gateway-proxy" : "false", "ignore-warnings":"true"})
        
        if add_json_feed.success:
            log.info("Created JSON network feed object")
        else:
            log.error(add_json_feed.error_message)

        add_list_feed = client.api_call(
            "add-network-feed", payload={  "name" : "network_feed_list", "feed-url" : f"http://{parsed_args.server}:5000/get-list", "feed-format" : "Flat List", "feed-type" : "IP Address", "fields-delimiter" : ",", "ignore-lines-that-start-with" : "#", "use-gateway-proxy" : "false", "ignore-warnings":"true"})
        
        if add_list_feed.success:
            log.info("Created flat list network feed object")
        else:
            log.error(add_list_feed.error_message)
            
        # publish after creating SmartTasks and Mail server
        publish = client.api_call(
            "publish", payload={})

        if publish.success:
            log.info("Publishing session")
        else:
            log.error(publish.error_message)

  
        check_list_feed = client.api_call(
            "check-network-feed", payload={ "network-feed" : {"name" : "network_feed_list", "feed-url" : f"http://{parsed_args.server}:5000/get-list"}, "targets" : f"{parsed_args.targets}"})
        
        if check_list_feed.success:
            log.info("Checking network feed status")
            log.info(check_list_feed.data['tasks'][0]['task-details'][0])
        else:
            log.error(check_list_feed)
                      
if __name__ == "__main__":
    main()