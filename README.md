# geotif2fds
Convert LANDFIRE raster data into Fire Dynamics Simulator (FDS) simulations and input files.

# API 
**RUN-FDS (/run-fds)**

*Supports GET/POST requests*

**Description:** Generate and run an FDS simulation with specified conditions. Uses LANDFIRE CONUS raster data to create simulation.

**Query Parameters:**

    latitude
        - latitude coordinate for center of simulation domain. must be within CONUS.
        
    longitude
        - longitude coordinate for center of simulation domain must be within CONUS.
        
    resolution (max=30 ???)
        - the resolution for queried data in meters.
        
    extent (min=5, max=60)
        - the area for the simulation domain in miles. (centered at the lat/long coordinates provided)
        
    x1_fire, y1_fire, x2_fire, y2_fire
        - ???
        
    run (true/false)
        - if "true", query triggers an FDS simulation and returns the input file & output upon completion. 
        - if "false", query returns only the generated FDS input file.
