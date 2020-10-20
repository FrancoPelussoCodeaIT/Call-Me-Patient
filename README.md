# Call me, Patient

Query your patient data from different sources and wrangle it into a single dataset with any criteria you like the most.


## Dependencies

* Python 3.8 (3.6 and 3.7 may work but aren't tested, older versions won't work).


## Try it out!

You may run the example code inside **example_usage.py** file by simply running: `python3.8 example_usage.py`.


## Running tests

A simple set of tests is included in the **tests.py** file which can be run with following command: `python3.8 tests.py`.


## Design

* It is intended to be used as a library, therefore why it can be installed with pip right out of the box (`pip install git+https://github.com/FrancoPelussoCodeaIT/Call-Me-Patient`).

* Its main focus is on versatility and extensibility. You may add your own parsers, wranglers and patient queries by just subclassing what you need. Read any input you want and wrangle it as needed!

* It has three different elements:
    * **Parser**: It reads an input and processes it into the library's custom model: **PatientInfo**.
    * **Wrangler**: It takes a list of **PatientInfo** instances with different data and unifies it into a single **PatientInfo**.
    * **PatientQuery**: It links a *Parser* with one or more *Wranglers*.
