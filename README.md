# ua-borderpoints

Fetch and show data from the State Customs Service of Ukraine at kordon.customs.gov.ua

#### Installation

Steps assume that `python` (>= 3.9) and `pip` are already installed.

Then, run:

    $ pip install ua-borderpoints

Install directly from ``github``:

    $ pip install git+https://github.com/amstelchen/ua-borderpoints#egg=ua-borderpoints

#### Usage

    $ ua_borderpoints [-h] [-l {uk,en,ru,hu,pl,ro,sk}] -c {md,ro,hu,sk,pl,by,ru,kr} [-d DIRECTION] [-q] [-f FORMAT] [-v]

    Fetch and show data from the State Customs Service of Ukraine at kordon.customs.gov.ua

    options:
    -h, --help            show this help message and exit
    -l {uk,en,ru,hu,pl,ro,sk}, --language {uk,en,ru,hu,pl,ro,sk}
                            what language to use in output
    -c {md,ro,hu,sk,pl,by,ru,kr}, --country {md,ro,hu,sk,pl,by,ru,kr}
                            search for country, i.e. `RO` or `ro` for `Romania`
    -d DIRECTION, --direction DIRECTION
                            specify a direction, i.e. `entry` or `exit`
    -q, --quiet           suppress output
    -f FORMAT, --format FORMAT
                            output format [tab (default)|pandas|json|csv]
    -v, --version         show program's version number and exit

#### Licence

*ua-borderpoints* is licensed under the [MIT](LICENSE) license.
