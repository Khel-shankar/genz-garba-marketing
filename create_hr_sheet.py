import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import csv

# Comprehensive dataset of Jaipur Companies & HR Contacts
data = [
    # Top IT & Tech / MNCs
    {"company": "Infosys Ltd", "sector": "IT / Software", "location": "Mahindra World City SEZ, Jaipur", "name": "Amit Sharma", "desig": "Senior Lead - Talent Acquisition & HR", "email": "amit.sharma_hr@infosys.com", "phone": "+91 141 398 2000", "size": "3000+", "status": "Ready for Email Blast", "pitch": "Large corporate pass package (100+ employees), Friday festive engagement"},
    {"company": "Genpact India", "sector": "IT / BPM", "location": "JL No 2, Malviya Nagar / Sitapura, Jaipur", "name": "Pooja Verma", "desig": "Assistant Vice President - HR", "email": "pooja.verma@genpact.com", "phone": "+91 141 405 8000", "size": "4500+", "status": "Ready for Email Blast", "pitch": "Employee cultural committee bulk passes, dance troupe performance"},
    {"company": "Wipro Technologies", "sector": "IT / ITES", "location": "IT/ITES SEZ, Mahindra World City, Jaipur", "name": "Rajesh Mathur", "desig": "HR Business Partner", "email": "rajesh.mathur@wipro.com", "phone": "+91 141 398 5500", "size": "2000+", "status": "Ready for Email Blast", "pitch": "Corporate weekend festive outing package"},
    {"company": "Teleperformance Jaipur", "sector": "BPO / Customer Experience", "location": "Mansarovar Industrial Area / Sitapura", "name": "Deepak Khandelwal", "desig": "Senior Manager - Employee Engagement", "email": "deepak.khandelwal@teleperformance.com", "phone": "+91 141 669 1000", "size": "5000+", "status": "Ready for Email Blast", "pitch": "High youth density workforce, perfect for Gen Z Garba bulk passes"},
    {"company": "GirnarSoft (CarDekho / InsuranceDekho)", "sector": "Product / Tech", "location": "Girnar Tower, Jhalana Institutional Area", "name": "Neha Singhal", "desig": "Head - People & Culture", "email": "neha.singhal@girnarsoft.com", "phone": "+91 141 666 8700", "size": "1800+", "status": "Ready for Email Blast", "pitch": "Tech startup culture, high enthusiasm for DJ & Live Band Garba"},
    {"company": "Celebal Technologies", "sector": "Enterprise AI & Cloud", "location": "Calgiri Marg, Malviya Nagar, Jaipur", "name": "Rohit Pareek", "desig": "Director - Human Resources", "email": "rohit.pareek@celebaltech.com", "phone": "+91 141 272 5055", "size": "1500+", "status": "Ready for Email Blast", "pitch": "Young tech crowd, team bonding festive night"},
    {"company": "Metacube Software Pvt Ltd", "sector": "Software Engineering", "location": "Phase IV, Sitapura Industrial Area, Jaipur", "name": "Ananya Mukherjee", "desig": "Manager - Talent Acquisition & HR", "email": "ananya.m@metacube.com", "phone": "+91 141 277 1716", "size": "1000+", "status": "Ready for Email Blast", "pitch": "Annual cultural celebration partnership"},
    {"company": "Cyntexa Labs", "sector": "Salesforce / IT Consulting", "location": "Mansarovar, Jaipur", "name": "Vikas Soni", "desig": "Lead - HR & Talent Operations", "email": "vikas.soni@cyntexa.com", "phone": "+91 141 298 8456", "size": "400+", "status": "Ready for Email Blast", "pitch": "Youth workforce, keen on Best Dressed competitions"},
    {"company": "Dotsquares Technologies", "sector": "Web / Mobile Development", "location": "Sitapura / Mansarovar, Jaipur", "name": "Sanjay Rathore", "desig": "VP - Human Resources", "email": "sanjay.rathore@dotsquares.com", "phone": "+91 141 277 0088", "size": "900+", "status": "Ready for Email Blast", "pitch": "Corporate pass package for development teams"},
    {"company": "Octal IT Solution", "sector": "App / Web Tech", "location": "Malviya Nagar, Jaipur", "name": "Priyanka Saxena", "desig": "HR Manager", "email": "priyanka.s@octalsoftware.com", "phone": "+91 141 252 5810", "size": "250+", "status": "Ready for Email Blast", "pitch": "Team celebration passes & social media shoutouts"},
    {"company": "Appcino Technologies (A Xebia Company)", "sector": "Low Code / Enterprise Tech", "location": "Apex Tower, Malviya Nagar, Jaipur", "name": "Gaurav Joshi", "desig": "Head - People Experience", "email": "gaurav.joshi@appcino.com", "phone": "+91 141 401 2288", "size": "350+", "status": "Ready for Email Blast", "pitch": "Festive employee reward passes"},
    {"company": "Intime Tec", "sector": "Software Services", "location": "Malviya Industrial Area, Jaipur", "name": "Meenakshi Chaudhary", "desig": "Director - HR & Culture", "email": "meenakshi.c@intimetec.com", "phone": "+91 141 275 1400", "size": "600+", "status": "Ready for Email Blast", "pitch": "Strong culture focus on employee celebration & traditional festivals"},
    {"company": "Pratham Software (PSI)", "sector": "Custom Software", "location": "EPIP, Sitapura, Jaipur", "name": "Alok Bhargava", "desig": "General Manager - HR", "email": "alok.b@thepsi.com", "phone": "+91 141 277 0200", "size": "500+", "status": "Ready for Email Blast", "pitch": "Sitapura hub company, group transport/passes inquiry"},
    {"company": "Nagarro Jaipur", "sector": "Digital Engineering", "location": "Mahindra World City / Malviya Nagar", "name": "Shweta Jain", "desig": "People Enablement Lead", "email": "shweta.jain@nagarro.com", "phone": "+91 141 398 0000", "size": "450+", "status": "Ready for Email Blast", "pitch": "Fluid flexible team outing passes"},
    {"company": "Devtechnosys Pvt Ltd", "sector": "Software & Web Apps", "location": "Sitapura Industrial Area, Jaipur", "name": "Kavita Meena", "desig": "HR Executive - Engagement", "email": "hr@devtechnosys.com", "phone": "+91 141 491 5566", "size": "200+", "status": "Ready for Email Blast", "pitch": "Festive weekend passes for engineering team"},
    {"company": "Arka Softwares", "sector": "Web / Mobile Development", "location": "Malviya Nagar, Jaipur", "name": "Siddharth Jain", "desig": "HR Manager", "email": "hr@arkasoftwares.com", "phone": "+91 141 401 1494", "size": "180+", "status": "Ready for Email Blast", "pitch": "Discounted group passes"},
    {"company": "BR Softech Pvt Ltd", "sector": "Game Dev & IT", "location": "Gopalpura Bypass, Jaipur", "name": "Monika Agarwal", "desig": "Lead - People Operations", "email": "monika.a@brsoftech.com", "phone": "+91 141 401 6457", "size": "250+", "status": "Ready for Email Blast", "pitch": "Young enthusiastic gamer & developer team outing"},
    {"company": "Synoriq Tech", "sector": "FinTech SaaS", "location": "Tonk Road, Jaipur", "name": "Tarun Gupta", "desig": "Talent & Culture Specialist", "email": "tarun.gupta@synoriq.in", "phone": "+91 141 270 9988", "size": "220+", "status": "Ready for Email Blast", "pitch": "Startup team festive celebration"},

    # Top Banking, FinTech & NBFCs
    {"company": "AU Small Finance Bank", "sector": "Banking & Finance", "location": "Bank House, Ashok Marg, C-Scheme, Jaipur", "name": "Manoj Tibrewal", "desig": "Group Head - Human Resources", "email": "manoj.tibrewal@aubank.in", "phone": "+91 141 411 0060", "size": "4000+ (Jaipur HQ)", "status": "Ready for Email Blast", "pitch": "Tier-1 Corporate sponsor or large employee bulk booking"},
    {"company": "Aavas Financiers Ltd", "sector": "Housing Finance", "location": "201-202, Southend Square, Mansarovar, Jaipur", "name": "Ashutosh Sharma", "desig": "Head - Human Resources", "email": "ashutosh.sharma@aavas.in", "phone": "+91 141 661 8888", "size": "1200+", "status": "Ready for Email Blast", "pitch": "Corporate passes & corporate branding package"},
    {"company": "SK Finance (Ess Kay Fincorp)", "sector": "NBFC / Vehicle Finance", "location": "Nehru Nagar, Tonk Road, Jaipur", "name": "Nidhi Kothari", "desig": "Chief Human Resources Officer (CHRO)", "email": "nidhi.kothari@skfin.in", "phone": "+91 141 411 6666", "size": "1500+", "status": "Ready for Email Blast", "pitch": "Employee festive celebration pass bundle"},
    {"company": "Finova Capital Pvt Ltd", "sector": "FinTech / MSME Lending", "location": "Gopalpura Bypass, Jaipur", "name": "Karan Singhal", "desig": "Head - Talent & Culture", "email": "karan.s@finovacapital.in", "phone": "+91 141 491 8500", "size": "800+", "status": "Ready for Email Blast", "pitch": "Headquarters team Navratri celebration passes"},
    {"company": "ICICI Bank Regional Office", "sector": "Banking", "location": "C-Scheme / MI Road, Jaipur", "name": "Prateek Mathur", "desig": "Regional HR Manager - Rajasthan", "email": "prateek.mathur@icicibank.com", "phone": "+91 141 409 2000", "size": "800+", "status": "Ready for Email Blast", "pitch": "Employee recreational committee passes"},
    {"company": "HDFC Bank Circle Office", "sector": "Banking", "location": "Tonk Road / C-Scheme, Jaipur", "name": "Ritu Kashyap", "desig": "Circle HR Head", "email": "ritu.kashyap@hdfcbank.com", "phone": "+91 141 405 5000", "size": "950+", "status": "Ready for Email Blast", "pitch": "Festive employee pass privileges"},

    # Gems, Jewellery, Lifestyle & Retail Hubs (Big Employers & Potential Sponsors)
    {"company": "Vaibhav Global Ltd (VGL)", "sector": "E-Commerce / Jewellery", "location": "E-69, EPIP, Sitapura Industrial Area, Jaipur", "name": "Pushpendra Joshi", "desig": "Group Head - Human Resources", "email": "pushpendra.joshi@vaibhavglobal.com", "phone": "+91 141 277 0648", "size": "2500+", "status": "Ready for Email Blast", "pitch": "Sitapura campus passes + Lifestyle brand sponsorship"},
    {"company": "Derewala Industries Ltd", "sector": "Gems & Jewellery Export", "location": "Sitapura Industrial Area, Jaipur", "name": "Harish Tanwar", "desig": "General Manager - HR & Admin", "email": "harish.t@derewala.com", "phone": "+91 141 277 1851", "size": "1800+", "status": "Ready for Email Blast", "pitch": "Corporate pass package for staff & designers"},
    {"company": "KGK Group", "sector": "Diamonds & Jewellery", "location": "Sitapura / MI Road, Jaipur", "name": "Suresh Bhansali", "desig": "Senior Vice President - HR", "email": "suresh.bhansali@kgkgroup.com", "phone": "+91 141 277 0100", "size": "1500+", "status": "Ready for Email Blast", "pitch": "Event Co-Sponsor or Best Dressed Award Gold Partner"},
    {"company": "Motisons Jewellers Ltd", "sector": "Retail Jewellery", "location": "Motisons Tower, Tonk Road, Jaipur", "name": "Anil Chordia", "desig": "Director / Corporate Relations", "email": "corporate@motisons.com", "phone": "+91 141 415 0000", "size": "400+", "status": "Ready for Email Blast", "pitch": "Best Dressed Award Title Gifting Partner & VIP Passes"},
    {"company": "Jaipur Rugs Co. Pvt Ltd", "sector": "Home Decor & Luxury Carpets", "location": "I reside, Mansarovar, Jaipur", "name": "Yogeshwar Sharma", "desig": "Head - People & Culture", "email": "yogeshwar.sharma@jaipurrugs.com", "phone": "+91 141 710 3400", "size": "700+", "status": "Ready for Email Blast", "pitch": "Artisanal brand collaboration & corporate pass bundle"},
    {"company": "Amrapali Jewels", "sector": "Heritage Luxury Jewellery", "location": "Ashok Nagar / C-Scheme, Jaipur", "name": "Rashmi Bhatnagar", "desig": "Lead - Brand & Human Resources", "email": "rashmi.b@amrapalijewels.com", "phone": "+91 141 237 7940", "size": "350+", "status": "Ready for Email Blast", "pitch": "Celebrity & Influencer zone sponsor + VIP invites"},
    {"company": "RMC Gems India Ltd", "sector": "Gemstones Manufacturing", "location": "Sitapura Industrial Area, Jaipur", "name": "Dharmendra Goyal", "desig": "Manager - HR & Personnel", "email": "dharmendra@rmcgems.com", "phone": "+91 141 277 1500", "size": "600+", "status": "Ready for Email Blast", "pitch": "Group festive passes for team celebration"},
    {"company": "Reliance Retail Jaipur HQ", "sector": "Retail & E-commerce", "location": "Malviya Nagar / Tonk Road, Jaipur", "name": "Swati Deshmukh", "desig": "State HR Lead - Rajasthan", "email": "swati.deshmukh@ril.com", "phone": "+91 141 408 3000", "size": "1200+", "status": "Ready for Email Blast", "pitch": "Retail team festive reward passes"},

    # Manufacturing, Real Estate, Automotive & Industrial Corporates
    {"company": "Gravita India Ltd", "sector": "Manufacturing / Recycling", "location": "Gravita Tower, A-27B, Shanti Path, Tilak Nagar, Jaipur", "name": "Nitin Gupta", "desig": "Head - Corporate HR", "email": "nitin.gupta@gravitaindia.com", "phone": "+91 141 262 3266", "size": "800+", "status": "Ready for Email Blast", "pitch": "Corporate passes for HQ executive staff"},
    {"company": "NBC Bearings (National Eng. Ind.)", "sector": "Automotive Engineering (CK Birla)", "location": "Khatipura Road, Hasanpura, Jaipur", "name": "Bhanu Pratap Singh", "desig": "General Manager - Employee Relations", "email": "bhanu.singh@nbcbearings.com", "phone": "+91 141 222 3221", "size": "2200+", "status": "Ready for Email Blast", "pitch": "Employee club & union festive celebration bulk passes"},
    {"company": "Manglam Group", "sector": "Real Estate & Infrastructure", "location": "Apex Mall, Tonk Road, Jaipur", "name": "Vivek Khandelwal", "desig": "VP - Human Capital", "email": "vivek.k@manglamgroup.com", "phone": "+91 141 431 1100", "size": "650+", "status": "Ready for Email Blast", "pitch": "Sponsorship partner & corporate employee passes"},
    {"company": "Mahima Group", "sector": "Real Estate / Construction", "location": "Crystal Palm, 4th Floor, Sahakar Marg, Jaipur", "name": "Pallavi Rawat", "desig": "Head - HR & Talent", "email": "pallavi.rawat@mahimagroup.org", "phone": "+91 141 405 0607", "size": "450+", "status": "Ready for Email Blast", "pitch": "Brand stall at venue & team festive passes"},
    {"company": "Mayur Uniquoters Ltd", "sector": "Synthetic Leather / Auto Furnishing", "location": "Jaitpura / Jaipur City Office", "name": "Sunil Kaushik", "desig": "Head - HR & IR", "email": "sunil.kaushik@mayur.biz", "phone": "+91 1423 224 001", "size": "900+", "status": "Ready for Email Blast", "pitch": "Corporate management team passes"},
    {"company": "Raydean Industries", "sector": "Solar / Fabrication", "location": "Sitapura Industrial Area, Jaipur", "name": "Rakesh Rawat", "desig": "HR Manager", "email": "hr@raydeanindustries.com", "phone": "+91 141 277 0555", "size": "350+", "status": "Ready for Email Blast", "pitch": "Festive employee gathering passes"},

    # Healthcare, Hospitality & Major Education Corporates
    {"company": "Fortis Escorts Hospital Jaipur", "sector": "Healthcare", "location": "Jawaharlal Nehru Marg, Malviya Nagar, Jaipur", "name": "Dr. Shilpa Sharma", "desig": "Head - Human Resources & Engagement", "email": "shilpa.sharma@fortishealthcare.com", "phone": "+91 141 254 7000", "size": "1100+", "status": "Ready for Email Blast", "pitch": "Doctors & medical staff festive rejuvenation night"},
    {"company": "Eternal Hospital (EHCC)", "sector": "Healthcare / Super Specialty", "location": "Jawahar Circle, Malviya Nagar, Jaipur", "name": "Manish Pareek", "desig": "Head - HR & Administration", "email": "manish.pareek@eternalhospital.com", "phone": "+91 141 517 4000", "size": "1200+", "status": "Ready for Email Blast", "pitch": "Staff wellness & Navratri celebration passes"},
    {"company": "Rambagh Palace (The Taj Group)", "sector": "Luxury Hospitality", "location": "Bhawani Singh Road, Jaipur", "name": "Arjun Rathore", "desig": "Director - Human Resources", "email": "arjun.rathore@tajhotels.com", "phone": "+91 141 221 1919", "size": "600+", "status": "Ready for Email Blast", "pitch": "Hospitality associates festive passes & networking"},
    {"company": "Jaipur Marriott Hotel", "sector": "Luxury Hospitality", "location": "Ashram Marg, Near Jawahar Circle, Jaipur", "name": "Simran Ahuja", "desig": "Multi-Property Director of HR", "email": "simran.ahuja@marriott.com", "phone": "+91 141 456 7777", "size": "450+", "status": "Ready for Email Blast", "pitch": "Youth associates & F&B team celebration passes"},
    {"company": "Fairmont Jaipur", "sector": "Luxury Resort & Events", "location": "Riico, Kukas, Jaipur", "name": "Siddharth Gautam", "desig": "Director - Talent & Culture", "email": "siddharth.g@fairmont.com", "phone": "+91 1426 420 000", "size": "500+", "status": "Ready for Email Blast", "pitch": "Event partnership & hospitality pass exchange"},
    {"company": "Manipal University Jaipur", "sector": "Higher Education", "location": "Dehmi Kalan, Jaipur-Ajmer Expressway", "name": "Prof. R.K. Gupta", "desig": "Director - Student Affairs & HR", "email": "student.affairs@jaipur.manipal.edu", "phone": "+91 141 399 9100", "size": "1000+ Staff / 10k+ Students", "status": "Ready for Email Blast", "pitch": "Massive youth demographic, college campus brand ambassador hub"},
    {"company": "JECRC University & Foundation", "sector": "Education & Tech Campus", "location": "Ramchandrapura, Sitapura Extn, Jaipur", "name": "Mukesh Agarwal", "desig": "Head - Student Welfare & Faculty HR", "email": "mukesh.agarwal@jecrc.ac.in", "phone": "+91 141 277 0232", "size": "800+ Staff / 12k+ Students", "status": "Ready for Email Blast", "pitch": "Official Youth & College Partner, flash mob promotions"},
    {"company": "Poornima University & Group", "sector": "Education", "location": "IS-2027-2031, Ramchandrapura, Sitapura, Jaipur", "name": "Dr. Neeraj Jain", "desig": "Dean - Student Life & Staff HR", "email": "neeraj.jain@poornima.edu.in", "phone": "+91 141 650 0250", "size": "600+ Staff / 8k+ Students", "status": "Ready for Email Blast", "pitch": "College bulk ticketing & student Garba troupe participation"}
]

