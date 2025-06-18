import json
from prettytable import PrettyTable
import os

# --------------------------- DataHandler ---------------------------
class DataHandler:
    """Handles loading and saving data from a JSON file."""
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        # Check if file exists, if not create default structure
        if not os.path.exists(self.file_path):
            default_data = {
                "doctors": [],
                "patients": []
            }
            self.save_data(default_data)
            return default_data
        
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error reading file {self.file_path}. Creating new file.")
            default_data = {
                "doctors": [],
                "patients": []
            }
            self.save_data(default_data)
            return default_data

    def save_data(self, data):
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# --------------------------- Patient ---------------------------
class Patient:
    """Represents a patient in the hospital."""
    def __init__(self, name, age, condition, room_number=None, procedures=None):
        self.name = name
        self.age = age
        self.condition = condition
        self.room_number = room_number
        self.procedures = procedures if procedures else {}

# --------------------------- Doctor ---------------------------
class Doctor:
    def __init__(self, name, age, specialty):
        self.name = name
        self.age = age
        self.specialty = specialty

# --------------------------- EmergencyDept ---------------------------
class EmergencyDept:
    """Manages emergency patients."""
    def __init__(self):
        self.emergency_patients = []

    def add_patient(self, patient):
        self.emergency_patients.append(patient)

    def list_patients(self):
        return self.emergency_patients

# --------------------------- RoomManager ---------------------------
class RoomManager:
    """Manages room assignments."""
    def __init__(self):
        self.rooms = {}

    def assign_room(self, patient, room_number):
        if room_number in self.rooms:
            return False
        self.rooms[room_number] = patient.name
        patient.room_number = room_number
        return True

    def view_rooms(self):
        return self.rooms

# --------------------------- OperationManager ---------------------------
class OperationManager:
    """Schedules operations for patients."""
    def __init__(self):
        self.operations = []

    def schedule_operation(self, patient, doctor):
        self.operations.append({
            "patient": patient.name,
            "room": patient.room_number,
            "doctor": doctor.name
        })

# --------------------------- BillingSystem ---------------------------
class BillingSystem:
    """Generates and displays billing information for patients."""
    def generate_bill(self, patient):
        table = PrettyTable()
        table.field_names = ["Procedure", "Cost ($)"]
        total = 0
        for proc, cost in patient.procedures.items():
            table.add_row([proc, f"{cost:.2f}"])
            total += cost
        table.add_row(["Total", f"{total:.2f}"])
        return table

