file_path = "InsuranceData_Test.xlsx"

from openpyxl import load_workbook

print("i am inside this rough notebook")
# Load the Excel workbook
wb = load_workbook(file_path)

# Select the active worksheet
# Get data from row 3
sheet = wb.active

for i in range(3,16):
    row_data = [cell.value for idx, cell in enumerate(sheet[i], start=1) if idx != 6]  # sheet[3] gets all cells in row 3
    print(row_data) 


