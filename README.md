# UoE Grades Scraping
Web scrap your grades from [MyEd](https://www.myed.ed.ac.uk/myed-progressive/)!

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements from *requirements.txt*.

```shell script
pip install -r requirements.txt
```

Install the latest [Chrome WebDriver](https://chromedriver.chromium.org/downloads)
and place the *chromedriver* file in the *drivers* directory.

```
uoe-grades-scraping
├───drivers
│   └───chromedriver
├───main.py
...
```

## Usage
Run the *main.py* file with Python.
```shell script
python main.py
```

You will be prompted for your login and password for *MyEd*. The data is secure,
it isn't sent anywhere else - it just stays on your machine.

## Result
If everything goes well, you should get a file *grades.json*, similar to that one:
```json
{
    "name": "FirstName MiddleName LastName",
    "uun": "S*******",
    "average": "**.**%",
    "courses": [
        {
            "name": "*****************",
            "code": "*******",
            "grade": {
                "exact": "**%",
                "symbol": "A1"
            }
        },
        {
            "name": "*****************",
            "code": "*******",
            "grade": {
                "exact": "**%",
                "symbol": "A1"
            }
        },
        {
            "name": "*****************",
            "code": "*******",
            "grade": {
                "exact": "**%",
                "symbol": "A1"
            }
        },
        {
            "name": "*****************",
            "code": "*******",
            "grade": {
                "exact": "Pass",
                "symbol": "P"
            }
        },
        {
            "name": "*****************",
            "code": "*******",
            "grade": {
                "exact": "Pass",
                "symbol": "P"
            }
        },
        {
            "name": "*****************",
            "code": "*******",
            "grade": {
                "exact": "Pass",
                "symbol": "P"
            }
        }
    ]
}
```