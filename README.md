# Namedrop

Writes nice file names for your images.

Demo:
https://x.com/charliebholtz/status/1737667912784134344?s=20

Run it in the background to never have to see `<Screenshot 2023-12-20 at 7.30.01 PM.png>` again.

Namedrop also adds a meta attribute to your filename so you don't have to worry about it running twice on the same file.

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
export REPLICATE_API_TOKEN=<token>
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
