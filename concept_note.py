from fpdf import FPDF

class ConceptNotePDF(FPDF):
    def header(self):
        # Logo or Brand Name in Header
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100) # Grey color
        self.cell(0, 10, 'DELSTARFORD WORKS.CO.KE | UKULIMA SAFI ', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 100, 0) # Dark Green for headers
        self.cell(0, 10, f'{num}. {label}', 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, body)
        self.ln()

    def sub_section(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, 0, 1, 'L')

    def bullet_point(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        # Indent and add bullet char
        self.cell(5) 
        self.cell(5, 6, chr(149), 0, 0) # Bullet character
        self.multi_cell(0, 6, text)
        self.ln(1)

def generate_pdf():
    pdf = ConceptNotePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Title Page Area ---
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(0, 102, 51) # Agri Green
    pdf.cell(0, 15, 'CONCEPT NOTE: UKULIMA SAFI ', 0, 1, 'C')
    
    pdf.set_font('Arial', 'I', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, 'Transforming Agriculture through Precision Intelligence', 0, 1, 'C')
    pdf.cell(0, 10, 'and Hyper-Connectivity', 0, 1, 'C')
    pdf.ln(10)

    # --- Metadata ---
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 6, 'Architected by:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'DELSTARFORD WORKS.CO.KE', 0, 1)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 6, 'Date:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'February 2026', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 6, 'Sector:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'AgriTech / Artificial Intelligence / Sustainability', 0, 1)
    pdf.ln(10)

    # --- 1. Executive Summary ---
    pdf.chapter_title('1', 'Executive Summary')
    pdf.chapter_body(
        'Agriculture in developing markets faces a "Last Mile" problem. While agricultural inputs (seeds, fertilizers) '
        'and scientific knowledge exist, they rarely reach the smallholder farmer efficiently. UKULIMA SAFI AI is a '
        'holistic digital ecosystem designed to bridge this gap.\n\n'
        'Beyond simple disease detection, Ukulima Safi serves as a pocket agronomist and supply chain integrator. '
        'By combining offline-capable AI diagnostics, real-time weather logic, and a geolocation-based service network, '
        'we provide agricultural industries with the data, connectivity, and precision they need to secure their '
        'supply chains and maximize farmer output.'
    )

    # --- 2. The Problem ---
    pdf.chapter_title('2', 'The Problem')
    pdf.chapter_body('Agricultural stakeholders (Seed Companies, Chemical Manufacturers, Contract Farming Groups) face three critical challenges:')
    
    pdf.sub_section('Yield Volatility:')
    pdf.bullet_point('Preventable diseases and pests destroy up to 40% of crops annually due to delayed diagnosis.')
    
    pdf.sub_section('Inefficient Extension Services:')
    pdf.bullet_point('Human agronomists cannot physically visit every farm frequently enough to ensure best practices.')
    
    pdf.sub_section('Data Blindness:')
    pdf.bullet_point('Industries lack real-time visibility into what is happening on the ground - disease outbreaks, crop growth stages, and harvest timelines.')
    pdf.ln(3)

    # --- 3. The Solution ---
    pdf.chapter_title('3', 'The Solution: UKULIMA SAFI ')
    pdf.chapter_body('Ukulima Safi is not just an app; it is an Agronomic Decision Support System (ADSS) that operates in three layers:')

    pdf.sub_section('A. The Diagnostic Layer (The Eye)')
    pdf.bullet_point('AI-Powered Detection: Utilizing advanced Deep Learning (MobileNetV2 Architecture), the system detects diseases in Maize, Beans, Wheat, Rice, and more with >92% accuracy.')
    pdf.bullet_point('Offline Capability: Critical for rural penetration, the core diagnostic engine runs locally on the device without requiring internet access.')
    pdf.bullet_point('Expert Verification (Human-in-the-Loop): A dedicated portal allows professional agronomists to validate AI findings, ensuring the model constantly retrains and adapts to local mutations.')

    pdf.sub_section('B. The Logic Layer (The Brain)')
    pdf.bullet_point('Smart Weather Integration: Connects with satellite data to provide "Spray/No-Spray" advice, reducing chemical wastage and environmental runoff.')
    pdf.bullet_point('Precision Tools: Includes calculators for Irrigation Scheduling, Carbon Sequestration tracking, and Market Price Forecasting, enabling farmers to transition from subsistence to commercial farming.')

    pdf.sub_section('C. The Connectivity Layer (The Hand)')
    pdf.bullet_point('GPS Resource Locator: Automatically guides farmers to the nearest registered Agrovets and Agronomists. For industry partners, this ensures their products are accessible to the farmers who need them immediately after a diagnosis.')
    pdf.bullet_point('Community Hub: A monitored forum for peer-to-peer learning and expert intervention.')
    pdf.ln(3)

    # --- 4. Value Proposition ---
    pdf.chapter_title('4', 'Value Proposition for Industry Partners')
    
    pdf.sub_section('For Chemical & Input Companies:')
    pdf.bullet_point('Precision Marketing: When the AI detects Fall Armyworm in a specific region, your specific pesticide is recommended immediately as the solution.')
    pdf.bullet_point('Product Stewardship: Ensure farmers use chemicals correctly based on weather data, reducing liability and improving efficacy.')

    pdf.sub_section('For Contract Farming & Aggregators:')
    pdf.bullet_point('Remote Monitoring: Track the growth stage (Seedling vs. Fruiting) of thousands of out-growers instantly.')
    pdf.bullet_point('Yield Prediction: Use our aggregated data to forecast harvest volumes and market prices months in advance.')

    pdf.sub_section('For NGOs & Government Bodies:')
    pdf.bullet_point('Early Warning System: Detect disease outbreaks (e.g., Maize Lethal Necrosis) in real-time on a heatmap before they become epidemics.')
    pdf.bullet_point('Sustainability Goals: Use our Carbon Tracker to quantify and monetize sustainable farming practices.')
    pdf.ln(3)

    # --- 5. Technical Architecture ---
    pdf.chapter_title('5', 'Technical Architecture & Scalability')
    pdf.chapter_body('Ukulima Safi is built on a robust, scalable stack designed for reliability:')
    
    pdf.bullet_point('Frontend: Responsive, mobile-first design (iOS/Android/Desktop) ensuring accessibility on low-end devices.')
    pdf.bullet_point('Backend: Python/Flask architecture with TensorFlow for high-speed inference.')
    pdf.bullet_point('Data: Firebase Realtime Database for community interactions and synchronous updates.')
    pdf.bullet_point('Security: Enterprise-grade data handling with geolocation privacy protocols.')
    pdf.ln(3)

    # --- 6. Conclusion ---
    pdf.chapter_title('6', 'Conclusion & Call to Action')
    pdf.chapter_body(
        'The future of agriculture is data-driven. UKULIMA SAFI AI offers the infrastructure to digitize '
        'the agricultural value chain from soil to market. We invite partners to pilot this technology, '
        'integrate their networks, and drive the next Green Revolution together.'
    )
    pdf.ln(10)

    # --- Contact Info ---
    pdf.set_draw_color(0, 100, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Contact Information:', 0, 1)
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, 'Delstaford Isaiah', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 6, 'Lead Developer & Architect', 0, 1)
    pdf.cell(0, 6, 'DELSTARFORD WORKS.CO.KE', 0, 1)
    pdf.cell(0, 6, 'Kakamega, Kenya', 0, 1)
    pdf.cell(0, 6, 'Email:  delstarfordisaiah@gmail.com', 0, 1)
    pdf.cell(0, 6, 'Phone: 0707605751', 0, 1)

    # Output
    try:
        pdf.output('Ukulima Safi .pdf')
        print("Success! PDF generated as 'Ukulima_Safi_Concept_Note.pdf'")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    generate_pdf()