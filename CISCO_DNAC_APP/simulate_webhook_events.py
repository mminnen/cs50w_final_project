#!/usr/bin/env python
from __future__ import print_function
import requests
import datetime
import json
import random

requests.packages.urllib3.disable_warnings()
URL="http://localhost:8000/listen_web_hooks/"

# Generate random dummy sentences
word1 = ("An unmonitored.", "An unknown.", "A managed", "A rogue", "A new")
word2 = ("switch", "access point", "router", "gateway", "endpoint")
word3 = ("disconnects", "crashes", "alarms", "reboots", "is not responding")
word4 = ("without a reason.", "five times.", "again.", "on request of the user.", "above the allowed threshold.")
category = ("CRITICAL", "WARN", "INFO", "MAJOR", "MINOR")
num = random.randrange(0, 5)


def simulate_event():
  """
  https://developer.cisco.com/docs/dna-center/#!getting-started-with-webhooks-on-the-cisco-dna-center-platform/event-schema-and-sample-response
  Note that example on Cisco website is not valid JSON
  Adapted https://github.com/CiscoDevNet/DNAC-Platform for sending events to the Django webhook listener
  """
  event = {
    "category": category[num],
    "status": "NEW",
    "domain": "Availability",
    "severity": "P" + str(random.randint(1, 4)),
    "title": word2[num] + ' ' + word3[num],
    "instanceId": "E-NETWORK-EVENT-AWfQE8aJowzDvHZ5iroE-" + str(random.randint(1000000000, 999999999999)),
    "timestamp": datetime.datetime.now().timestamp() * 1000,
    "actualServiceId": "CC:16:7E:92:2B:40",
    "tenantId": "5c1b2facb982eb004c36c5bd",
    "priority": "P2",
    "source": "DNAC",
    "version": "1.2.0",
    "enrichmentInfo": {
      "connectedDevice": [
        {
          "deviceDetails": {
            "cisco360view": "https://10.10.10.181/dna/assurance/home#networkDevice/undefined"
          }
        }
      ],
      "issueDetails": {
        "issue": [
          {
            "impactedHosts": [],
            "issueDescription": "This AP \"3800.63D4\" is no longer connected to a WLC. This AP was previously connected to the switch \"\" and port \"\".",
            "issueCategory": "Availability",
            "issueSeverity": "MEDIUM",
            "issueSummary": word1[num] + ' ' + word2[num] + ' ' + word3[num] + ' ' + word4[num],
            "issuePriority": "",
            "issueTimestamp": 1545384195506,
            "issueEntityValue": "CC:16:7E:92:2B:40",
            "issueSource": "Cisco DNA",
            "issueEntity": "network_device",
            "issueName": "ap_down",
            "suggestedActions": [
              {
                "message": "Use the \"show cdp neighbor\" command on the switch to verify if the AP is still up, connected to the switch and the AP hostname has not changed. If the AP hostname has reset to the default value (in the form AP{mac-address}), this indicates that the AP has lost its configuration.",
                "steps": []
              },
              {
                "message": "Use the \"show cdp neighbor <portId> detail\" command on the switch to see if the AP has a valid IP address. If it doesn't have an IP address, check the DHCP server.",
                "steps": []
              },
              {
                "message": "Test the Ethernet cable by performing a cable diagnostic check on the switch \"\" and port \"\". Use the following commands: test cable-diagnostics tdr interface \"\" and show cable-diagnostics tdr interface \"\".",
                "steps": [
                  {
                    "entityId": "Unknown",
                    "command": "test cable-diagnostics tdr interface ",
                    "description": "perform cable diagnostic check",
                    "stepType": "command-Runner"
                  },
                  {
                    "entityId": "Unknown",
                    "command": "show cable-diagnostics tdr interface ",
                    "description": "show cable diagnostic check",
                    "stepType": "command-Runner"
                  }
                ]
              },
              {
                "message": "Use the show power inline \"\" command to verify whether PoE is enabled on the switchport \"\".",
                "steps": [
                  {
                    "entityId": "Unknown",
                    "command": "show power inline ",
                    "description": "show if PoE is enabled",
                    "stepType": "command-Runner"
                  }
                ]
              },
              {
                "message": "Use the Path Trace tool to verify whether the AP can communicate with the WLC via UDP ports: 5246 & 5247 (CAPWAP).",
                "steps": []
              },
              {
                "message": "Reboot the AP so it can rejoin the WLC.",
                "steps": []
              }
            ],
            "issueId": "AWfQE8aJowzDvHZ5iroE"
          }
        ]
      }
    },
    "assignedTo": "",
    "type": "Network",
    "id": "AWfQE8aJowzDvHZ5iroE",
    "description": "This AP \"3800.63D4\" is no longer connected to a WLC. This AP was previously connected to the switch \"\" and port \"\"."
    }

  headers={'content-type': 'application/json'}
  response = requests.post(url=URL, data=json.dumps(event), headers=headers, verify=False)
  print(response.status_code)

if __name__ == "__main__":
  simulate_event(event)

