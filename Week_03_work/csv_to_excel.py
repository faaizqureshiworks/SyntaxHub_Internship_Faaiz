import pandas as pd
import os

def clean_and_convert_csv(csv_path, excel_path):
    print("⏳ Reading CSV file...")
    
    # 1. Read the CSV file
    if not os.path.exists(csv_path):
        print(f"❌ Error: The file {csv_path} does not exist!")
        return

    df = pd.read_csv(csv_path)
    print("\n📊 Original Data Received:")
    print(df)

    print("\n🧹 Starting Data Cleaning Process...")

    # 2. Remove exact duplicate rows
    df.drop_duplicates(inplace=True)
    print("  -> Removed duplicate rows.")

    # 3. Clean up text/string data columns (Strip spaces and capitalize properly)
    if 'Name' in df.columns:
        df['Name'] = df['Name'].astype(str).str.strip().str.title()
        print("  -> Normalized text formatting (Capitalized names & stripped extra spaces).")

    # 4. Handle missing/null values
    # Fill missing numeric values with a default indicator or average, or leave blank cleanly
    df.fillna({"Age": "N/A"}, inplace=True)
    print("  -> Handled missing values (Replaced blanks in Age with 'N/A').")

    print("\n🚀 Exporting cleaned data to Excel...")

    # 5. Export cleanly to Excel using openpyxl engine
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        
        # Access the openpyxl workbook objects to apply basic layout styles auto-adjusting column widths
        workbook  = writer.book
        worksheet = writer.sheets['Cleaned Data']
        
        for col in worksheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    print(f"\n✅ Success! Cleaned file saved to: {excel_path}")

def main():
    # Changed paths because your terminal is already inside Week_03_work
    input_csv = "sample_data.csv"
    output_excel = "cleaned_report.xlsx"
    
    print("--- CSV to Excel Converter & Data Cleaner ---")
    clean_and_convert_csv(input_csv, output_excel)\
        
if __name__ == "__main__":
    main()