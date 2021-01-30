# geotif2fds
Convert LANDFIRE raster data into Fire Dynamics Simulator (FDS) simulations and input files.

<br>

# API 
**RUN-FDS (base-url/run-fds)** - Supports GET/POST requests

**Description:** Generate and run an FDS simulation with specified conditions. Returns specified output (simulation output files or FDS input file) in a compressed .zip folder.

**Query Parameters (all required):**

    latitude:
    - latitude coordinate for center of simulation domain. must be within CONUS.
        
    longitude
    - longitude coordinate for center of simulation domain must be within CONUS.
        
    resolution (max=30 ???)
    - the resolution of queried data in meters.
        
    extent (min=5, max=60)
    - the area of the simulation domain in square miles. (centered at the lat/long coordinates provided)
        
    x1_fire, y1_fire, x2_fire, y2_fire
    - ???
        
    run (true/false)
    - if "true", query triggers an FDS simulation and returns the input file & output upon completion. 
    - if "false", query returns only the generated FDS input file.

<br>

# Examples

**HTTP GET**

Request must specify values for each parameter. The following example creates and runs a FDS simulation roughly centered on Slacker Hill in the San Fransisco bay area, at 30 meters resolution:

    base-url/run-fds?name=slacker_hill&longitude=-122.489732&latitude=37.834887&resolution=30&extent=5&time=1&x1_fire=1&y1_fire=1&x2_fire=1&y2_fire=1&run=true

This request may be executed using the command line utility, <code>curl</code>, with the -o option, or instead by simply pasting into a browser window.

**HTTP POST**

POST requests are currently only supported through the request builder form, located at:

 **base-url/request-builder**

Fill out and submit the form to create an FDS input file or run a full simulation.

