#!/usr/bin/env python

import csv
import requests
from urllib.parse import urljoin

from datetime import datetime
from datetime import timedelta

def main():
    token = input("API Token:")

    headers = {"Authorization": "JWT {}".format(token)}

    api_base_url = "https://api.probely.com"
    targets_endpoint = urljoin(
        api_base_url, "targets/?include=compliance&length=10000"
    )

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
            api_base_url, f"targets/{target_id}/scheduledscans/"
        )

        # Send the new scheduled scan to Probely
        response = requests.post(
            scheduled_scan_url,
            headers=headers,
            json=schedule_payload,
        )

        # print(scheduled_scan_url)
        print(schedule_payload)
        print(response.status_code)
        print(response.reason)
        # print(response.content)


if __name__ == '__main__':
    main()
