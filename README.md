# bloodhound-convert
Python based [Bloodhound](https://github.com/BloodHoundAD/BloodHound) data converter from the legacy pre 4.1 format to 4.1+ format

**NOTE**  
While I've tested this on multiple dumps of mine and they seemed to work fine, I don't expect all the Bloodhound queries to work correctly on this so keep this in mind.

## Installation
The tool can be installed manually by cloning this repository and running the setup file:
```sh
git clone https://github.com/szymex73/bloodhound-convert
cd bloodhound-convert

# For a global install
python setup.py install

# For a local install
python setup.py install --user
```

## Usage
Project can be used with or without installing it on the system.

With [installation](#installation) the project installs a module and can be either accessed through the global `bloodhound-convert` script or through `python -m bloodhound_convert`.
Without installation it can be used by cloning the repository and running the `bloodhound-convert.py` python script.

Usage is as follows:
```sh
bloodhound-convert input output
```
Where the arguments are:
- `input` is either a bloodhound data zip file, or a directory containing bloodhound json data files
- `output` is either a zip filename for the data to be bundled into, or a directory for the json files to be saved in

## Why?
As I go back to previous bloodhound dumps from various ctf boxes and/or labs I've done I have to switch between the new version and the pre 4.1 version because of the data format change. This is both tedious and annoying, especially since the old version stopped working on my machine :).  
So to fix this I made this to convert my old bloodhound dumps into the new format so I can use a single version until the format changes again.

## TODO?
Maybe add some actual json file checks as currently this just verifies the json files by the extension.  
Maybe make this into an actual ingestor so it pushes data straight into neo4j? Most likely not but who knows.  
Even though Bloodhound ingests the data fine, it seems to quietly throw errors when importing the computer objects into the DB, doesn't seem to cause problems but might be worth investigating.

## Acknowledgements
I've used the [BloodHound.py](https://github.com/fox-it/BloodHound.py) project as a rough guide on how to do the format conversion, specifically the commits used to make it compatible with the new 4.1+ format.
