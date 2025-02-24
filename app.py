from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'healthcare1.db'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = query_db('SELECT * FROM patients WHERE id = ?', [patient_id], one=True)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    claims = query_db('SELECT * FROM claims WHERE patient_id = ?', [patient_id])

    patient_data = {
        'id': patient['id'],
        'name': patient['name'],
        'dob': patient['dob'],
        'address': patient['address'],
        'phone': patient['phone'],
        'insurance_provider': patient['insurance_provider'],
        'policy_number': patient['policy_number'],
        'claims': [
            {
                'provider_name': claim['provider_name'],
                'member_name': claim['member_name'],
                'member_id': claim['member_id'],
                'claim_number': claim['claim_number'],
                'date_of_service': claim['date_of_service'],
                'billed_amount': claim['billed_amount'],
                'npi': claim['npi'],
                'facility_name': claim['facility_name'],
                'payment_mode': claim['payment_mode'],
                'status': claim['status']
            } for claim in claims
        ]
    }
    return jsonify(patient_data)



if __name__ == '__main__':
    app.run(debug=True)
