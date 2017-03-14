# wifi-occupancy-sensor

This goal of this project is to build a Wi-Fi powered occupancy sensor. This
will become the basis for a series of home automation projects.


## The Premise
The members of my household (and authorized visitors) tend to carry Wi-Fi
enabled devices (like smartphones) which automatically connect to my Wi-Fi
network when they are in range. Each time a device connects, it uses DHCP to
acquire an IP address and configuration. The DHCP server keeps track of
connected devices so that it knows which IP addresses are available to assign
to new devices. Since each device has a unique identifier (the MAC address), I
can associate the unique identifier with a person and query the leases table to
see when they are home (or within Wi-Fi range.

## The Plan
To take advantage of this, I plan to configure a Raspberry Pi to run the DHCP
server for my home network. The Raspberry Pi will also the software in this
repository to do the following.

1. Monitor the DHCP leases and keep track of them in a SQLite repository.
1. Provide a web application for mapping devices to profiles (ie. a person who
   lives here, a named guest, an anonymous guest, infrastructure).
1. Provide a RESTful web interface to allow other devices or applications to
   query the occupancy.
1. Trigger arbitrary events based on presence (control thermostat, lighting,
   garage door, music selections, etc.).
1. Track the occupancy data over time to allow for analytical analysis.

