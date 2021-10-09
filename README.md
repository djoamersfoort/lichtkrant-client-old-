# Lichtkrant Client

This is the client for all the online games on the djo lichtkrant

## Installation

```bash
git clone https://@github.com/djoamersfoort/lichtkrant-client
cd lichtkrant-client
python -m venv ENV
source ./ENV/bin/activate
pip install -r requirements.txt
```

Then you can simply run it with `python client.py`.
If the pip install gives you some kind of python execution error,
you might need to install the python development package: `python-dev` or `python-devel`.

## Info

You can find the implementation of the games in the [lichtkrant repo](https://github.com/djoamersfoort/lichtkrant).
Playing the games using plain netcat is technically supported,
but there are a few quirks to do so:

- You need to type the key and send it with Enter (or turn on instant send with `Ctrl-D`
- If you want to stop moving you also need to send a new key that is not a movement key

This small client solves these issues by sending a single key combined based on listeners.
