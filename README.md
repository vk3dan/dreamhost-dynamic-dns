# dreamhost-dynamic-dns
A tool that can be run as a cronjob on a home machine to update a subdomain with a dynamic IP via dreamhost API

Just put it somewhere, edit config.py with your Dreamhost API key and the subdomain you are updating, then set up your cron job or just run it when you want.
If you do not yet have an API key, visit https://panel.dreamhost.com/index.cgi?tree=home.api and make sure to select "All DNS functions".

To set this up as a cron job to run every 5 minutes, add a line like this using crontab -e

```*/5 * * * * cd /name/of/directory/where/you/put/this/app && ./ddns.py >> ./ddns.log 2>&1```

example log output:
```
[2021-12-19 00:00:05.710972] Public IP address is: 123.123.123.123
[2021-12-19 00:00:07.487294] Current Record: some.domain.name | A | 123.123.123.123
[2021-12-19 00:00:07.487395] Exiting: No change needed
```

This tool is based on [@ianloic's](https://github.com/ianloic) [dreamhost-ddns](https://github.com/ianloic/dreamhost-ddns) server-side CGI script for updating via dyndns tools, but without that functionality, updated for python 3 and customised the way I want it.
