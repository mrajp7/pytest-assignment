Requirement:

- python3

Python packages:
- pip3 install pytest
- pip3 install pytest-html
- pip3 install pytest-check
- pip3 install jsonschema

Test group (markers) available are
- user_details
- order
- date_time

To Run the tests navigate to the project folder and run the below command
> pytest
or
> python3 -m pytest

To run only selected group marker
> pytest -m order

Reports can be found on the following path,
> <project>/report/report.html
> <project>/report/report.xml