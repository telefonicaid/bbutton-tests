# bbutton-tests
BButton project Tests repository 


## How to launch the tests

### Requirements

To the tests need python 2.7 and the required libs listed in the requirements file

´´´
pip install -r requirements.txt
´´´  

### Config your environment 

In the instances.json file set your ips of the instances under test
Set your ports and config in the properties.json file (if needed)
 
### Launch the tests: 

Smoke tests to validate the access and up&running enviroment

´´´ 
 behave tests/ --tags=ft-smoke
´´´

Demo tag to launch a basic happy path flows that creates a services, subservices, buttons and four kinds of interaction with the platform

´´´
 behave tests/ --tags=ft-demo
´´´






if 


### Enjoy :)
