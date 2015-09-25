# bbutton-tests
BButton project Tests repository 


## How to launch the tests

### Requirements

To the tests need python 2.7 and the required libs listed in the requirements file

```
pip install -r requirements.txt
```  

### Config your environment 

In the instances.json file set your ips of the instances under test
Set your ports and config in the properties.json file (if needed)
 
### Launch the tests: 
The tests are tagged to be launched.


Smoke tests are under the tag "ft-smoke" 
 It validate the access and up&running enviroment

``` 
 behave tests/ --tags=ft-smoke
```

Happy path tests are under the tag "ft-happypath" 
 It validate the basic happy path flows that includes the services, subservices, buttons provision and four kinds of flows interaction with the platform

```
 behave tests/ --tags=ft-happypath
```

Once the buttons are created if you want to relaunch just the flows (with the same values or not)
```
 behave tests/ --tags=hp-buttons-flows
```
or just a type os sync flow

```
 behave tests/ --tags=hp-buttons-async-flow
```
```
 behave tests/ --tags=hp-buttons-sync-flow
```










### Enjoy :)
