# GUI_tester_production


**Overview**

The purpose of this page is to describe the SW design of the Kazuar Production tester UX/UI with an emphasis of user name and password to process login 

authentication.

Kazuar Production tester is a graphical application that runs

options of burning and automation test for each PC system including save data into database (for each burn steps SI/SO/AT and automation test)

After switching to application mode the user will get permission to do burning of SI/SO/AT include automation and screen panel test.

 

**System and Architecture Requirements**

Functional Requirements:

* Burning of secure input

* Burning of anti-tamper

* Burning of secure output

* Flashing ISO for each UUT PC

* Automation test for each UUT PC

* Screen panel test for each UUT PC

* save of all the (data) serial numbers (Si / So (SOM) / PC (HW information)) into databases


**System Requirements ( equipment):**

* USB type C  

* USB 2.0

* J-Link ( SEGGER)

* AT MCU to JTAG cable

* BARCODE QR

**Use Cases:**

When the user enters the wrong password we inform him by message on the login screen.

When the user authenticates he get permission to do all the burning processes except access to the database.

access to the database will be given only to kazuar users by knowing the password

 

**Architecture:**

The Kazuar Production tester GUI is a Python Tkinter-based GUI application that displays a login dialog in full-screen mode.

The tester is a closed/private PC without connection to the network database and/or out server which are used in endpoint files and automation workspace 

inside.

The database which we used is sqlite3 (internal python database), which saves all the serial numbers (Si / So (SOM) / PC (HW information)) and all the automation tests.

 

**Flow (block diagram):**

**login screen:**

![image](https://user-images.githubusercontent.com/66781442/208664470-aa571f81-83b9-4b4d-971e-31ae156ad447.png)


**Secure Input:**

![image](https://user-images.githubusercontent.com/66781442/208664582-cbef7727-3c9d-4947-be77-8502ffa9f76b.png)


**Secure Output:**

![image](https://user-images.githubusercontent.com/66781442/208664691-88155813-9357-42ef-a4c6-b43533c79731.png)


**Anti-tamper:**

![image](https://user-images.githubusercontent.com/66781442/208664803-c27c7051-0b88-4532-bd88-240f4ef82a91.png)










