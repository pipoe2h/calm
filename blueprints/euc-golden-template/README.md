# Automating Citrix Golden Templates with Calm and MDT

---
**NOTE**

* Tested with PC 2020.9, Calm 3.1.0, MDT 6.3.8456.1000 and Citrix Studio 7.14.1.43

---

## Requirements

* Have ready Nutanix Calm with an AHV entitled project

* An existing MDT deployment with a working Deployment Share and Task Sequence that includes CVDA installation

* An existing MDT bootstrap ISO image for Calm to boot the VM with it. Example of a `bootstrap.ini`:

    ```ini
    [Settings]
    Priority=Default

    [Default]
    DeployRoot=\\YOUR_MDT_HOST\YOUR_MDT_SHARED_FOLDER$
    UserDomain=YOUR_DOMAIN
    UserID=YOUR_DOMAIN_SERVICE_ACCOUNT
    UserPassword=YOUR_DOMAIN_SERVICE_ACCOUNT_PASSWORD

    SkipBDDWelcome=YES
    ```
