# SoundCloud Add-on for [Kodi](https://github.com/xbmc/xbmc)

This add-on provides a minimal interface for SoundCloud.

## Features

* Search tracks
* Play tracks

## API

Documentation of the **public** interface.

### plugin://plugin.audio.soundcloud/play/?[id|slug]

Examples:

* `plugin://plugin.audio.soundcloud/play/?id=1`
* `plugin://plugin.audio.soundcloud/play/?slug=epic-song`

## Development

This add-on uses [Pipenv](https://pypi.org/project/pipenv/) to manage its dependencies.

### Setup

[Install Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) and run `pipenv install --dev`.

### Build

Run `pipenv run build`.

### Lint

Run `pipenv run lint`.

### Test

Run `pipenv run test`.

> Requires at least Python 3.6!

## Roadmap

* Re-implement all features from original add-on

## Attributions

This add-on is strongly inspired by the [original add-on](https://github.com/SLiX69/plugin.audio.soundcloud)
developed by [bromix](https://kodi.tv/addon-author/bromix) and [SLiX](https://github.com/SLiX69).

## Copyright and license

This add-on is licensed under the MIT License - see `LICENSE.txt` for details.
