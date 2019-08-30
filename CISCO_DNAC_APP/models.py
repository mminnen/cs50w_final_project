from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DnacControllers(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class WebhookEvents(models.Model):
    """
    127.0.0.1
    b'{"category": "Warn", "status": "NEW", "domain": "Availability", "severity": "P1", "title": "Device unreachable", "instanceId": "E-NETWORK-EVENT-AWfPwITHowzDvHZ5irk1-1545378759808", "timestamp": 1545378759808, "actualServiceId": "192.168.200.80", "tenantId": "5c1b2facb982eb004c36c5bd", "priority": "P1", "source": "DNAC", "version": "1.2.0", "enrichmentInfo": {"connectedDevice": [{"deviceDetails": {"macAddress": "24:7e:12:50:db:00", "upTime": "55 days, 4:16:00.40", "bootDateTime": "2018-10-27 03:20:37", "neighborTopology": [{"nodes": [{"nodeType": "NetworkDevice", "family": "Switches and Hubs", "platformId": "C9300-48P", "ip": "192.168.200.80", "id": "44e52201-6133-4d6f-b3a6-e0ce24c19d26", "name": "encs-9k.adamlab.cisco.com", "level": 1, "softwareVersion": "16.6.2", "deviceType": "Cisco Catalyst 9300 Switch", "healthScore": 10, "role": "ACCESS"}], "links": []}], "family": "Switches and Hubs", "snmpContact": "", "lineCardCount": "1", "series": "Cisco Catalyst 9300 Series Switches", "apManagerInterfaceIp": "", "lastUpdated": "2018-12-21 07:52:39", "errorCode": "DEV-UNREACHED", "cisco360view": "https://10.10.10.181/dna/assurance/home#networkDevice/44e52201-6133-4d6f-b3a6-e0ce24c19d26", "interfaceCount": "65", "id": "44e52201-6133-4d6f-b3a6-e0ce24c19d26", "serialNumber": "FCW2148G04P", "reachabilityFailureReason": "SNMP Connectivity Failed", "associatedWlcIp": "", "instanceUuid": "44e52201-6133-4d6f-b3a6-e0ce24c19d26", "lastUpdateTime": 1545378759827, "reachabilityStatus": "Unreachable", "hostname": "encs-9k.adamlab.cisco.com", "memorySize": "889822112", "roleSource": "AUTO", "managementIpAddress": "192.168.200.80", "inventoryStatusDetail": "<status><general code=\\"DEV_UNREACHED\\"/></status>", "platformId": "C9300-48P", "collectionStatus": "Partial Collection Failure", "role": "ACCESS", "lineCardId": "d25ce2f9-1675-4638-86c2-bcf5aadc40b9", "tagCount": "0", "errorDescription": "SNMP timeouts are occurring with this device. Either the SNMP credentials are not correctly provided to controller or the device is responding slow and snmp timeout is low. If its a timeout issue, controller will attempt to progressively adjust the timeout in subsequent collection cycles to get device to managed state. User can also run discovery again only for this device using the discovery feature after adjusting the timeout and snmp credentials as required. Or user can update the timeout and snmp credentials as required using update credentials.", "snmpLocation": "", "collectionInterval": "Global Default", "type": "Cisco Catalyst 9300 Switch", "softwareVersion": "16.6.2"}}], "issueDetails": {"issue": [{"issueDescription": "This network device encs-9k.adamlab.cisco.com is unreachable from controller. The device role is ACCESS.", "issueCategory": "Availability", "issuePriority": "", "issueTimestamp": 1545378759808, "issueSource": "Cisco DNA", "issueId": "AWfPwITHowzDvHZ5irk1", "impactedHosts": [], "issueSeverity": "HIGH", "issueSummary": "Network Device 192.168.200.80 Is Unreachable From Controller", "issueEntityValue": "192.168.200.80", "issueEntity": "network_device", "issueName": "snmp_device_down", "suggestedActions": [{"message": "From the controller, verify whether the last hop is reachable.", "steps": []}, {"message": "Verify that the physical port(s) on the network device associated with the network device discovery(IP) is UP.", "steps": []}, {"message": "Verify access to the device.", "steps": []}]}]}}, "id": "AWfPwITHowzDvHZ5irk1", "type": "Network", "assignedTo": "", "description": "This network device encs-9k.adamlab.cisco.com is unreachable from controller. The device role is ACCESS."}'
    """

    instance_id = models.CharField(max_length=50, unique=True)      # instanceId (unique identifier of DNA event)
    source_ip = models.GenericIPAddressField()                      # request.META['REMOTE_ADDR']
    title = models.CharField(max_length=50)                         # title
    category = models.CharField(max_length=50)                      # Category
    domain = models.CharField(max_length=50)                        # domain
    severity = models.CharField(max_length=50)                      # severity
    timestamp = models.DateTimeField(name='Date')                   # timestamp (integer)
    actual_service_id = models.CharField(max_length=50)             # actualServiceId
    issue_description = models.CharField(max_length=100, blank=True, default='', verbose_name='Issue Description')
    # ["enrichmentInfo"]["issueDetails"]["issue"][0]["issueSummary"]

    def __str__(self):
        return f"{self.instance_id} - {self.title}"



