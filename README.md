# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* To caculate the monthly bills of the outstanding instances spinned up for the Teraki members in Tools Account

### How do I get set up? ###

* Using AWS Cost Explorer API and EC2 Resource API, we query the costs incurred by all AWS resources in the Tools account having tags: Name 
* The script will generate a tabular format of the costs incurred by instances and send a email to Manager
