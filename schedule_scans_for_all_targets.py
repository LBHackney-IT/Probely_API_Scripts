#!/usr/bin/env python

import csv
import requests
from urllib.parse import urljoin

from datetime import datetime
from datetime import timedelta

API_BASE_URL = "https://api.probely.com"

def api_headers(api_token):
    return {"Authorization": "JWT {}".format(api_token)}

# def flatten_scan_response(scheduled_scan):
#     return {
#         "id": scheduled_scan["id"],
#         "target_id": scheduled_scan["target"]["id"],
#         "target_name": scheduled_scan["target"]["site"]["name"]
#     }

def get_scheduled_scans(api_token):
    scheduled_scans_endpoint = urljoin(
        API_BASE_URL, "scheduledscans/?length=10000"
    )

    headers = api_headers(api_token)
    response = requests.get(scheduled_scans_endpoint, headers=headers)
    print(response.content)
    # results = list(map(flatten_scan_response, response.json()["results"]))

    targets = {}
    for scheduled_scan in response.json()["results"]:
        target_id = scheduled_scan["target"]["id"]
        if target_id not in targets:
            targets[target_id] = {
                "id": target_id,
                "name": scheduled_scan["target"]["site"]["name"],
                "scheduled_scans": []
            }

        targets[target_id]["schedule_scans"].append({
            scheduled_scan["id"]
        })
    print(results)

def main():
    api_token = input("API Token:")
    
    get_scheduled_scans(api_token=api_token)
    quit()

    targets_endpoint = urljoin(
        API_BASE_URL, "targets/?include=compliance&length=10000"
    )
    headers = api_headers(api_token)
    response = requests.get(targets_endpoint, headers=headers)
    results = response.json()["results"]

        # target id
        # "date_time": "2019-08-24T14:15:22Z",
        # "recurrence": "h",
        # "timezone": "string",
        # "run_on_day_of_week": true,
        # "scheduled_day_of_week": 1,
        # "week_index": "first",
        # "partial_scan": true,
        # "override_target_settings": true,
        # "incremental": true,
        # "reduced_scope": true,
        # "scan_profile": "lightning"

    # Given timestamp in string
    time_str = '23/9/2023 00:00:00'
    date_format_str = '%d/%m/%Y %H:%M:%S'

    # create datetime object from timestamp string
    start_time = datetime.strptime(time_str, date_format_str)
    minutes_to_add_each_time = 5

    for result in results:
        start_time = start_time + timedelta(minutes=minutes_to_add_each_time)

        # Convert datetime object to string in the format Probely needs 
        schedule_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Create a payload to create a scheduled scan. 
        # See https://developers.probely.com/#tag/Scheduled-Scans/operation/targets_scheduledscans_create
        schedule_payload = {
            "date_time": schedule_time_str,
            "recurrence": "w", # weekly
            "timezone": "UTC",
            # "run_on_day_of_week":
            # "scheduled_day_of_week": 6, # Saturday
            # "week_index":
            # "partial_scan": False
            # "override_target_settings":
            # "incremental":
            # "reduced_scope":
            # "scan_profile": # not set, as we'll use the target's settings
        }

        target_id = result["id"]
        scheduled_scan_url = urljoin(
            API_BASE_URL, f"targets/{target_id}/scheduledscans/"
        )

        # Send the new scheduled scan to Probely
        # response = requests.post(
        #     scheduled_scan_url,
        #     headers=headers,
        #     json=schedule_payload,
        # )

        # print(scheduled_scan_url)
        print(schedule_payload)
        print(response.status_code)
        print(response.reason)
        # print(response.content)


if __name__ == '__main__':
    main()
