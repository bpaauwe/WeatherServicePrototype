
# weatherserver-prototype

This is a node server to pull weather data from a service and make it available to a [Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2)
(c) 2018 Robert Paauwe
MIT license.

This node server is intended as a prototype. It is not intendted to be used in any production environment. 

## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install.
3. Add NodeServer in Polyglot Web
   * After the install completes, Polyglot will reboot your ISY, you can watch the status in the main polyglot log.
4. Once your ISY is back up open the Admin Console.
5. Configure the node server per configuration section below.

### Node Settings
The settings for this node are:

#### Short Poll
   * Not used
#### Long Poll
   * How often to poll the weather service. Note that various weather services have restrictions on how often they can be called, exeeding that limit may result in the node server being blocked.


## Requirements

1. Polyglot V2 itself should be run on Raspian Stretch.
  To check your version, ```cat /etc/os-release``` and the first line should look like
  ```PRETTY_NAME="Raspbian GNU/Linux 9 (stretch)"```. It is possible to upgrade from Jessie to
  Stretch, but I would recommend just re-imaging the SD card.  Some helpful links:
   * https://www.raspberrypi.org/blog/raspbian-stretch/
   * https://linuxconfig.org/raspbian-gnu-linux-upgrade-from-jessie-to-raspbian-stretch-9
2. This has only been tested with ISY 5.0.14 so it is not guaranteed to work with any other version.

# Upgrading

Open the Polyglot web page, go to nodeserver store and click "Update" for "WeatherFlow".

For Polyglot 2.0.35, hit "Cancel" in the update window so the profile will not be updated and ISY rebooted.  The install procedure will properly handle this for you.  This will change with 2.0.36, for that version you will always say "No" and let the install procedure handle it for you as well.

Then restart the nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

The nodeserver keeps track of the version number and when a profile rebuild is necessary.  The profile/version.txt will contain the profile_version which is updated in server.json when the profile should be rebuilt.

# Release Notes

- 0.0.1 10/24/2018
   - Initial version published to github
