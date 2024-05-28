from tkinter import ttk
import tkinter as tk  # Import the Tkinter module for creating GUI
from tkinter import messagebox  # Import messagebox from Tkinter for displaying messages
from pymongo import MongoClient  # Import MongoClient from pymongo for MongoDB interaction
from datetime import datetime  # Import datetime module for date and time handling
import bson  # Import bson module for Binary JSON data handling
from tkcalendar import Calendar
from PIL import Image, ImageTk


# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['meditech_system']
users_collection = db['users']  # Collection to store user credentials
patients_collection = db['patients']
doctors_collection = db['doctors']
appointments_collection = db['appointments']
invoices_collection = db['invoices']
staff_collection = db["staff"] 
medical_records_collection=db["Medical Records"]


def create_login_window():
    login_window = tk.Tk()
    login_window.title("MediTech System - Login")
    
    label_username = tk.Label(login_window, text="Username:")
    label_username.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    
    entry_username = tk.Entry(login_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)
    
    label_password = tk.Label(login_window, text="Password:")
    label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    
    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)
    
    button_login = tk.Button(login_window, text="Login", command=lambda: authenticate_user(login_window, entry_username.get(), entry_password.get()))
    button_login.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    login_window.mainloop()
def authenticate_user(login_window, username, password):
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        create_main_window()
    else:
        messagebox.showerror("Error", "Invalid username or password")
def logout(main_window):
    main_window.destroy()
    create_login_window()


