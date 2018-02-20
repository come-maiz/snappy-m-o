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
SNAPCRAFT_AUTOPKGTEST_SECRET=${SNAPCRAFT_AUTOPKGTEST_SECRET} snappy-m-o &
```

Where `${SNAPCRAFT_AUTOPKGTEST_SECRET}` is a value provided by the Canonical Foundations team.

## Maintainer

[@kyrofa](https://github.com/kyrofa/)

## Contribute

If you want to contribute, contact [@kyrofa](https://github.com/kyrofa/) or
leave a comment in the [snapcraft forum](https://forum.snapcraft.io/).

## License

[GNU General Public License v3.0 only](LICENSE) (C) 2017-2018 Canonical Ltd
