# Hospital Management System

A comprehensive hospital management system built in Python that handles patient registration, doctor management, room assignments, operation scheduling, and billing.

## Features

- **Patient Management**: Add and track patients with their medical conditions
- **Doctor Management**: Maintain doctor profiles with specialties
- **Emergency Department**: Handle emergency patients separately
- **Room Management**: Assign and track room occupancy
- **Operation Scheduling**: Schedule operations with doctors and patients
- **Billing System**: Generate detailed bills for patient procedures
- **Data Persistence**: Save and load data from JSON files

## Project Structure

```
hospital-management-system/
├── run.py                  # Main entry point
├── hospital_system.py      # Core hospital system classes
├── requirements.txt        # Python dependencies
├── requirements.system     # System dependencies (if any)
├── output/                 # Output directory for generated files
└── README.md              # This file
```

## Environment Variables

The system supports various environment variables for configuration:

### Basic Configuration
- `DATA_FILE`: Name of the JSON data file (default: `hospital_data.json`)
- `OUTPUT_DIR`: Output directory path (default: `output`)
- `MODE`: Run mode - `interactive` or `batch` (default: `interactive`)

### Batch Operations
When `MODE=batch`, you can perform automated operations:

- `OPERATION`: Type of operation (`add_patient`, `add_doctor`, `generate_report`)

#### Adding Patients (OPERATION=add_patient)
- `PATIENT_NAME`: Patient's name
- `PATIENT_AGE`: Patient's age
- `PATIENT_CONDITION`: Medical condition
- `PATIENT_ROOM`: Room number (optional)

#### Adding Doctors (OPERATION=add_doctor)
- `DOCTOR_NAME`: Doctor's name
- `DOCTOR_AGE`: Doctor's age
- `DOCTOR_SPECIALTY`: Medical specialty

#### Initial Data
- `INITIAL_DOCTORS`: JSON string with initial doctors data
- `INITIAL_PATIENTS`: JSON string with initial patients data

## Usage Examples

### Interactive Mode (Default)
```bash
python run.py
```

### Batch Mode - Add Patient
```bash
export MODE=batch
export OPERATION=add_patient
export PATIENT_NAME="John Doe"
export PATIENT_AGE=35
export PATIENT_CONDITION="Flu"
export PATIENT_ROOM=101
python run.py
```

### Batch Mode - Add Doctor
```bash
export MODE=batch
export OPERATION=add_doctor
export DOCTOR_NAME="Dr. Smith"
export DOCTOR_AGE=45
export DOCTOR_SPECIALTY="Cardiology"
python run.py
```

### Batch Mode - Generate Report
```bash
export MODE=batch
export OPERATION=generate_report
python run.py
```

### With Initial Data
```bash
export INITIAL_DOCTORS='[{"name": "Dr. Johnson", "age": 40, "specialty": "General Practice"}]'
export INITIAL_PATIENTS='[{"name": "Jane Doe", "age": 28, "condition": "Checkup", "room_number": 102}]'
python run.py
```

## Output Files

The system generates files in the `output/` directory:

- `hospital_data.json`: Main data file with all hospital information
- `hospital_report.txt`: Comprehensive hospital report (when generated)

## Interactive Menu Options

1. **Emergency Department**: View all emergency patients
2. **View Rooms**: Check room occupancy status
3. **Add Patient**: Register a new patient
4. **Add Doctor**: Add a new doctor to the system
5. **Schedule Operation**: Schedule an operation for a patient
6. **Generate Bill**: Create a bill for patient procedures
7. **Save Data**: Save current state to file
8. **Exit**: Exit the system

## Data Format

### Doctors JSON Format
```json
{
  "name": "Dr. Smith",
  "age": 45,
  "specialty": "Cardiology"
}
```

### Patients JSON Format
```json
{
  "name": "John Doe",
  "age": 35,
  "condition": "Heart condition",
  "room_number": 101,
  "procedures": {
    "ECG": 150.00,
    "Blood Test": 75.00
  }
}
```

## Requirements

- Python 3.6+
- prettytable library (automatically installed from requirements.txt)

## Installation

1. Ensure all files are in the project root directory
2. The system will automatically install dependencies and create necessary directories
3. Run with `python run.py`

## Error Handling

The system includes comprehensive error handling for:
- Invalid input data
- Missing files
- JSON parsing errors
- User input validation
- File I/O operations

## License

This project is open source and available under the MIT License.