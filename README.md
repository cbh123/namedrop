# Namedrop

Writes nice file names for your images.

https://twitter.com/charliebholtz/status/1724815159590293764

## Setup

Clone this repo, and setup and activate a virtualenv:

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Then, install the dependencies:
`pip install -r requirements.txt`

Make a [Replicate](https://replicate.com) account and set your tokens:

```
export REPLICATE_APIT_TOKEN=<token>
```

## Run it!

In on terminal, run `python main.py <directory-name>`. namedrop
will then watch that directory for changes and rename any image file.

For example, I run it on my desktop with:

```bash
python main.py ~/Desktop
```

You can also run namedrop on a specific file:

```bash
python main.py <path-to-file>
```
