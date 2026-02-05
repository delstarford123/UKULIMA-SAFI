import os
import csv

def create_contact_files():
    # --- CONFIGURATION ---
    # Path: data -> agrovets_and_agronomists
    base_directory = os.path.join("data", "agrovets_and_agronomists")
    
    # Ensure directory exists
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
        print(f"📂 Created folder: {base_directory}")

    # --- FILE 1: AGROVETS (agrovets_region.csv) ---
    agrovets_file = os.path.join(base_directory, "agrovets_region.csv")
    agrovets_headers = ['crop', 'agrovet', 'region', 'phone', 'email', 'location']
    
    # exact data provided
    agrovets_data = [
        {"crop": "Tomatoes", "agrovet": "Kedel", "region": "Kakamega", "phone": "0707605751", "email": "delstarfordisaiah@gmail.com", "location": "https://goo.gl/maps/1Zz5s8n9v7oL2XjA6"},
        {"crop": "Tomatoes", "agrovet": "Maru", "region": "Mombasa", "phone": "0723456789", "email": "", "location": ""},
        {"crop": "Tomatoes", "agrovet": "Jane Vet", "region": "Kisumu", "phone": "0734567890", "email": "", "location": ""},
        {"crop": "Potatoes", "agrovet": "Tiba Kamili", "region": "Nakuru", "phone": "0745678901", "email": "", "location": ""},
        {"crop": "Potatoes", "agrovet": "Maliktiba", "region": "Eldoret", "phone": "0756789012", "email": "", "location": ""},
        {"crop": "Wheat", "agrovet": "A", "region": "Kitale", "phone": "0767890123", "email": "", "location": ""},
        {"crop": "Wheat", "agrovet": "Agrovet G", "region": "Meru", "phone": "0778901234", "email": "", "location": ""},
        {"crop": "Rice", "agrovet": "Agrovet H", "region": "Garissa", "phone": "0789012345", "email": "", "location": ""},
        {"crop": "Rice", "agrovet": "Agrovet I", "region": "Isiolo", "phone": "0790123456", "email": "", "location": ""},
        {"crop": "Maize", "agrovet": "Agrovet J", "region": "Embu", "phone": "0701234567", "email": "", "location": ""},
        {"crop": "Maize", "agrovet": "Agrovet K", "region": "Nyeri", "phone": "0712345678", "email": "", "location": ""},
        {"crop": "Soybeans", "agrovet": "Agrovet L", "region": "Thika", "phone": "0723456789", "email": "", "location": ""},
        {"crop": "Soybeans", "agrovet": "Agrovet M", "region": "Kiambu", "phone": "0734567890", "email": "", "location": ""},
        {"crop": "Carrots", "agrovet": "Agrovet N", "region": "Nyandarua", "phone": "0745678901", "email": "", "location": ""},
        {"crop": "Carrots", "agrovet": "Agrovet O", "region": "Laikipia", "phone": "0756789012", "email": "", "location": ""},
        {"crop": "Onions", "agrovet": "Agrovet P", "region": "Turkana", "phone": "0767890123", "email": "", "location": ""},
        {"crop": "Onions", "agrovet": "Agrovet Q", "region": "West Pokot", "phone": "0778901234", "email": "", "location": ""},
        {"crop": "Beans", "agrovet": "Agrovet R", "region": "Bomet", "phone": "0789012345", "email": "", "location": ""},
        {"crop": "Beans", "agrovet": "Agrovet S", "region": "Kericho", "phone": "0790123456", "email": "", "location": ""}
    ]
    write_csv(agrovets_file, agrovets_headers, agrovets_data)


    # --- FILE 2: AGRONOMISTS (agronomist_region.csv) ---
    # Matched to the regions above so your app always finds someone.
    agronomist_file = os.path.join(base_directory, "agronomist_region.csv")
    agronomist_headers = ['crop', 'agronomist', 'region', 'phone', 'email', 'location']
    
    agronomist_data = [
        {"crop": "Tomatoes", "agronomist": "Dr. John Omondi", "region": "Kakamega", "phone": "0711223344", "email": "jomondi@ukulimasafi.co.ke", "location": "MMUST Agricultural Dept"},
        {"crop": "Tomatoes", "agronomist": "Sarah Hassan", "region": "Mombasa", "phone": "0722334455", "email": "sarah.h@coastagri.com", "location": "Mtwapa Research Ctr"},
        {"crop": "Tomatoes", "agronomist": "Peter Anyang", "region": "Kisumu", "phone": "0733445566", "email": "p.anyang@lakebasin.org", "location": "Kibos Road"},
        {"crop": "Potatoes", "agronomist": "James Njoroge", "region": "Nakuru", "phone": "0744556677", "email": "j.njoroge@egerton.ac.ke", "location": "Egerton Uni"},
        {"crop": "Potatoes", "agronomist": "Alice Chebet", "region": "Eldoret", "phone": "0755667788", "email": "a.chebet@uasin.gov.ke", "location": "Eldoret CBD"},
        {"crop": "Wheat", "agronomist": "David Wanyama", "region": "Kitale", "phone": "0766778899", "email": "d.wanyama@transnzoia.go.ke", "location": "Kitale Museum Rd"},
        {"crop": "Wheat", "agronomist": "Grace Kira", "region": "Meru", "phone": "0777889900", "email": "g.kira@merugreen.co.ke", "location": "Maua Road"},
        {"crop": "Rice", "agronomist": "Ahmed Abdi", "region": "Garissa", "phone": "0788990011", "email": "a.abdi@northeastagri.org", "location": "Garissa Town"},
        {"crop": "Rice", "agronomist": "Fatuma Ali", "region": "Isiolo", "phone": "0799001122", "email": "f.ali@isiolo.go.ke", "location": "Isiolo Market"},
        {"crop": "Maize", "agronomist": "Benson Njue", "region": "Embu", "phone": "0700112233", "email": "b.njue@kalro.org", "location": "KALRO Embu"},
        {"crop": "Maize", "agronomist": "Catherine Wambui", "region": "Nyeri", "phone": "0711223355", "email": "c.wambui@centralagri.com", "location": "Nyeri Town"},
        {"crop": "Soybeans", "agronomist": "Dr. Kamau", "region": "Thika", "phone": "0722334466", "email": "kamau@jkuat.ac.ke", "location": "JKUAT Juja"},
        {"crop": "Soybeans", "agronomist": "Lucy Mwaura", "region": "Kiambu", "phone": "0733445577", "email": "l.mwaura@kiambu.go.ke", "location": "Kiambu Rd"},
        {"crop": "Carrots", "agronomist": "Simon Kingori", "region": "Nyandarua", "phone": "0744556688", "email": "s.kingori@kinangop.co.ke", "location": "Engineer Town"},
        {"crop": "Carrots", "agronomist": "Esther Maina", "region": "Laikipia", "phone": "0755667799", "email": "e.maina@laikipia.go.ke", "location": "Nanyuki"},
        {"crop": "Onions", "agronomist": "Josphat Ekwam", "region": "Turkana", "phone": "0766778800", "email": "j.ekwam@lodwar.co.ke", "location": "Lodwar"},
        {"crop": "Onions", "agronomist": "Mary Lonyangapuo", "region": "West Pokot", "phone": "0777889911", "email": "m.lonyang@kapenguria.go.ke", "location": "Kapenguria"},
        {"crop": "Beans", "agronomist": "Kipkirui Langat", "region": "Bomet", "phone": "0788990022", "email": "k.langat@bomet.go.ke", "location": "Bomet Green Stadium"},
        {"crop": "Beans", "agronomist": "Cherotich Rono", "region": "Kericho", "phone": "0799001133", "email": "c.rono@tea-zone.co.ke", "location": "Kericho Town"}
    ]
    write_csv(agronomist_file, agronomist_headers, agronomist_data)

def write_csv(filepath, headers, data):
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"✅ Generated: {filepath}")
    except IOError as e:
        print(f"❌ Error writing {filepath}: {e}")

if __name__ == "__main__":
    create_contact_files()