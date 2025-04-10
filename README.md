
## How to use this repo

This project uses Python. In order to build the project locally, run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

To start the server, from the root directory, run:

```bash
uvicorn main:app --reload
```