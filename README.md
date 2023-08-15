# locode-to-osmid

This is a data set mapping UN/LOCODE to a corresponding OSM ID for the boundary or node of the city.

## License

Let's say Apache 2.0 for the code, and ODBL for the data? https://opendatacommons.org/licenses/odbl/

Since it's largely output from Nominatim, it probably makes sense to use the same license.

## How it works

The source data is the `Actor.csv` file. It's from OpenClimate, for all the UN/LOCODE cities.

I wrote a script, `generate_locode_to_osmid.py`, that takes a CSV file in the `Actor.csv` format and looks up the name and region or country code in Nominatim, the OpenStreetMap naming system. It then returns the OSM ID for the boundary or node of that item.

The script is probably only going to run once, since it takes a long time to run. (Nominatim has a rate limit of 1 request per second, and there are 100,000+ cities in the data set, so it's about a day of running.)

To run the script, I split the original file into chunks of 1000 cities, so if there was a failure I could start up again from the last chunk.

I also scrambled the chunks, so that the initial output data would be more interesting to test.

I'll upload the output_* files as they finish running, and then I'll combine them into a single file once they're done.