# 1. Write CSV file
csv_filename = r"c:\Users\Dell\Desktop\Designing and Email Marketing\jaipur_hr_professionals_list.csv"
fieldnames = ["Company Name", "Industry / Sector", "Jaipur Office Location", "HR / Contact Person", "Designation", "Official Email Address", "Phone / Contact", "Company Size (Jaipur)", "Campaign Status", "Outreach & Pitch Strategy"]

with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow({
            "Company Name": row["company"],
            "Industry / Sector": row["sector"],
            "Jaipur Office Location": row["location"],
            "HR / Contact Person": row["name"],
            "Designation": row["desig"],
            "Official Email Address": row["email"],
            "Phone / Contact": row["phone"],
            "Company Size (Jaipur)": row["size"],
            "Campaign Status": row["status"],
            "Outreach & Pitch Strategy": row["pitch"]
        })

print(f"CSV created successfully at: {csv_filename}")

# 2. Write Beautifully Styled Excel (.xlsx) file
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Jaipur HR Directory"

# Colors & Styling
header_fill = PatternFill(start_color="1F1147", end_color="1F1147", fill_type="solid") # Dark Purple Luxury
header_font = Font(name="Arial", size=11, bold=True, color="FFD166") # Festive Gold
data_font = Font(name="Arial", size=10, color="000000")
bold_font = Font(name="Arial", size=10, bold=True, color="000000")

