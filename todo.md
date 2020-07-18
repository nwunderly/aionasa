# TO DO

- APOD
    - add async downloading to --download option
        - (need to limit number of connections somehow and wait until all tasks are complete)
        - allow users to specify a directory to download images to (ie: "--download .")
    - add support for undocumented parameters (multiple dates, etc).
    - --dump csv support?
    - add support for non-apod archived images (youtube etc)

- decide if each API will get its own client, or one module-level client

- handle rate limiting

- next API: InSight?