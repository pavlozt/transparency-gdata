# Transparency Report Downloader

[Google's Public Data Program](https://transparencyreport.google.com/traffic/overview) provides researchers, data journalists, and community activists with access to Google's array of structured data about amount of traffic. This data is not available as files.  To obtain live data, an additional container with  [Selenium Browser](https://github.com/SeleniumHQ/selenium) is used.


## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [First run](#first-run)
- [Periodical data updates](#periodical-data-updates)
- [Debugging](#debugging)
- [License](#license)

## Requirements

You need install `docker` with  `docker compose` plugin.
Because it runs a browser inside the container, for normal operation, you will need resources amounting to 1-1.5 GB of RAM.

## Usage

The parser can be run without specifying command line arguments, but there are some useful arguments

-   `--loop`: Start special loop mode.
-   `--start`: Start time in Unix timestamp * 1000 (miliseconds).
-   `--end`: End time in Unix timestamp * 1000 (miliseconds).
-   `--product`: Product identifier. Default is `21` (YouTube).
-   `--region`: Region identifier. Default is `RU`.
-   `--step`: Step interval in miliseconds. Default is 30 days (`60*60*24*30*1000`).
-   `--pause`: Pause. Wait some seconds between fetching in loop mode. Default is `30`.
-   `--filename`: Output filename.  (default is `data.xlsx`).

Data is written to the directory `data` using `openpyxl` python module.

## First run

First of all, you need to build container images:
```
docker compose build
```

Most likely, for the first download you will want to download historical data.
To do this, you need to run the container with the **--loop** parameter. The necessary date parameters can be obtained from the page URL.
```
docker compose run --rm parser  --loop --start 1643587200000 --end 1734825599999 --pause 10 --product 21 --region RU
```

Parameters can be obtained from the URL in Google Transparency Report. These are millseconds of Unixtime. That is, you need to use Unixtime and multiply by 1000.


## Periodical data updates


The program is adapted for launching in Docker Compose. To update the data periodically, you need to configure the launch of the following command to the cron:

```
0 2 * * * /usr/bin/docker compose -f /path/to/project/docker-compose.yaml run --rm parser --product 21 --region RU
```

To save resources you can additionally run
`/usr/bin/docker compose -f /path/to/project/docker-compose.yaml down geckodriver`

## Debugging

Sometimes it may not work well. Here are some tips for debugging:

- Read about debugging Selenium https://github.com/SeleniumHQ/docker-selenium#debugging
- Uncomment port 7900 in docker-compose.yaml and check browser state at URL http://localhost:7900/?autoconnect=1&resize=scale


## Publishing data

I suggest publishing data to Google Drive using [rclone](https://github.com/rclone/rclone).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
