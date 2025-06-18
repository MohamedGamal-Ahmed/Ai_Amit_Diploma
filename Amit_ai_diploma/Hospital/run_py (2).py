#!/usr/bin/env python3
"""
Hospital Management System - Entry Point
This is the main script that runs the hospital management system.
"""

import os
import sys
import json
from hospital_system_py import HospitalSystem

def main():
    """Main function to run the hospital management system"""
    print("Starting Hospital Management System...")
    
    # Get configuration from environment variables
    data_file = os.environ.get('DATA_FILE', 'hospital_data.json')
    output_dir = os.environ.get('OUTPUT_DIR', 'output')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Set the data file path to be in the output directory
    data_file_path = os.path.join(output_dir, data_file)
    
    # Check if we have initial data from environment variables
    initial_doctors = os.environ.get('INITIAL_DOCTORS')
    initial_patients = os.environ.get('INITIAL_PATIENTS')
    
    # Create initial data if provided
    if initial_doctors or initial_patients:
        create_initial_data(data_file_path, initial_doctors, initial_patients)
    
    try:
        # Initialize and run the hospital system
        system = HospitalSystem(data_file_path)
        
        # Check if we're running in interactive mode or batch mode
        mode = os.environ.get('MODE', 'interactive')
        
        if mode.lower() == 'interactive':
            system.main_menu()
        else:
            # Run in batch mode - perform specific operations based on environment variables
            run_batch_operations(system)
            
    except KeyboardInterrupt:
        print("\nSystem interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error running hospital system: {e}")
        sys.exit(1)

def create_initial_data(file_path, doctors_json=None, patients_json=None):
    """Create initial data file with doctors and patients"""
    data = {"doctors": [], "patients": []}
    
    if doctors_json:
        try:
            data["doctors"] = json.loads(doctors_json)
        except json.JSONDecodeError:
            print("Warning: Invalid doctors JSON data")
    
    if patients_json:
        try:
            data["patients"] = json.loads(patients_json)
        except json.JSONDecodeError:
            print("Warning: Invalid patients JSON data")
    
    # Save initial data
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Initial data created at {file_path}")

def run_batch_operations(system):
    """Run batch operations based on environment variables"""
    operation = os.environ.get('OPERATION', '').lower()
    
    if operation == 'add_patient':
        name = os.environ.get('PATIENT_NAME', 'John Doe')
        age = int(os.environ.get('PATIENT_AGE', '30'))
        condition = os.environ.get('PATIENT_CONDITION', 'General checkup')
        room = os.environ.get('PATIENT_ROOM')
        
        # Add patient programmatically
        from hospital_system_py import Patient
        patient = Patient(name, age, condition)
        system.patients.append(patient)
        system.emergency.add_patient(patient)
        
        if room:
            system.room_manager.assign_room(patient, int(room))
        
        print(f"Patient {name} added successfully")
        
    elif operation == 'add_doctor':
        name = os.environ.get('DOCTOR_NAME', 'Dr. Smith')
        age = int(os.environ.get('DOCTOR_AGE', '45'))
        specialty = os.environ.get('DOCTOR_SPECIALTY', 'General Practice')
        
        # Add doctor programmatically
        from hospital_system_py import Doctor
        doctor = Doctor(name, age, specialty)
        system.doctors.append(doctor)
        
        print(f"Doctor {name} added successfully")
        
    elif operation == 'generate_report':
        generate_hospital_report(system)
    
    # Always save the current state after batch operations
    system.save_current_state()

def generate_hospital_report(system):
    """Generate a comprehensive hospital report"""
    output_dir = os.environ.get('OUTPUT_DIR', 'output')
    report_file = os.path.join(output_dir, 'hospital_report.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("           CAPITAL HOSPITAL - SYSTEM REPORT\n")
        f.write("="*60 + "\n\n")
        
        # Doctors section
        f.write("DOCTORS:\n")
        f.write("-"*40 + "\n")
        if system.doctors:
            for i, doctor in enumerate(system.doctors, 1):
                f.write(f"{i}. {doctor.name} (Age: {doctor.age}, Specialty: {doctor.specialty})\n")
        else:
            f.write("No doctors in the system\n")
        f.write("\n")
        
        # Patients section
        f.write("PATIENTS:\n")
        f.write("-"*40 + "\n")
        if system.patients:
            for i, patient in enumerate(system.patients, 1):
                room_info = f"Room {patient.room_number}" if patient.room_number else "No room assigned"
                f.write(f"{i}. {patient.name} (Age: {patient.age}, Condition: {patient.condition}, {room_info})\n")
        else:
            f.write("No patients in the system\n")
        f.write("\n")
        
        # Emergency patients
        f.write("EMERGENCY PATIENTS:\n")
        f.write("-"*40 + "\n")
        emergency_patients = system.emergency.list_patients()
        if emergency_patients:
            for i, patient in enumerate(emergency_patients, 1):
                f.write(f"{i}. {patient.name} - {patient.condition}\n")
        else:
            f.write("No emergency patients\n")
        f.write("\n")
        
        # Room occupancy
        f.write("ROOM OCCUPANCY:\n")
        f.write("-"*40 + "\n")
        rooms = system.room_manager.view_rooms()
        if rooms:
            for room_num, patient_name in sorted(rooms.items()):
                f.write(f"Room {room_num}: {patient_name}\n")
        else:
            f.write("All rooms are empty\n")
        f.write("\n")
        
        # Statistics
        f.write("STATISTICS:\n")
        f.write("-"*40 + "\n")
        f.write(f"Total Doctors: {len(system.doctors)}\n")
        f.write(f"Total Patients: {len(system.patients)}\n")
        f.write(f"Emergency Patients: {len(emergency_patients)}\n")
        f.write(f"Occupied Rooms: {len(rooms)}\n")
        f.write(f"Scheduled Operations: {len(system.operations.operations)}\n")
    
    print(f"Hospital report generated: {report_file}")

if __name__ == "__main__":
    main()