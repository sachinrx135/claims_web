import sqlite3
from faker import Faker

fake = Faker()

DATABASE = 'healthcare.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            insurance_provider TEXT NOT NULL,
            policy_number TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            provider_name TEXT NOT NULL,
            member_name TEXT NOT NULL,
            member_id TEXT NOT NULL,
            claim_number TEXT NOT NULL,
            date_of_service TEXT NOT NULL,
            billed_amount REAL NOT NULL,
            npi TEXT NOT NULL,
            facility_name TEXT NOT NULL,
            payment_mode TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            notes TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    conn.commit()
    conn.close()

def insert_patient():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, dob, address, phone, insurance_provider, policy_number)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        fake.name(),
        fake.date_of_birth().strftime('%Y-%m-%d'),
        fake.address().replace('\n', ', '),
        fake.phone_number(),
        fake.company(),
        fake.bothify(text='??????????')
    ))
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id

def insert_claim(patient_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO claims (patient_id, provider_name, member_name, member_id, claim_number, date_of_service, billed_amount, npi, facility_name, payment_mode, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        patient_id,
        fake.name(),
        fake.name(),
        fake.bothify(text='??????????'),
        fake.bothify(text='??????????'),
        fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d'),
        fake.random_int(min=100, max=10000),
        fake.bothify(text='??????????'),
        fake.company(),
        fake.random_element(elements=('Cheque', 'EFT')),
        fake.random_element(elements=('Pending', 'Approved', 'Rejected'))
    ))
    conn.commit()
    conn.close()

def insert_note(patient_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notes (patient_id, notes)
        VALUES (?, ?)
    ''', (
        patient_id,
        fake.paragraph(nb_sentences=5)
    ))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

    num_patients = 10

    for _ in range(num_patients):
        patient_id = insert_patient()
        print(f"Inserted patient with ID: {patient_id}")

        insert_claim(patient_id)
        print(f"Inserted claim for patient with ID: {patient_id}")

        insert_note(patient_id)
        print(f"Inserted note for patient with ID: {patient_id}")