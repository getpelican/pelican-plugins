# Change Log #
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## x.x.x – TBA
### Fixed
- Add support for the autoreload mode of pelican [PR #782](https://github.com/getpelican/pelican-plugins/pull/782) [Fixes pelican#1949](https://github.com/getpelican/pelican/issues/1949)

## 1.2.0 – 2016-05-23
### Fixed - Documentation
- Correct template path [PR #713](https://github.com/getpelican/pelican-plugins/pull/713)

### Added - Documentation
- Adds Quickstart guide + default theme [PR #686](https://github.com/getpelican/pelican-plugins/pull/686)

### Fixed
- Fix mailto link: use '\r\n' instead of '\n' [PR #720](https://github.com/getpelican/pelican-plugins/pull/720)
- Fix comparison of offset-naive and offset-aware datetimes [PR #722](https://github.com/getpelican/pelican-plugins/pull/722)

### Added
- Logs a warning if the parent of a comment can not be found [PR #715](https://github.com/getpelican/pelican-plugins/pull/715)

## 1.1.0 – 2016-02-18
### Fixed – Documentation
- Updated old URLs [PR #677](https://github.com/getpelican/pelican-plugins/pull/677)

### Changed
- Main logic runs a bit earlier (allows other plugins to access comments earlier)  [PR #677](https://github.com/getpelican/pelican-plugins/pull/677)
- The writer to generate the feeds can now be exchanged (via a normal pelican writer plugin) [PR #677](https://github.com/getpelican/pelican-plugins/pull/677)


## 1.0.1 – 2015-10-04
### Fixed – Documentation
- Add commas indicating tuple (`PELICAN_COMMENT_SYSTEM_AUTHORS`) [PR #579](https://github.com/getpelican/pelican-plugins/pull/579)


## 1.0.0 – 2014-11-05
### Added
- Basic static comments
- Atom Feeds
- Replies to comments
- Avatars and identicons


This change log uses [Keep a CHANGELOG](http://keepachangelog.com/) as a template.

