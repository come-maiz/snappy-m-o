# Snappy Microbe-Obliterator _(snappy-m-o)_

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat)](https://github.com/RichardLitt/standard-readme)

[![Snap Status](https://build.snapcraft.io/badge/elopio/snappy-m-o.svg)](https://build.snapcraft.io/user/elopio/snappy-m-o)

Continuous integration bot for the snapcraft team.

## Install

In any of the [supported Linux distros](https://snapcraft.io/docs/core/install):

```
sudo snap install snappy-m-o --edge --classic
```

## Usage

```
SNAPCRAFT_AUTOPKGTEST_SECRET=${SNAPCRAFT_AUTOPKGTEST_SECRET} SNAPPY_M_O_SLACK_TOKEN=${SNAPPY_M_O_SLACK_TOKEN} snappy-m-o &
```

Where `${SNAPCRAFT_AUTOPKGTEST_SECRET}` is a value provided by the Canonical
Foundations team and `${SNAPPY_M_O_SLACK_TOKEN}` is the token for the slack
integration.

After running this command, the bot will join slack and most be invited to a
channel.

### Available commands

Run the autopkgtests in a pull request:

    @snappy-m-o autopkgtest <pull-request-number> [<distribution>:<architecture> ...]

For example, to run the autopkgtests in pull request 1111 for xenial amd64 and bionic armhf:

    @snappy-m-o autopkgtest 1111 xenial:amd64 bionic:armhf

Subscribe to the results of a pull request:

    @snappy-m-o github subscribe <pull-request-number>

Build and publish the snapcraft snap from a pull request:

    @snappy-m-o github build <pull-request-number>

Get the URL to download the snapcraft snap build by travis:

    @snappy-m-o travis snapurl <pull-request-number>

## Maintainer

[@kyrofa](https://github.com/kyrofa/)

## Contribute

If you want to contribute, contact [@kyrofa](https://github.com/kyrofa/) or
leave a comment in the [snapcraft forum](https://forum.snapcraft.io/).

## License

[GNU General Public License v3.0 only](LICENSE) (C) 2017-2018 Canonical Ltd