# --------------------------- HospitalSystem ---------------------------
class HospitalSystem:
    """Main class that connects all components and handles the UI."""
    def __init__(self, file_path):
        self.data_handler = DataHandler(file_path)
        self.data = self.data_handler.load_data()
        self.room_manager = RoomManager()
        self.emergency = EmergencyDept()
        self.operations = OperationManager()
        self.billing = BillingSystem()
        
        # تعديل هنا لتجنب الخطأ
        self.doctors = []
        doctors_data = self.data.get("doctors", [])
        for d in doctors_data:
            if isinstance(d, dict) and all(key in d for key in ['name', 'age', 'specialty']):
                self.doctors.append(Doctor(d['name'], d['age'], d['specialty']))
        
        self.patients = []
        patients_data = self.data.get("patients", [])
        for p in patients_data:
            if isinstance(p, dict) and all(key in p for key in ['name', 'age', 'condition']):
                patient = Patient(
                    p['name'], 
                    p['age'], 
                    p['condition'], 
                    p.get('room_number'), 
                    p.get('procedures', {})
                )
                self.patients.append(patient)
                
        # إضافة المرضى للغرف
        for p in self.patients:
            if p.room_number is not None:
                self.room_manager.assign_room(p, p.room_number)

    def save_current_state(self):
        """Save current state to file"""
        data = {
            "doctors": [
                {"name": d.name, "age": d.age, "specialty": d.specialty} 
                for d in self.doctors
            ],
            "patients": [
                {
                    "name": p.name, 
                    "age": p.age, 
                    "condition": p.condition,
                    "room_number": p.room_number,
                    "procedures": p.procedures
                } 
                for p in self.patients
            ]
        }
        self.data_handler.save_data(data)

    def add_doctor(self):
        """Add a new doctor"""
        name = input("Enter doctor's name: ")
        try:
            age = int(input("Enter doctor's age: "))
        except ValueError:
            print("Age must be a number")
            return
        specialty = input("Enter doctor's specialty: ")
        doctor = Doctor(name, age, specialty)
        self.doctors.append(doctor)
        print(f"Doctor {name} added successfully")

    def add_patient(self):
        name = input("Enter patient's name: ")
        try:
            age = int(input("Enter patient's age: "))
        except ValueError:
            print("Age must be a number")
            return
        condition = input("Enter diagnosis: ")
        p = Patient(name, age, condition)
        self.patients.append(p)
        self.emergency.add_patient(p)
        choice = input("Assign room? (yes/no): ")
        if choice.lower() in ['yes', 'y']:
            try:
                room = int(input("Enter room number: "))
                if self.room_manager.assign_room(p, room):
                    print(f"Assigned to room {room}")
                else:
                    print("Room is already taken")
            except ValueError:
                print("Room number must be a number")

    def schedule_operation(self):
        if not self.doctors:
            print("No doctors in the system. Please add a doctor first")
            return
            
        try:
            room = int(input("Enter room number: "))
        except ValueError:
            print("Room number must be a number")
            return
            
        patient = next((p for p in self.patients if p.room_number == room), None)
        if not patient:
            print("No patient in that room")
            return
            
        print("Available doctors:")
        for i, doc in enumerate(self.doctors):
            print(f"{i+1}. {doc.name} ({doc.specialty})")
        
        try:
            index = int(input("Select doctor number: ")) - 1
            if 0 <= index < len(self.doctors):
                self.operations.schedule_operation(patient, self.doctors[index])
                print("Operation scheduled successfully")
            else:
                print("Invalid doctor number")
        except ValueError:
            print("Please enter a valid number")

    def generate_bill(self):
        try:
            room = int(input("Enter room number: "))
        except ValueError:
            print("Room number must be a number")
            return
            
        patient = next((p for p in self.patients if p.room_number == room), None)
        if not patient:
            print("No patient in that room")
            return
            
        print(f"Adding procedures for patient: {patient.name}")
        while True:
            proc = input("Enter procedure name (or 'done' to finish): ")
            if proc.lower() == 'done':
                break
            try:
                cost = float(input("Enter cost: "))
                patient.procedures[proc] = cost
            except ValueError:
                print("Cost must be a number")
                
        print("\n--- Patient Bill ---")
        print(self.billing.generate_bill(patient))

    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("         Capital Hospital - Patient Management System")
            print("="*50)
            print("1. Emergency Department")
            print("2. View Rooms")
            print("3. Add Patient")
            print("4. Add Doctor")
            print("5. Schedule Operation")
            print("6. Generate Bill")
            print("7. Save Data")
            print("8. Exit")
            print("-"*50)
            
            choice = input("Select option (1-8): ")
            
            if choice == '1':
                print("\n--- Emergency Department ---")
                emergency_patients = self.emergency.list_patients()
                if emergency_patients:
                    for p in emergency_patients:
                        room_status = f"Room: {p.room_number}" if p.room_number else "No room assigned"
                        print(f"Name: {p.name}, Age: {p.age}, Condition: {p.condition}, {room_status}")
                else:
                    print("No patients in emergency department")
                    
            elif choice == '2':
                print("\n--- Room Status ---")
                rooms = self.room_manager.view_rooms()
                if rooms:
                    for room, name in rooms.items():
                        print(f"Room {room}: {name}")
                else:
                    print("All rooms are empty")
                    
            elif choice == '3':
                self.add_patient()
                
            elif choice == '4':
                self.add_doctor()
                
            elif choice == '5':
                self.schedule_operation()
                
            elif choice == '6':
                self.generate_bill()
                
            elif choice == '7':
                self.save_current_state()
                print("Data saved successfully")
                
            elif choice == '8':
                print("Do you want to save data before exiting? (yes/no): ", end="")
                save_choice = input()
                if save_choice.lower() in ['yes', 'y']:
                    self.save_current_state()
                    print("Data saved")
                print("Thank you for using Capital Hospital Management System")
                break
                
            else:
                print("Invalid choice. Please try again")