# MediTech

MediTech is a comprehensive healthcare management system designed to streamline various administrative tasks within healthcare facilities. Leveraging Python, MongoDB, and Tkinter, it offers a robust set of features to enhance efficiency and effectiveness in managing patient information, appointments, medical records, billing, and reporting.

## Key Features:
- **Secure Login:** Ensure authorized access to the system with secure authentication.
- **Patient Management:** Easily add, update, and remove patient records, facilitating efficient patient administration.
- **Doctor and Staff Management:** Manage doctor and staff records seamlessly, ensuring adequate staffing levels.
- **Appointment Scheduling:** Schedule appointments with specific doctors and patients, optimizing healthcare delivery.
- **Medical Record Keeping:** Maintain detailed medical records associated with patients and doctors for comprehensive care.
- **Invoicing:** Automatically generate invoices based on services rendered to patients, simplifying billing processes.
- **Payment Tracking:** Track payment status for invoices, ensuring timely payments and financial transparency.
- **Report Generation:** Generate detailed reports on sales and appointments for informed decision-making and analysis.

## How It Works:
MediTech utilizes a modular architecture to facilitate maintainability and scalability. The system's graphical user interface, built with Tkinter, provides an intuitive user experience with tabbed navigation for easy access to various functionalities. MongoDB, a NoSQL database, offers scalability and flexibility in managing healthcare data efficiently.

## Detailed Description:
MediTech's modular design allows for seamless integration of key healthcare management modules, including patient management, appointment scheduling, medical record keeping, invoicing, and reporting. Each module is carefully designed to address specific aspects of healthcare administration, ensuring comprehensive coverage of administrative tasks.
The system's user-friendly interface enables healthcare providers and administrators to navigate between modules effortlessly, facilitating smooth workflow and enhancing productivity. With secure authentication, authorized users can access patient records, schedule appointments, generate invoices, and track payments with confidence.
MediTech's robust reporting capabilities empower healthcare facilities to analyze key metrics, identify trends, and make informed decisions to optimize operations and improve patient care. By centralizing healthcare data and automating administrative tasks, MediTech streamlines workflow, reduces errors, and enhances overall efficiency in healthcare management.

## Requirements:
- ## Requirements:
- [VS Code](https://code.visualstudio.com/download) with Python and MongoDB extensions installed
- [MongoDB Compass](https://www.mongodb.com/try/download/compass)
- Required Python Packages (install with commands):
```python
pip install tk
pip install pymongo
pip install tkcalendar
pip install Pillow
```

## Steps For the Application to Run:
1. Extract the zip file.
2. Open the `Code.py` file in VS Code.
3. Connect the MongoDB Extension to the MongoDB application.
4. Import all the MediTech System JSON files into the MongoDB application as test data.
5. Change the path of the logo with the real path of `MediTech-Logo.png`. Find the following line in the `Code.py` file and modify it accordingly:logo_path = "C:/Users/Desktop/MediTech/MediTech-Logo.png"
6. MediTech will be ready to work seamlessly.
