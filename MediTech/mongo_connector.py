# mongo_connector.py
from pymongo import MongoClient

# Connect to MongoDB (default host and port)
client = MongoClient()

# Specify the database name (if it doesn't exist, MongoDB will create it)
db = client['MediEase']

# Specify the collection (similar to a table in relational databases)
patients_collection = db['patients']

# Insert data into the collection
patient_data = {
    "name": "John Doe",
    "age": 35,
    "gender": "Male",
    "address": "123 Main St, City",
    "contact_details": "123-456-7890",
    "insurance_information": "ABC Insurance",
    "medical_history": {
        "diagnoses": ["Hypertension", "Diabetes"],
        "treatments": ["Medication A", "Medication B"],
        "surgeries": ["Appendectomy"],
        "allergies": ["Penicillin"],
        "family_medical_history": ["Heart disease"]
    }
}

# Insert the data into the collection
result = patients_collection.insert_one(patient_data)

# Check if the data was inserted successfully
if result.inserted_id:
    print(f"Data inserted successfully with ID: {result.inserted_id}")
else:
    print("Failed to insert data.")

# Add medical history to patient record
medical_history = {
    "diagnoses": ["Hypertension", "Diabetes"],
    "treatments": ["Medication A", "Medication B"],
    "surgeries": ["Appendectomy"],
    "allergies": ["Penicillin"],
    "family_medical_history": ["Heart disease"]
}
patients_collection.update_one({"name": "John Doe"}, {"$set": {"medical_history": medical_history}})

# Create appointments collection
appointments_collection = db['appointments']

# Schedule an appointment
appointment_data = {
    "patient_id": "123456",
    "doctor_id": "789012",
    "appointment_date": "2025-03-01",
    "status": "Scheduled"
}
appointments_collection.insert_one(appointment_data)

# Create staff collection
staff_collection = db['staff']

# Add staff profile
staff_data = {
    "name": "Dr. Smith",
    "qualification": "MD",
    "specialty": "Cardiology",
    "contact_info": "456-789-0123",
    "work_schedule": "Mon-Fri, 9am-5pm"
}
staff_collection.insert_one(staff_data)

# Create invoices collection
invoices_collection = db['invoices']

# Generate invoice
invoice_data = {
    "patient_id": "123456",
    "service_description": "Consultation",
    "cost": 100,
    "insurance_coverage": 80,
    "payment_due_date": "2025-03-15"
}
invoices_collection.insert_one(invoice_data)

# Create inventory collection
inventory_collection = db['inventory']

# Add inventory item
inventory_data = {
    "item_name": "Medication A",
    "quantity": 100,
    "expiration_date": "2025-12-31",
    "reorder_threshold": 20
}
inventory_collection.insert_one(inventory_data)

# Generate custom report
report = patients_collection.aggregate([
    {"$group": {"_id": "$gender", "count": {"$sum": 1}}}
])
for doc in report:
    print(doc)