# Function to resize the logo image
def resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)
def display_dashboard(dashboard_tab):
    # Clear existing content in the dashboard tab
    for widget in dashboard_tab.winfo_children():
        widget.destroy()

    # Fetch key metrics from the database
    total_patients = patients_collection.count_documents({})
    total_appointments = appointments_collection.count_documents({})
    pending_bills = invoices_collection.count_documents({"status": "Pending"})

    # Display key metrics
    label_title = tk.Label(dashboard_tab, text="Dashboard", font=("Helvetica", 16, "bold"))
    label_title.pack(pady=10)

    label_patients = tk.Label(dashboard_tab, text=f"Total Patients: {total_patients}")
    label_patients.pack()

    label_appointments = tk.Label(dashboard_tab, text=f"Total Appointments: {total_appointments}")
    label_appointments.pack()

    label_bills = tk.Label(dashboard_tab, text=f"Pending Bills: {pending_bills}")
    label_bills.pack()

    # Load and resize the logo image
    logo_path = "C:\\Users\\ammok\\Desktop\\Hacking\\Projects\\MediTech-Python & Mongodb\\MediTech-Logo.png"
    try:
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((200, 200), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load logo image: {e}")
        return

    # Create a label to display the logo image
    label_logo = tk.Label(dashboard_tab, image=logo_image)
    label_logo.image = logo_image  # Keep a reference to prevent garbage collection
    label_logo.place(x=10, y=10)  # Adjust the x and y coordinates as needed



# Patient Management
def patient_management_window(patient_management_tab):
    # Clear existing content in the patient management tab
    for widget in patient_management_tab.winfo_children():
        widget.destroy()

    # Title label
    label_title = tk.Label(patient_management_tab, text="Patient Management", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=3, pady=10)

    # Buttons
    button_add_patient = tk.Button(patient_management_tab, text="Add Patient", command=add_patient_window)
    button_add_patient.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    button_view_patient = tk.Button(patient_management_tab, text="View Patient", command=view_patient_window)
    button_view_patient.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    button_update_patient = tk.Button(patient_management_tab, text="Update Patient", command=update_patient_window)
    button_update_patient.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    button_delete_patient = tk.Button(patient_management_tab, text="Delete Patient", command=delete_patient_window)
    button_delete_patient.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    button_search_patient = tk.Button(patient_management_tab, text="Search Patient", command=search_patient_window)
    button_search_patient.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    button_view_all_patients = tk.Button(patient_management_tab, text="View All Patients", command=view_all_patients_window)
    button_view_all_patients.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

    # Adjust column weights
    patient_management_tab.columnconfigure(0, weight=1)
    patient_management_tab.columnconfigure(1, weight=1)
    patient_management_tab.columnconfigure(2, weight=1)
def add_patient_window():
    add_patient_window = tk.Toplevel()
    add_patient_window.title("Add New Patient")

    label_title = tk.Label(add_patient_window, text="Add New Patient", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_name = tk.Label(add_patient_window, text="Name:")
    label_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_age = tk.Label(add_patient_window, text="Age:")
    label_age.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_gender = tk.Label(add_patient_window, text="Gender:")
    label_gender.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    label_address = tk.Label(add_patient_window, text="Address:")
    label_address.grid(row=4, column=0, padx=10, pady=5, sticky="e")

    entry_name = tk.Entry(add_patient_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5)
    entry_age = tk.Entry(add_patient_window)
    entry_age.grid(row=2, column=1, padx=10, pady=5)
    entry_gender = tk.Entry(add_patient_window)
    entry_gender.grid(row=3, column=1, padx=10, pady=5)
    entry_address = tk.Entry(add_patient_window)
    entry_address.grid(row=4, column=1, padx=10, pady=5)

    button_submit = tk.Button(add_patient_window, text="Submit", command=lambda: add_patient(entry_name.get(), entry_age.get(), entry_gender.get(), entry_address.get()))
    button_submit.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
def add_patient(name, age, gender, address):
    patient_data = {
        "name": name,
        "age": int(age),
        "gender": gender,
        "address": address
    }
    patients_collection.insert_one(patient_data)
    messagebox.showinfo("Success", "Patient added successfully!")
def view_patient_window():
    view_patient_window = tk.Toplevel()
    view_patient_window.title("View Patient")

    label_title = tk.Label(view_patient_window, text="View Patient", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_patient_id = tk.Label(view_patient_window, text="Patient ID:")
    label_patient_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_patient_id = tk.Entry(view_patient_window)
    entry_patient_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(view_patient_window, text="Submit", command=lambda: view_patient(entry_patient_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def view_patient(patient_id):
    patient = patients_collection.find_one({"_id": bson.ObjectId(patient_id)})
    if patient:
        messagebox.showinfo("Patient Details", f"Name: {patient['name']}\nAge: {patient['age']}\nGender: {patient['gender']}\nAddress: {patient['address']}")
    else:
        messagebox.showerror("Error", "Patient not found")
def update_patient_window():
    update_patient_window = tk.Toplevel()
    update_patient_window.title("Update Patient")

    label_title = tk.Label(update_patient_window, text="Update Patient", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_patient_id = tk.Label(update_patient_window, text="Patient ID:")
    label_patient_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_patient_id = tk.Entry(update_patient_window)
    entry_patient_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_patient_window, text="Submit", command=lambda: get_patient_data_to_update(entry_patient_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def get_patient_data_to_update(patient_id):
    update_patient_data_window = tk.Toplevel()
    update_patient_data_window.title("Update Patient Data")

    label_title = tk.Label(update_patient_data_window, text="Update Patient Data", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_name = tk.Label(update_patient_data_window, text="Name:")
    label_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_age = tk.Label(update_patient_data_window, text="Age:")
    label_age.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_gender = tk.Label(update_patient_data_window, text="Gender:")
    label_gender.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    label_address = tk.Label(update_patient_data_window, text="Address:")
    label_address.grid(row=4, column=0, padx=10, pady=5, sticky="e")

    entry_name = tk.Entry(update_patient_data_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5)
    entry_age = tk.Entry(update_patient_data_window)
    entry_age.grid(row=2, column=1, padx=10, pady=5)
    entry_gender = tk.Entry(update_patient_data_window)
    entry_gender.grid(row=3, column=1, padx=10, pady=5)
    entry_address = tk.Entry(update_patient_data_window)
    entry_address.grid(row=4, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_patient_data_window, text="Update", command=lambda: update_patient(patient_id, {
        "name": entry_name.get(),
        "age": int(entry_age.get()),
        "gender": entry_gender.get(),
        "address": entry_address.get()
    }))
    button_submit.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
def update_patient(patient_id, updated_data):
    patients_collection.update_one({"_id": bson.ObjectId(patient_id)}, {"$set": updated_data})
    messagebox.showinfo("Success", "Patient record updated successfully!")
def delete_patient_window():
    delete_patient_window = tk.Toplevel()
    delete_patient_window.title("Delete Patient")

    label_title = tk.Label(delete_patient_window, text="Delete Patient", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_patient_id = tk.Label(delete_patient_window, text="Patient ID:")
    label_patient_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_patient_id = tk.Entry(delete_patient_window)
    entry_patient_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(delete_patient_window, text="Delete", command=lambda: delete_patient(entry_patient_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def delete_patient(patient_id):
    patients_collection.delete_one({"_id": bson.ObjectId(patient_id)})
    messagebox.showinfo("Success", "Patient record deleted successfully!")
def search_patient_window():
    search_patient_window = tk.Toplevel()
    search_patient_window.title("Search Patient")

    label_title = tk.Label(search_patient_window, text="Search Patient", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_keyword = tk.Label(search_patient_window, text="Keyword:")
    label_keyword.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_keyword = tk.Entry(search_patient_window)
    entry_keyword.grid(row=1, column=1, padx=10, pady=5)

    button_search = tk.Button(search_patient_window, text="Search", command=lambda: search_patient(entry_keyword.get()))
    button_search.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def search_patient(keyword):
    search_results_window = tk.Toplevel()
    search_results_window.title("Search Results")
    # Query the database for patient records matching the keyword
    results = patients_collection.find({
        "$or": [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"age": {"$regex": keyword, "$options": "i"}},
            {"gender": {"$regex": keyword, "$options": "i"}},
            {"address": {"$regex": keyword, "$options": "i"}}
        ]
    })
    # Display search results in a treeview widget
    tree = ttk.Treeview(search_results_window)
    tree["columns"] = ("name", "age", "gender", "address")
    tree.heading("#0", text="ID")
    tree.heading("name", text="Name")
    tree.heading("age", text="Age")
    tree.heading("gender", text="Gender")
    tree.heading("address", text="Address")
    for result in results:
        tree.insert("", "end", text=result["_id"], values=(result["name"], result["age"], result["gender"], result["address"]))
    tree.pack()
def view_all_patients_window():
    def sort_by_name():
        results = patients_collection.find().sort("name")
        populate_treeview(results)

    def sort_by_age():
        results = patients_collection.find().sort("age")
        populate_treeview(results)

    def sort_by_gender():
        results = patients_collection.find().sort("gender")
        populate_treeview(results)

    def populate_treeview(results):
        for row in tree.get_children():
            tree.delete(row)
        for result in results:
            tree.insert("", "end", text=result["_id"], values=(result["name"], result["age"], result["gender"], result["address"]))

    view_all_patients_window = tk.Toplevel()
    view_all_patients_window.title("View All Patients")

    # Sort buttons
    button_sort_name = tk.Button(view_all_patients_window, text="Sort by Name (A-Z)", command=sort_by_name)
    button_sort_name.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="ew")

    button_sort_age = tk.Button(view_all_patients_window, text="Sort by Age (Ascending)", command=sort_by_age)
    button_sort_age.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    button_sort_gender = tk.Button(view_all_patients_window, text="Sort by Gender", command=sort_by_gender)
    button_sort_gender.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="ew")

    # Treeview
    tree = ttk.Treeview(view_all_patients_window)
    tree["columns"] = ("name", "age", "gender", "address")
    tree.heading("#0", text="ID")
    tree.heading("name", text="Name")
    tree.heading("age", text="Age")
    tree.heading("gender", text="Gender")
    tree.heading("address", text="Address")
    results = patients_collection.find()
    populate_treeview(results)
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

    view_all_patients_window.grid_rowconfigure(1, weight=1)
    view_all_patients_window.grid_columnconfigure(0, weight=1)



# Doctor Management
def doctor_management_window(doctor_management_tab):
    # Clear existing content in the doctor management tab
    for widget in doctor_management_tab.winfo_children():
        widget.destroy()

    # Title label
    label_title = tk.Label(doctor_management_tab, text="Doctor Management", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=3, pady=10)

    # Buttons
    button_add_doctor = tk.Button(doctor_management_tab, text="Add Doctor", command=add_doctor_window)
    button_add_doctor.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    button_view_doctor = tk.Button(doctor_management_tab, text="View Doctor", command=view_doctor_window)
    button_view_doctor.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    button_update_doctor = tk.Button(doctor_management_tab, text="Update Doctor", command=update_doctor_window)
    button_update_doctor.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    button_delete_doctor = tk.Button(doctor_management_tab, text="Delete Doctor", command=delete_doctor_window)
    button_delete_doctor.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    button_search_doctor = tk.Button(doctor_management_tab, text="Search Doctor", command=search_doctor_window)
    button_search_doctor.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    button_view_all_doctors = tk.Button(doctor_management_tab, text="View All Doctors", command=view_all_doctors_window)
    button_view_all_doctors.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

    # Adjust column weights for uniform button width
    doctor_management_tab.columnconfigure((0, 1, 2), weight=1)
def add_doctor_window():
    add_doctor_window = tk.Toplevel()
    add_doctor_window.title("Add New Doctor")

    label_title = tk.Label(add_doctor_window, text="Add New Doctor", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_name = tk.Label(add_doctor_window, text="Name:")
    label_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_specialty = tk.Label(add_doctor_window, text="Specialty:")
    label_specialty.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_contact = tk.Label(add_doctor_window, text="Contact:")
    label_contact.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    entry_name = tk.Entry(add_doctor_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5)
    entry_specialty = tk.Entry(add_doctor_window)
    entry_specialty.grid(row=2, column=1, padx=10, pady=5)
    entry_contact = tk.Entry(add_doctor_window)
    entry_contact.grid(row=3, column=1, padx=10, pady=5)

    button_submit = tk.Button(add_doctor_window, text="Submit", command=lambda: add_doctor(entry_name.get(), entry_specialty.get(), entry_contact.get()))
    button_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
def add_doctor(name, specialty, contact):
    doctor_data = {
        "name": name,
        "specialty": specialty,
        "contact": contact
    }
    doctors_collection.insert_one(doctor_data)
    messagebox.showinfo("Success", "Doctor added successfully!")
def view_doctor_window():
    view_doctor_window = tk.Toplevel()
    view_doctor_window.title("View Doctor")

    label_title = tk.Label(view_doctor_window, text="View Doctor", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_doctor_id = tk.Label(view_doctor_window, text="Doctor ID:")
    label_doctor_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_doctor_id = tk.Entry(view_doctor_window)
    entry_doctor_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(view_doctor_window, text="Submit", command=lambda: view_doctor(entry_doctor_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def view_doctor(doctor_id):
    doctor = doctors_collection.find_one({"_id": bson.ObjectId(doctor_id)})
    if doctor:
        messagebox.showinfo("Doctor Details", f"Name: {doctor['name']}\nSpecialty: {doctor['specialty']}\nContact: {doctor['contact']}")
    else:
        messagebox.showerror("Error", "Doctor not found")
def update_doctor_window():
    update_doctor_window = tk.Toplevel()
    update_doctor_window.title("Update Doctor")

    label_title = tk.Label(update_doctor_window, text="Update Doctor", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_doctor_id = tk.Label(update_doctor_window, text="Doctor ID:")
    label_doctor_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_doctor_id = tk.Entry(update_doctor_window)
    entry_doctor_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_doctor_window, text="Submit", command=lambda: get_doctor_data_to_update(entry_doctor_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def get_doctor_data_to_update(doctor_id):
    update_doctor_data_window = tk.Toplevel()
    update_doctor_data_window.title("Update Doctor Data")

    label_title = tk.Label(update_doctor_data_window, text="Update Doctor Data", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_name = tk.Label(update_doctor_data_window, text="Name:")
    label_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_specialty = tk.Label(update_doctor_data_window, text="Specialty:")
    label_specialty.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_contact = tk.Label(update_doctor_data_window, text="Contact:")
    label_contact.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    entry_name = tk.Entry(update_doctor_data_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5)
    entry_specialty = tk.Entry(update_doctor_data_window)
    entry_specialty.grid(row=2, column=1, padx=10, pady=5)
    entry_contact = tk.Entry(update_doctor_data_window)
    entry_contact.grid(row=3, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_doctor_data_window, text="Update", command=lambda: update_doctor(doctor_id, {
        "name": entry_name.get(),
        "specialty": entry_specialty.get(),
        "contact": entry_contact.get()
    }))
    button_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
def update_doctor(doctor_id, updated_data):
    doctors_collection.update_one({"_id": bson.ObjectId(doctor_id)}, {"$set": updated_data})
    messagebox.showinfo("Success", "Doctor profile updated successfully!")
def delete_doctor_window():
    delete_doctor_window = tk.Toplevel()
    delete_doctor_window.title("Delete Doctor")

    label_title = tk.Label(delete_doctor_window, text="Delete Doctor", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_doctor_id = tk.Label(delete_doctor_window, text="Doctor ID:")
    label_doctor_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_doctor_id = tk.Entry(delete_doctor_window)
    entry_doctor_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(delete_doctor_window, text="Delete", command=lambda: delete_doctor(entry_doctor_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def delete_doctor(doctor_id):
    doctors_collection.delete_one({"_id": bson.ObjectId(doctor_id)})
    messagebox.showinfo("Success", "Doctor profile deleted successfully!")
def search_doctor_window():
    search_doctor_window = tk.Toplevel()
    search_doctor_window.title("Search Doctor")

    label_title = tk.Label(search_doctor_window, text="Search Doctor", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_keyword = tk.Label(search_doctor_window, text="Keyword:")
    label_keyword.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_keyword = tk.Entry(search_doctor_window)
    entry_keyword.grid(row=1, column=1, padx=10, pady=5)

    button_search = tk.Button(search_doctor_window, text="Search", command=lambda: search_doctor(entry_keyword.get()))
    button_search.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def search_doctor(keyword):
    search_results_window = tk.Toplevel()
    search_results_window.title("Search Results")
    # Query the database for doctor records matching the keyword
    results = doctors_collection.find({
        "$or": [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"specialty": {"$regex": keyword, "$options": "i"}},
            {"contact": {"$regex": keyword, "$options": "i"}}
        ]
    })
    # Display search results in a treeview widget
    tree = ttk.Treeview(search_results_window)
    tree["columns"] = ("name", "specialty", "contact")
    tree.heading("#0", text="ID")
    tree.heading("name", text="Name")
    tree.heading("specialty", text="Specialty")
    tree.heading("contact", text="Contact")
    for result in results:
        tree.insert("", "end", text=result["_id"], values=(result["name"], result["specialty"], result["contact"]))
    tree.pack()
def view_all_doctors_window():
    def sort_by_name():
        results = doctors_collection.find().sort("name")
        populate_treeview(results)

    def sort_by_specialty():
        results = doctors_collection.find().sort("specialty")
        populate_treeview(results)

    def sort_by_contact():
        results = doctors_collection.find().sort("contact")
        populate_treeview(results)

    def populate_treeview(results):
        for row in tree.get_children():
            tree.delete(row)
        for result in results:
            tree.insert("", "end", text=result["_id"], values=(result["name"], result["specialty"], result["contact"]))

    view_all_doctors_window = tk.Toplevel()
    view_all_doctors_window.title("View All Doctors")

    # Sort buttons
    button_sort_name = tk.Button(view_all_doctors_window, text="Sort by Name (A-Z)", command=sort_by_name)
    button_sort_name.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="ew")

    button_sort_specialty = tk.Button(view_all_doctors_window, text="Sort by Specialty", command=sort_by_specialty)
    button_sort_specialty.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    button_sort_contact = tk.Button(view_all_doctors_window, text="Sort by Contact", command=sort_by_contact)
    button_sort_contact.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="ew")

    # Treeview
    tree = ttk.Treeview(view_all_doctors_window)
    tree["columns"] = ("name", "specialty", "contact")
    tree.heading("#0", text="ID")
    tree.heading("name", text="Name")
    tree.heading("specialty", text="Specialty")
    tree.heading("contact", text="Contact")
    results = doctors_collection.find()
    populate_treeview(results)
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

    view_all_doctors_window.grid_rowconfigure(1, weight=1)
    view_all_doctors_window.grid_columnconfigure(0, weight=1)


#Staff Management
def staff_management_window(staff_management_tab):
    # Clear existing content in the staff management tab
    for widget in staff_management_tab.winfo_children():
        widget.destroy()
    
    # Title label
    label_title = tk.Label(staff_management_tab, text="Staff Management", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=3, pady=10)

    # Buttons
    button_add_staff = tk.Button(staff_management_tab, text="Add Staff", command=add_staff_window)
    button_add_staff.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    button_view_staff = tk.Button(staff_management_tab, text="View Staff", command=view_staff_window)
    button_view_staff.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    button_update_staff = tk.Button(staff_management_tab, text="Update Staff", command=update_staff_window)
    button_update_staff.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    button_delete_staff = tk.Button(staff_management_tab, text="Delete Staff", command=delete_staff_window)
    button_delete_staff.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    button_search_staff = tk.Button(staff_management_tab, text="Search Staff", command=search_staff_window)
    button_search_staff.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    button_view_all_staff = tk.Button(staff_management_tab, text="View All Staff", command=view_all_staff_window)
    button_view_all_staff.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

    # Adjust column weights for uniform button width
    staff_management_tab.columnconfigure((0, 1, 2), weight=1)
def add_staff_window():
    add_staff_window = tk.Toplevel()
    add_staff_window.title("Add New Staff")

    label_title = tk.Label(add_staff_window, text="Add New Staff", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_name = tk.Label(add_staff_window, text="Name:")
    label_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_role = tk.Label(add_staff_window, text="Role:")
    label_role.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_contact = tk.Label(add_staff_window, text="Contact:")
    label_contact.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    entry_name = tk.Entry(add_staff_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5)
    entry_role = tk.Entry(add_staff_window)
    entry_role.grid(row=2, column=1, padx=10, pady=5)
    entry_contact = tk.Entry(add_staff_window)
    entry_contact.grid(row=3, column=1, padx=10, pady=5)

    button_submit = tk.Button(add_staff_window, text="Submit", command=lambda: add_staff(entry_name.get(), entry_role.get(), entry_contact.get()))
    button_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
def add_staff(name, role, contact):
    staff_data = {
        "name": name,
        "role": role,
        "contact": contact
    }
    staff_collection.insert_one(staff_data)
    messagebox.showinfo("Success", "Staff added successfully!")
def view_staff_window():
    view_staff_window = tk.Toplevel()
    view_staff_window.title("View Staff")

    label_title = tk.Label(view_staff_window, text="View Staff", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_staff_id = tk.Label(view_staff_window, text="Staff ID:")
    label_staff_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_staff_id = tk.Entry(view_staff_window)
    entry_staff_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(view_staff_window, text="Submit", command=lambda: view_staff(entry_staff_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def view_staff(staff_id):
    staff = staff_collection.find_one({"_id": bson.ObjectId(staff_id)})
    if staff:
        messagebox.showinfo("Staff Details", f"Name: {staff['name']}\nRole: {staff['role']}\nContact: {staff['contact']}")
    else:
        messagebox.showerror("Error", "Staff not found")
def update_staff_window():
    update_staff_window = tk.Toplevel()
    update_staff_window.title("Update Staff")

    label_title = tk.Label(update_staff_window, text="Update Staff", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_staff_id = tk.Label(update_staff_window, text="Staff ID:")
    label_staff_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_staff_id = tk.Entry(update_staff_window)
    entry_staff_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_staff_window, text="Submit", command=lambda: get_staff_data_to_update(entry_staff_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def get_staff_data_to_update(staff_id):
    update_staff_data_window = tk.Toplevel()
    update_staff_data_window.title("Update Staff Data")

    label_title = tk.Label(update_staff_data_window, text="Update Staff Data", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_name = tk.Label(update_staff_data_window, text="Name:")
    label_name.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_role = tk.Label(update_staff_data_window, text="Role:")
    label_role.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_contact = tk.Label(update_staff_data_window, text="Contact:")
    label_contact.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    staff = staff_collection.find_one({"_id": bson.ObjectId(staff_id)})
    if staff:
        entry_name = tk.Entry(update_staff_data_window)
        entry_name.insert(tk.END, staff["name"])
        entry_name.grid(row=1, column=1, padx=10, pady=5)
        entry_role = tk.Entry(update_staff_data_window)
        entry_role.insert(tk.END, staff["role"])
        entry_role.grid(row=2, column=1, padx=10, pady=5)
        entry_contact = tk.Entry(update_staff_data_window)
        entry_contact.insert(tk.END, staff["contact"])
        entry_contact.grid(row=3, column=1, padx=10, pady=5)

        button_submit = tk.Button(update_staff_data_window, text="Submit", command=lambda: update_staff(staff_id, entry_name.get(), entry_role.get(), entry_contact.get()))
        button_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    else:
        messagebox.showerror("Error", "Staff not found")
def update_staff(staff_id, name, role, contact):
    staff_data = {
        "name": name,
        "role": role,
        "contact": contact
    }
    staff_collection.update_one({"_id": bson.ObjectId(staff_id)}, {"$set": staff_data})
    messagebox.showinfo("Success", "Staff updated successfully!")
def delete_staff_window():
    delete_staff_window = tk.Toplevel()
    delete_staff_window.title("Delete Staff")

    label_title = tk.Label(delete_staff_window, text="Delete Staff", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_staff_id = tk.Label(delete_staff_window, text="Staff ID:")
    label_staff_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_staff_id = tk.Entry(delete_staff_window)
    entry_staff_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(delete_staff_window, text="Submit", command=lambda: delete_staff(entry_staff_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def delete_staff(staff_id):
    result = staff_collection.delete_one({"_id": bson.ObjectId(staff_id)})
    if result.deleted_count == 1:
        messagebox.showinfo("Success", "Staff deleted successfully!")
    else:
        messagebox.showerror("Error", "Staff not found")
def search_staff_window():
    search_staff_window = tk.Toplevel()
    search_staff_window.title("Search Staff")

    label_title = tk.Label(search_staff_window, text="Search Staff", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_keyword = tk.Label(search_staff_window, text="Keyword:")
    label_keyword.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_keyword = tk.Entry(search_staff_window)
    entry_keyword.grid(row=1, column=1, padx=10, pady=5)

    button_search = tk.Button(search_staff_window, text="Search", command=lambda: search_staff(entry_keyword.get()))
    button_search.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def search_staff(keyword):
    search_results_window = tk.Toplevel()
    search_results_window.title("Search Results")

    # Query the database for staff records matching the keyword
    results = staff_collection.find({
        "$or": [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"role": {"$regex": keyword, "$options": "i"}},
            {"contact": {"$regex": keyword, "$options": "i"}}
        ]
    })

    # Display search results in a treeview widget
    tree = ttk.Treeview(search_results_window)
    tree["columns"] = ("name", "role", "contact")
    tree.heading("#0", text="ID")
    tree.heading("name", text="Name")
    tree.heading("role", text="Role")
    tree.heading("contact", text="Contact")

    for result in results:
        tree.insert("", "end", text=result["_id"], values=(result["name"], result["role"], result["contact"]))

    tree.pack()
def view_all_staff_window():
    def sort_by_name():
        results = staff_collection.find().sort("name")
        populate_treeview(results)

    def sort_by_role():
        results = staff_collection.find().sort("role")
        populate_treeview(results)

    def sort_by_contact():
        results = staff_collection.find().sort("contact")
        populate_treeview(results)

    def populate_treeview(results):
        for row in tree.get_children():
            tree.delete(row)
        for result in results:
            tree.insert("", "end", text=result["_id"], values=(result["name"], result["role"], result["contact"]))

    view_all_staff_window = tk.Toplevel()
    view_all_staff_window.title("View All Staff")

    # Sort buttons
    button_sort_name = tk.Button(view_all_staff_window, text="Sort by Name (A-Z)", command=sort_by_name)
    button_sort_name.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="ew")

    button_sort_role = tk.Button(view_all_staff_window, text="Sort by Role", command=sort_by_role)
    button_sort_role.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    button_sort_contact = tk.Button(view_all_staff_window, text="Sort by Contact", command=sort_by_contact)
    button_sort_contact.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="ew")

    # Treeview
    tree = ttk.Treeview(view_all_staff_window)
    tree["columns"] = ("name", "role", "contact")
    tree.heading("#0", text="ID")
    tree.heading("name", text="Name")
    tree.heading("role", text="Role")
    tree.heading("contact", text="Contact")

    results = staff_collection.find()
    populate_treeview(results)

    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
    view_all_staff_window.grid_rowconfigure(1, weight=1)
    view_all_staff_window.grid_columnconfigure(0, weight=1)



# Appointment Management
def appointment_management_window(appointment_management_tab):
    # Clear existing content in the appointment management tab
    for widget in appointment_management_tab.winfo_children():
        widget.destroy()
    
    # Title label
    label_title = tk.Label(appointment_management_tab, text="Appointment Management", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Buttons
    button_schedule_appointment = tk.Button(appointment_management_tab, text="Schedule Appointment", command=schedule_appointment_window)
    button_schedule_appointment.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    button_view_all_appointments = tk.Button(appointment_management_tab, text="View All Appointments", command=view_all_appointments_window)
    button_view_all_appointments.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    button_cancel_appointment = tk.Button(appointment_management_tab, text="Cancel Appointment", command=cancel_appointment_window)
    button_cancel_appointment.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    button_update_appointment = tk.Button(appointment_management_tab, text="Update Appointment", command=update_appointment_window)
    button_update_appointment.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Adjust column weights for uniform button width
    appointment_management_tab.columnconfigure((0, 1), weight=1)
def schedule_appointment_window():
    schedule_appointment_window = tk.Toplevel()
    schedule_appointment_window.title("Schedule New Appointment")

    # Labels
    label_title = tk.Label(schedule_appointment_window, text="Schedule New Appointment", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_patient_id = tk.Label(schedule_appointment_window, text="Patient ID:")
    label_patient_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_doctor_id = tk.Label(schedule_appointment_window, text="Doctor ID:")
    label_doctor_id.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    label_datetime = tk.Label(schedule_appointment_window, text="Date:")
    label_datetime.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    # Entry fields
    entry_patient_id = tk.Entry(schedule_appointment_window)
    entry_patient_id.grid(row=1, column=1, padx=10, pady=5)
    entry_doctor_id = tk.Entry(schedule_appointment_window)
    entry_doctor_id.grid(row=2, column=1, padx=10, pady=5)

    cal = Calendar(schedule_appointment_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.grid(row=3, column=1, padx=10, pady=5)

    # Submit button
    button_submit = tk.Button(schedule_appointment_window, text="Submit", command=lambda: schedule_appointment(entry_patient_id.get(), entry_doctor_id.get(), cal.get_date()))
    button_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
def schedule_appointment(patient_id, doctor_id, datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
        appointment_data = {
            "patient_id": bson.ObjectId(patient_id),
            "doctor_id": bson.ObjectId(doctor_id),
            "datetime": datetime_obj
        }
        appointments_collection.insert_one(appointment_data)
        messagebox.showinfo("Success", "Appointment scheduled successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to schedule appointment: {str(e)}")
def view_all_appointments_window():
    view_all_appointments_window = tk.Toplevel()
    view_all_appointments_window.title("View All Appointments")

    # Treeview
    tree = ttk.Treeview(view_all_appointments_window)
    tree["columns"] = ("patient_id", "doctor_id", "datetime")
    tree.heading("#0", text="ID")
    tree.heading("patient_id", text="Patient ID")
    tree.heading("doctor_id", text="Doctor ID")
    tree.heading("datetime", text="Date and Time")

    results = appointments_collection.find()
    for result in results:
        tree.insert("", "end", text=result["_id"], values=(result["patient_id"], result["doctor_id"], result["datetime"]))

    tree.pack()
def cancel_appointment_window():
    cancel_appointment_window = tk.Toplevel()
    cancel_appointment_window.title("Cancel Appointment")

    label_title = tk.Label(cancel_appointment_window, text="Cancel Appointment", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_appointment_id = tk.Label(cancel_appointment_window, text="Appointment ID:")
    label_appointment_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_appointment_id = tk.Entry(cancel_appointment_window)
    entry_appointment_id.grid(row=1, column=1, padx=10, pady=5)

    button_submit = tk.Button(cancel_appointment_window, text="Submit", command=lambda: cancel_appointment(entry_appointment_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def cancel_appointment(appointment_id):
    appointments_collection.delete_one({"_id": bson.ObjectId(appointment_id)})
    messagebox.showinfo("Success", "Appointment cancelled successfully!")
def update_appointment_window():
    update_appointment_window = tk.Toplevel()
    update_appointment_window.title("Update Appointment")

    label_title = tk.Label(update_appointment_window, text="Update Appointment", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_appointment_id = tk.Label(update_appointment_window, text="Appointment ID:")
    label_appointment_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_appointment_id = tk.Entry(update_appointment_window)
    entry_appointment_id.grid(row=1, column=1, padx=10, pady=5)

    label_new_datetime = tk.Label(update_appointment_window, text="New Date:")
    label_new_datetime.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    cal = Calendar(update_appointment_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.grid(row=2, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_appointment_window, text="Submit", command=lambda: update_appointment(entry_appointment_id.get(), cal.get_date()))
    button_submit.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
def update_appointment(appointment_id, new_date_str):
    try:
        # Adjust the date format to match the pattern retrieved from the Calendar widget
        new_datetime_str = f"{new_date_str} 00:00:00"  # Assuming time is not provided by the Calendar widget
        new_datetime_obj = datetime.strptime(new_datetime_str, "%Y-%m-%d %H:%M:%S")
        
        appointments_collection.update_one(
            {"_id": bson.ObjectId(appointment_id)},
            {"$set": {"datetime": new_datetime_obj}}
        )
        
        messagebox.showinfo("Success", "Appointment updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update appointment: {str(e)}")




# Medical Records Management
def medical_records_management_window(medical_records_management_tab):
    # Clear existing content in the medical records management tab
    for widget in medical_records_management_tab.winfo_children():
        widget.destroy()
    
    # Title label
    label_title = tk.Label(medical_records_management_tab, text="Medical Records Management", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Buttons
    button_add_medical_record = tk.Button(medical_records_management_tab, text="Add Medical Record", command=add_medical_record_window)
    button_add_medical_record.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    button_view_medical_record = tk.Button(medical_records_management_tab, text="View Medical Record", command=view_medical_record_window)
    button_view_medical_record.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    button_update_medical_record = tk.Button(medical_records_management_tab, text="Update Medical Record", command=update_medical_record_window)
    button_update_medical_record.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    button_delete_medical_record = tk.Button(medical_records_management_tab, text="Delete Medical Record", command=delete_medical_record_window)
    button_delete_medical_record.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Adjust column weights for uniform button width
    medical_records_management_tab.columnconfigure((0, 1), weight=1)
def add_medical_record_window():
    add_medical_record_window = tk.Toplevel()
    add_medical_record_window.title("Add Medical Record")

    # Labels
    label_title = tk.Label(add_medical_record_window, text="Add Medical Record", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_patient_id = tk.Label(add_medical_record_window, text="Patient ID:")
    label_patient_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Dropdown for selecting existing patient ID or registering a new patient
    patient_ids = [str(patient['_id']) for patient in patients_collection.find({}, {"_id": 1})]
    patient_ids.append("New Patient")  # Option to register a new patient
    patient_var = tk.StringVar()
    patient_dropdown = ttk.Combobox(add_medical_record_window, textvariable=patient_var, values=patient_ids)
    patient_dropdown.grid(row=1, column=1, padx=10, pady=5)

    def register_new_patient():
        # Function to register a new patient
        new_patient_window = tk.Toplevel()
        new_patient_window.title("Register New Patient")

        # Labels and entry fields for registering a new patient
        label_patient_name = tk.Label(new_patient_window, text="Patient Name:")
        label_patient_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_patient_name = tk.Entry(new_patient_window)
        entry_patient_name.grid(row=0, column=1, padx=10, pady=5)

        label_patient_age = tk.Label(new_patient_window, text="Age:")
        label_patient_age.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_patient_age = tk.Entry(new_patient_window)
        entry_patient_age.grid(row=1, column=1, padx=10, pady=5)

        label_patient_gender = tk.Label(new_patient_window, text="Gender:")
        label_patient_gender.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        gender_options = ["Male", "Female", "Other"]
        patient_gender_var = tk.StringVar()
        patient_gender_dropdown = ttk.Combobox(new_patient_window, textvariable=patient_gender_var, values=gender_options)
        patient_gender_dropdown.grid(row=2, column=1, padx=10, pady=5)

        label_patient_address = tk.Label(new_patient_window, text="Address:")
        label_patient_address.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_patient_address = tk.Entry(new_patient_window)
        entry_patient_address.grid(row=3, column=1, padx=10, pady=5)

        def save_patient_details():
            # Function to save the details of the new patient to the database
            patient_data = {
                "name": entry_patient_name.get(),
                "age": entry_patient_age.get(),
                "gender": patient_gender_var.get(),
                "address": entry_patient_address.get(),
            }
            patients_collection.insert_one(patient_data)
            messagebox.showinfo("Success", "Patient details saved successfully!")
            new_patient_window.destroy()  # Close the window after saving

        button_save_patient = tk.Button(new_patient_window, text="Save", command=save_patient_details)
        button_save_patient.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Button to register a new patient
    button_register_patient = tk.Button(add_medical_record_window, text="Register New Patient", command=register_new_patient)
    button_register_patient.grid(row=1, column=2, padx=10, pady=5)

    label_date = tk.Label(add_medical_record_window, text="Date:")
    label_date.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_date = tk.Entry(add_medical_record_window)
    entry_date.grid(row=2, column=1, padx=10, pady=5)

    label_doctor = tk.Label(add_medical_record_window, text="Doctor:")
    label_doctor.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    # Dropdown for selecting doctors
    doctor_names = [doctor['name'] for doctor in doctors_collection.find({}, {"_id": 0, "name": 1})]
    doctor_var = tk.StringVar()
    doctor_dropdown = ttk.Combobox(add_medical_record_window, textvariable=doctor_var, values=doctor_names)
    doctor_dropdown.grid(row=3, column=1, padx=10, pady=5)

    label_notes = tk.Label(add_medical_record_window, text="Notes:")
    label_notes.grid(row=4, column=0, padx=10, pady=5, sticky="e")

    # Text field for notes
    entry_notes = tk.Text(add_medical_record_window, height=5, width=30)
    entry_notes.grid(row=4, column=1, padx=10, pady=5)

    # Dropdown for selecting famous diseases
    label_disease = tk.Label(add_medical_record_window, text="Select Disease:")
    label_disease.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    diseases = ["Diabetes", "Heart Disease", "Asthma", "Cancer", "Hypertension", "Stroke","Skin Disease","Blood Pressure"]
    disease_var = tk.StringVar()
    disease_dropdown = ttk.Combobox(add_medical_record_window, textvariable=disease_var, values=diseases)
    disease_dropdown.grid(row=5, column=1, padx=10, pady=5)

    # Submit button
    button_submit = tk.Button(add_medical_record_window, text="Submit", command=lambda: add_medical_record(patient_var.get(), {
        "date": entry_date.get(),
        "doctor": doctor_var.get(),
        "notes": entry_notes.get("1.0", "end-1c"),  # Get text from the text field
        "disease": disease_var.get()
    }))
    button_submit.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Allow the text field for notes to expand dynamically
    entry_notes.config(wrap="word")
def add_medical_record(patient_id, medical_record_data):
    # Add medical record for patient
    medical_record_data["patient_id"] = bson.ObjectId(patient_id)
    medical_records_collection.insert_one(medical_record_data)
    messagebox.showinfo("Success", "Medical record added successfully!")
def view_medical_record_window():
    view_medical_record_window = tk.Toplevel()
    view_medical_record_window.title("View Medical Records")

    label_title = tk.Label(view_medical_record_window, text="View Medical Records", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Retrieve all medical records from the database
    medical_records = medical_records_collection.find()

    if medical_records:
        # Display the medical records in a text widget
        text_display = tk.Text(view_medical_record_window, height=20, width=80)
        text_display.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        for record in medical_records:
            text_display.insert(tk.END, f"Date: {record['date']}\nDoctor: {record['doctor']}\nNotes: {record['notes']}\nDisease: {record['disease']}\n\n")
    else:
        # If no records found, display a message
        label_no_records = tk.Label(view_medical_record_window, text="No medical records found.")
        label_no_records.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Close the window button
    button_close = tk.Button(view_medical_record_window, text="Close", command=view_medical_record_window.destroy)
    button_close.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Retrieve medical records for the specified patient
    medical_records = medical_records_collection.find({"patient_id": bson.ObjectId(patient_id)})
    
    # Display the medical records (for example, in a new window or a message box)
    if medical_records:
        for record in medical_records:
            messagebox.showinfo("Medical Record", f"Date: {record['date']}\nDoctor: {record['doctor']}\nNotes: {record['notes']}\nDisease: {record['disease']}")
    else:
        messagebox.showinfo("No Records", "No medical records found for the specified patient.")
def update_medical_record_window():
    update_medical_record_window = tk.Toplevel()
    update_medical_record_window.title("Update Medical Record")

    label_title = tk.Label(update_medical_record_window, text="Update Medical Record", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_medical_record_id = tk.Label(update_medical_record_window, text="Medical Record ID:")
    label_medical_record_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Dropdown for selecting existing medical record IDs
    medical_record_ids = [str(record['_id']) for record in medical_records_collection.find({}, {"_id": 1})]
    medical_record_var = tk.StringVar()
    medical_record_dropdown = ttk.Combobox(update_medical_record_window, textvariable=medical_record_var, values=medical_record_ids)
    medical_record_dropdown.grid(row=1, column=1, padx=10, pady=5)

    def fill_data():
        # Retrieve the selected medical record
        selected_record_id = bson.ObjectId(medical_record_var.get())
        selected_record = medical_records_collection.find_one({"_id": selected_record_id})

        # Fill the input fields with the data from the selected record
        entry_date.delete(0, tk.END)
        entry_date.insert(0, selected_record['date'])

        entry_doctor.delete(0, tk.END)
        entry_doctor.insert(0, selected_record['doctor'])

        entry_notes.delete(0, tk.END)
        entry_notes.insert(0, selected_record['notes'])

    # Button to fill data based on selected medical record
    button_fill_data = tk.Button(update_medical_record_window, text="Fill Data", command=fill_data)
    button_fill_data.grid(row=1, column=2, padx=10, pady=5)

    label_date = tk.Label(update_medical_record_window, text="Date:")
    label_date.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    entry_date = tk.Entry(update_medical_record_window)
    entry_date.grid(row=2, column=1, padx=10, pady=5)

    label_doctor = tk.Label(update_medical_record_window, text="Doctor:")
    label_doctor.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    entry_doctor = tk.Entry(update_medical_record_window)
    entry_doctor.grid(row=3, column=1, padx=10, pady=5)

    label_notes = tk.Label(update_medical_record_window, text="Notes:")
    label_notes.grid(row=4, column=0, padx=10, pady=5, sticky="e")

    entry_notes = tk.Entry(update_medical_record_window)
    entry_notes.grid(row=4, column=1, padx=10, pady=5)

    button_submit = tk.Button(update_medical_record_window, text="Submit", command=lambda: update_medical_record(medical_record_var.get(), {
        "date": entry_date.get(),
        "doctor": entry_doctor.get(),
        "notes": entry_notes.get()
    }))
    button_submit.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
def update_medical_record(record_id, update_data):
    # Update medical record in the database
    medical_records_collection.update_one({"_id": bson.ObjectId(record_id)}, {"$set": update_data})
    messagebox.showinfo("Success", "Medical record updated successfully!")
def delete_medical_record_window():
    delete_medical_record_window = tk.Toplevel()
    delete_medical_record_window.title("Delete Medical Record")

    label_title = tk.Label(delete_medical_record_window, text="Delete Medical Record", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    label_medical_record_id = tk.Label(delete_medical_record_window, text="Select Medical Record ID:")
    label_medical_record_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Dropdown for selecting existing medical record IDs
    medical_record_ids = [str(record['_id']) for record in medical_records_collection.find({}, {"_id": 1})]
    medical_record_var = tk.StringVar()
    medical_record_dropdown = ttk.Combobox(delete_medical_record_window, textvariable=medical_record_var, values=medical_record_ids)
    medical_record_dropdown.grid(row=1, column=1, padx=10, pady=5)

    def delete_record():
        # Delete the selected medical record
        selected_record_id = bson.ObjectId(medical_record_var.get())
        medical_records_collection.delete_one({"_id": selected_record_id})
        messagebox.showinfo("Success", "Medical record deleted successfully!")
        delete_medical_record_window.destroy()  # Close the window after deletion

    # Button to delete the selected medical record
    button_delete_record = tk.Button(delete_medical_record_window, text="Delete Record", command=delete_record)
    button_delete_record.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


# Billing and Invoicing
def generate_invoice(patient_id, services_rendered_str):
    services_rendered_list = services_rendered_str.split(',')
    services_rendered = {}
    for service in services_rendered_list:
        service_name, service_cost = service.split(':')
        services_rendered[service_name.strip()] = float(service_cost.strip())
    
    total_cost = sum(services_rendered.values())
    
    invoice_data = {
        "patient_id": bson.ObjectId(patient_id),
        "services_rendered": services_rendered,
        "total_cost": total_cost,
        "status": "Pending"
    } 
    
    invoices_collection.insert_one(invoice_data)
    messagebox.showinfo("Success", "Invoice generated successfully!")
def generate_invoice_window(generate_invoice_tab):
    # Clear existing content in the generate invoice tab
    for widget in generate_invoice_tab.winfo_children():
        widget.destroy()
    
    # Title label
    label_title = tk.Label(generate_invoice_tab, text="Generate Invoice", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Labels
    label_patient_id = tk.Label(generate_invoice_tab, text="Patient ID:")
    label_patient_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    
    label_services_rendered = tk.Label(generate_invoice_tab, text="Services Rendered (comma-separated):")
    label_services_rendered.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    # Entry fields
    entry_patient_id = tk.Entry(generate_invoice_tab)
    entry_patient_id.grid(row=1, column=1, padx=10, pady=5)
    
    entry_services_rendered = tk.Entry(generate_invoice_tab)
    entry_services_rendered.grid(row=2, column=1, padx=10, pady=5)

    # Submit button
    button_submit = tk.Button(generate_invoice_tab, text="Submit", command=lambda: generate_invoice(entry_patient_id.get(), entry_services_rendered.get()))
    button_submit.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
def track_payment_window(track_payment_tab):
    # Clear existing content in the track payment tab
    for widget in track_payment_tab.winfo_children():
        widget.destroy()
    
    # Title label
    label_title = tk.Label(track_payment_tab, text="Track Payment Status", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Labels
    label_invoice_id = tk.Label(track_payment_tab, text="Invoice ID:")
    label_invoice_id.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Entry field
    entry_invoice_id = tk.Entry(track_payment_tab)
    entry_invoice_id.grid(row=1, column=1, padx=10, pady=5)

    # Submit button
    button_submit = tk.Button(track_payment_tab, text="Submit", command=lambda: track_payment_status(entry_invoice_id.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def track_payment_status(invoice_id):
    # Track payment status for invoice
    invoice = invoices_collection.find_one({"_id": bson.ObjectId(invoice_id)})
    if invoice:
        payment_status = invoice.get("status", "Unknown")
        messagebox.showinfo("Payment Status", f"The payment status for Invoice {invoice_id} is: {payment_status}")
    else:
        messagebox.showerror("Error", "Invoice not found")
def generate_report_window(generate_report_tab):
    # Clear existing content in the generate report tab
    for widget in generate_report_tab.winfo_children():
        widget.destroy()
    
    # Title label
    label_title = tk.Label(generate_report_tab, text="Generate Report", font=("Helvetica", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Report type dropdown
    label_report_type = tk.Label(generate_report_tab, text="Report Type:")
    label_report_type.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    report_type_var = tk.StringVar()
    report_type_dropdown = ttk.Combobox(generate_report_tab, textvariable=report_type_var, values=["Sales", "Appointments"])
    report_type_dropdown.grid(row=1, column=1, padx=10, pady=5)

    # Submit button
    button_submit = tk.Button(generate_report_tab, text="Generate", command=lambda: generate_report(report_type_var.get()))
    button_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def generate_report(report_type):
    if report_type == "Sales":
        generate_sales_report()
    elif report_type == "Appointments":
        generate_appointments_report()
    else:
        messagebox.showerror("Error", "Invalid report type")
def generate_sales_report():
    sales_data = invoices_collection.find({})
    total_cost = sum(invoice["total_cost"] for invoice in sales_data)

    # Create report window
    report_window = tk.Toplevel()
    report_window.title("Sales Report")

    # Sales data table
    tree = ttk.Treeview(report_window, columns=("Patient ID", "Services Rendered", "Total Cost"))
    tree.heading("#0", text="Invoice ID")
    tree.heading("Patient ID", text="Patient ID")
    tree.heading("Services Rendered", text="Services Rendered")
    tree.heading("Total Cost", text="Total Cost")

    for invoice in invoices_collection.find({}):
        tree.insert("", "end", text=invoice["_id"], values=(invoice["patient_id"], ", ".join(invoice["services_rendered"].keys()), invoice["total_cost"]))

    tree.pack()

    # Total cost label
    label_total_cost = tk.Label(report_window, text=f"Total Cost: ${total_cost}")
    label_total_cost.pack()
def generate_appointments_report():
    appointments_data = appointments_collection.find({})

    # Create report window
    report_window = tk.Toplevel()
    report_window.title("Appointments Report")

    # Appointments data table
    tree = ttk.Treeview(report_window, columns=("Date", "Doctor"))
    tree.heading("#0", text="Appointment ID")
    tree.heading("Date", text="Date")
    tree.heading("Doctor", text="Doctor")

    for appointment in appointments_data:
        tree.insert("", "end", text=appointment["_id"], values=(appointment["datetime"], appointment["doctor_id"]))

    tree.pack()


# GUI Interface
def create_main_window():
    global main_window
    main_window = tk.Tk()
    main_window.title("MediTech System - Main Menu")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(main_window)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create tabs for different functionalities
    dashboard_tab = tk.Frame(notebook)
    patient_management_tab = tk.Frame(notebook)
    doctor_management_tab = tk.Frame(notebook)
    staff_management_tab = tk.Frame(notebook)
    appointment_management_tab = tk.Frame(notebook)
    medical_records_management_tab = tk.Frame(notebook)
    generate_invoice_tab = tk.Frame(notebook)
    generate_report_tab = tk.Frame(notebook)
    track_payment_tab = tk.Frame(notebook)

    # Add tabs to the notebook
    notebook.add(dashboard_tab, text="Dashboard")
    notebook.add(patient_management_tab, text="Patient Management")
    notebook.add(doctor_management_tab, text="Doctor Management")
    notebook.add(staff_management_tab, text="Nurse/Staff Management")
    notebook.add(appointment_management_tab, text="Appointment Management")
    notebook.add(medical_records_management_tab, text="Medical Records Management")
    notebook.add(generate_invoice_tab, text="Generate Invoice")
    notebook.add(generate_report_tab, text="Generate Report")
    notebook.add(track_payment_tab, text="Track Payment Status")

    # Add a logout button outside the notebook
    button_logout = tk.Button(main_window, text="Logout", command=lambda: logout(main_window))
    button_logout.pack(pady=5)

    # Call display_dashboard function when Dashboard tab is clicked
    def on_tab_change(event):
        current_tab_name = notebook.tab(notebook.select(), "text")
        if current_tab_name == "Dashboard":
            display_dashboard(dashboard_tab)
        elif current_tab_name == "Patient Management":
            patient_management_window(patient_management_tab)
        elif current_tab_name == "Doctor Management":
            doctor_management_window(doctor_management_tab)
        elif current_tab_name == "Nurse/Staff Management":
            staff_management_window(staff_management_tab)
        elif current_tab_name == "Appointment Management":
            appointment_management_window(appointment_management_tab)
        elif current_tab_name == "Medical Records Management":
            medical_records_management_window(medical_records_management_tab)
        elif current_tab_name == "Generate Invoice":
            generate_invoice_window(generate_invoice_tab)
        elif current_tab_name == "Generate Report":
            generate_report_window(generate_report_tab)
        elif current_tab_name == "Track Payment Status":
            track_payment_window(track_payment_tab)

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    main_window.mainloop()

# Call create_main_window after successful login
if __name__ == "__main__":
    create_login_window()
