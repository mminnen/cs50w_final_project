#Final project for CS50w 2019.

 A Django APP which integrates with the Cisco Software Defined Network Controller (DNA Center).

The Cisco SDN Controller, also referred to as DNA-C provides a REST API (Intent API) that exposes capabilities
 of the Cisco Platform. This Django app utilizes the Intent API to gather live health-
 statistics from DNAC.
 
Cisco DNA-C can also send events and notificiations using webhooks. This Django app can receive these
events and store them to allow the user to search through these logged events.

Admins have the ability to add DNAC controllers via the Web interface.

More information regarding the DNAC capabilities can be found here:

https://developer.cisco.com/docs/dna-center/#!cisco-dna-center-platform-overview