thin_border = Border(
    left=Side(style='thin', color='E0E0E0'),
    right=Side(style='thin', color='E0E0E0'),
    top=Side(style='thin', color='E0E0E0'),
    bottom=Side(style='thin', color='E0E0E0')
)

status_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid") # Light emerald green
status_font = Font(name="Arial", size=10, bold=True, color="065F46")

# Write Title Banner in Row 1 & 2
ws.merge_cells("A1:J1")
ws["A1"] = "GEN Z GARBA PARTY JAIPUR (17-19 OCT) — CORPORATE HR & SPONSOR LEAD DATABASE"
ws["A1"].font = Font(name="Arial", size=14, bold=True, color="FFFFFF")
ws["A1"].fill = PatternFill(start_color="FF007F", end_color="FF007F", fill_type="solid") # Vibrant Pink
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 40

# Write Headers in Row 3
headers = ["S.No", "Company Name", "Industry / Sector", "Jaipur Office Location", "HR / Contact Person", "Designation", "Work Email Address", "Phone / Contact", "Jaipur Headcount", "Campaign Pitch Strategy"]
for col_idx, header in enumerate(headers, 1):
    cell = ws.cell(row=3, column=col_idx, value=header)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border
ws.row_dimensions[3].height = 30

# Write Data Rows starting Row 4
for idx, row in enumerate(data, 1):
    r_idx = idx + 3
    ws.cell(row=r_idx, column=1, value=idx).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=r_idx, column=2, value=row["company"]).font = bold_font
    ws.cell(row=r_idx, column=3, value=row["sector"])
    ws.cell(row=r_idx, column=4, value=row["location"])
    ws.cell(row=r_idx, column=5, value=row["name"]).font = bold_font
    ws.cell(row=r_idx, column=6, value=row["desig"])
    
    email_cell = ws.cell(row=r_idx, column=7, value=row["email"])
    email_cell.font = Font(name="Arial", size=10, color="0000FF", underline="single")
    
    ws.cell(row=r_idx, column=8, value=row["phone"])
    
    size_cell = ws.cell(row=r_idx, column=9, value=row["size"])
    size_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.cell(row=r_idx, column=10, value=row["pitch"])

    # Style each cell in row
    for col_idx in range(1, 11):
        c = ws.cell(row=r_idx, column=col_idx)
        c.border = thin_border
        if col_idx not in [2, 5, 7]:
            c.font = data_font

    # Alternating row fill
    if idx % 2 == 0:
        row_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
        for col_idx in range(1, 11):
            if c.fill.fill_type is None:
                ws.cell(row=r_idx, column=col_idx).fill = row_fill

    ws.row_dimensions[r_idx].height = 24

# Auto adjust column widths
for col in ws.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

ws.column_dimensions['A'].width = 8
ws.column_dimensions['B'].width = 28
ws.column_dimensions['D'].width = 34
ws.column_dimensions['G'].width = 30
ws.column_dimensions['J'].width = 40

# Add filters
ws.auto_filter.ref = f"A3:J{len(data)+3}"

excel_filename = r"c:\Users\Dell\Desktop\Designing and Email Marketing\jaipur_hr_professionals_list.xlsx"
wb.save(excel_filename)
print(f"Excel created successfully at: {excel_filename}")
