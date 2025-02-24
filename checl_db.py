import sqlite3

def check_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('healthcare_claims.db')
        cursor = conn.cursor()

        # Check if Patients table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Patients'")
        if cursor.fetchone() is None:
            print("Patients table does not exist!")
            return

        # Get all patients
        cursor.execute("SELECT PatientID, PatientName FROM Patients")
        patients = cursor.fetchall()
        
        print(f"\nTotal number of patients: {len(patients)}")
        print("\nPatient IDs and Names:")
        for patient in patients:
            print(f"ID: {patient[0]}, Name: {patient[1]}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_database()