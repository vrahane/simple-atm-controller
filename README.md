# simple-atm-controller
Simple ATM controller

CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Test Cases
 * To Do
 * Requirements
 * Maintainers


INTRODUCTION
------------

 * This is a basic implementation of an ATM controller

 * To submit bug reports and feature suggestions, or to track changes visit:
   https://github.com/vrahane/simple-atm-controller


TEST CASES
----------

 * This code was tested using built in test cases, the output for for the particular test case should be as follows:

```
  $python atm_controller.py
   TEST CASE 0: Empty ATM: PASS
   TEST CASE 1: Valid ATM: PASS
   TEST CASE 2: Overdraft handling: PASS
   TEST CASE 3: Incorrect Pin Number: PASS
   TEST CASE 4: Incorrect Account Number: PASS
   TEST CASE 5: Cash bin overflow: PASS
   TEST CASE 6: Exit: PASS
```

 * The test cases are defined in the code, so, if running any new test case is required, please make changes to the code accordingly


TO DO
-----

 * Add some more test cases
 * Add distributed database support for scaling
 * Make it multi-threaded to take care of any race conditions


REQUIREMENTS
------------

 * This module runs on Python 3.7.2 and higher. 


MAINTAINERS
-----------

 * Vipul Rahane - vrahane@gmail.com 
