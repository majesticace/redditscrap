﻿# Reddit PC Deals Scraper
This Python script scrapes the latest deals from the r/buildapcsales subreddit, specifically targeting posts about "4080 super" white GPUs and 4K OLED monitors. The script runs indefinitely, updating the list every hour, and sends an email notification when new deals are found.

Features
Scrapes the r/buildapcsales subreddit for the latest deals.
Filters posts to find "4080 super" white GPUs and 4K OLED monitors.
Runs continuously, updating the list every hour.
Sends email notifications for new deals.
Requirements
Python 3.x
httpx library
pandas library
smtplib library
