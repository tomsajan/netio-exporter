# Changelog

All notable changes to this project will be documented in this file.

## [0.0.4] - 2024-03-02
- Added support for caching. This is handy when your netio often looses Wi-Fi connection and you graph in grafana contains gaps. Caching will return the latest collected value in case of problem. It will ensure smooth graph. Cache expiration is configurable to avoid serving stale data for long time.
- Small bugfixes
- add changelog

### Improvements
- Add support for caching

### Bugfix
- fix typo in default `username` value (it included a space)


## [0.0.3] - 2023-03-24
- Add port label to port metrics

### Improvements
- Add port label to port metrics


## [0.0.2] - 2023-03-24
- Fixed AttributeError exception when no MAC or SerialNumber is present
- Add netio application note

### Bugfix
- Fixed AttributeError exception when no MAC or SerialNumber is present

## [0.0.1] - 2019-10-27
Initial release
