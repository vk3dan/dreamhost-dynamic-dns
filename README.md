# dreamhost-dynamic-dns
A tool that can be run as a cronjob on a home machine to update a subdomain with a dynamic IP via dreamhost API

Just put it somewhere, edit config.py with your Dreamhost API key and the subdomain you are updating, then set up your cron job or just run it when you want.
If you do not yet have an API key, visit https://panel.dreamhost.com/index.cgi?tree=home.api and make sure to select "All DNS functions".

This tool is based on [@ianloic's](https://github.com/ianloic) [dreamhost-ddns](https://github.com/ianloic/dreamhost-ddns) server-side CGI script for updating via dyndns tools, but without that functionality and updated for python 3.
