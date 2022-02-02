NiftyTracker
-----

### Introduction

A simple app that allows a user to connect their Metamask wallet, sign in and see some information about themselves.

Based on the [siwe-quickstart](https://github.com/spruceid/siwe-quickstart) demo by [Spruce](https://spruceid.com/), changing the backend from NodeJs to Flask. Lots of help from the [django-siwe-auth](https://github.com/payton/django-siwe-auth) demo written by [Payton](https://twitter.com/PaytonGarland).

### Tech Stack

* **Python3** and **Flask** as server language and server framework
* **HTML**, **NodeJs** for the frontend
* [**SIWE**](https://github.com/spruceid/siwe) and [**SIWE-py**](https://github.com/spruceid/siwe-py) for Ethereum-based authentication

### Running Locally

In Anaconda, install siwe-py using pip:
```bash
pip install siwe
```
Run the Flask server
```bash
set FLASK_APP=app.py
flask run
```

In a separate terminal navigate into the frontend folder
```bash
cd frontend
```
Install all the necessary packages
```bash
npm install
```
Launch the frontend
```bash
npm run dev
```

### Deploy to Heroku
**TODO**

### TODOs
- logout button
- display signed in address on frontend
