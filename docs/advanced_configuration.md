# Advanced Configuration

Can only be configured before building

## Logging format and levels

see `app.config.log.py`

## Timestamp format

Currently set to `DD.MM.YY HH:MM:SS`. Timestamps are saved to the database as UTC and displayed according to local time

Change in `app.config.internal_config.py`

## Background color

Default: `(204 / 255, 204 / 255, 204 / 255)`

Change in `app.config.internal_config.py`

