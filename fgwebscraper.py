# webscraping and download data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
import sys

# Add MLB team logos dictionary
team_logos = {
    'ARI': 'https://www.mlbstatic.com/team-logos/109.svg',
    'ATL': 'https://www.mlbstatic.com/team-logos/144.svg',
    'BAL': 'https://www.mlbstatic.com/team-logos/110.svg',
    'BOS': 'https://www.mlbstatic.com/team-logos/111.svg',
    'CHC': 'https://www.mlbstatic.com/team-logos/112.svg',
    'CWS': 'https://www.mlbstatic.com/team-logos/145.svg',
    'CIN': 'https://www.mlbstatic.com/team-logos/113.svg',
    'CLE': 'https://www.mlbstatic.com/team-logos/114.svg',
    'COL': 'https://www.mlbstatic.com/team-logos/115.svg',
    'DET': 'https://www.mlbstatic.com/team-logos/116.svg',
    'HOU': 'https://www.mlbstatic.com/team-logos/117.svg',
    'KC': 'https://www.mlbstatic.com/team-logos/118.svg',
    'LAA': 'https://www.mlbstatic.com/team-logos/108.svg',
    'LAD': 'https://www.mlbstatic.com/team-logos/119.svg',
    'MIA': 'https://www.mlbstatic.com/team-logos/146.svg',
    'MIL': 'https://www.mlbstatic.com/team-logos/158.svg',
    'MIN': 'https://www.mlbstatic.com/team-logos/142.svg',
    'NYM': 'https://www.mlbstatic.com/team-logos/121.svg',
    'NYY': 'https://www.mlbstatic.com/team-logos/147.svg',
    'OAK': 'https://www.mlbstatic.com/team-logos/133.svg',
    'PHI': 'https://www.mlbstatic.com/team-logos/143.svg',
    'PIT': 'https://www.mlbstatic.com/team-logos/134.svg',
    'SD': 'https://www.mlbstatic.com/team-logos/135.svg',
    'SF': 'https://www.mlbstatic.com/team-logos/137.svg',
    'SEA': 'https://www.mlbstatic.com/team-logos/136.svg',
    'STL': 'https://www.mlbstatic.com/team-logos/138.svg',
    'TB': 'https://www.mlbstatic.com/team-logos/139.svg',
    'TEX': 'https://www.mlbstatic.com/team-logos/140.svg',
    'TOR': 'https://www.mlbstatic.com/team-logos/141.svg',
    'WSH': 'https://www.mlbstatic.com/team-logos/120.svg'
}

current_date = datetime.now().strftime('%m%d')

##### LOAD WEBDRIVER TO BEGIN BUILDING WEBSCRAPER FOR FANGRAPHS #####
chrome_options = Options()
download_dir = r"C:\path\to\directory"

prefs = {"download.default_directory": download_dir,
         "download.prompt_for_download": False,
         "download.directory_upgrade": True,
         "safebrowsing.enabled": True}

chrome_options.add_experimental_option("prefs", prefs)

# setup chrome webdriver
driver_path = r"C:\path\to\directory\with\driver"
driver = webdriver.Chrome(executable_path=driver_path, options = chrome_options)

# open fangraphs sign in page
driver.get('https://blogs.fangraphs.com/wp-login.php?redirect_to=https://www.fangraphs.com/')

# locate username and password field
username_field = driver.find_element('id', 'user_login')
password_field = driver.find_element('id', 'user_pass')

username_field.send_keys('username')
password_field.send_keys('password')

password_field.send_keys(Keys.RETURN)
# wait for login to complete
time.sleep(5)

# List URL's to navigate to
urls = {'Batters - Full Season': 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&season=2024&season1=2024&ind=0&type=c%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C16%2C21%2C22%2C23%2C34%2C35%2C37%2C38%2C39%2C40%2C43%2C44%2C45%2C47%2C211%2C308%2C311&month=33&qual=50&v_cr=202301',
        'Batters - Last 30': 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&season=2024&season1=2024&ind=0&v_cr=202301&type=c%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C16%2C21%2C22%2C23%2C34%2C35%2C37%2C38%2C39%2C40%2C43%2C44%2C45%2C47%2C211%2C308%2C311&month=3&qual=30',
        'Batters - Last 14': 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&season=2024&season1=2024&ind=0&v_cr=202301&type=c%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C16%2C21%2C22%2C23%2C34%2C35%2C37%2C38%2C39%2C40%2C43%2C44%2C45%2C47%2C211%2C308%2C311&month=2&qual=20',
        'Batters - Last 7': 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&season=2024&season1=2024&ind=0&v_cr=202301&type=c%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C16%2C21%2C22%2C23%2C34%2C35%2C37%2C38%2C39%2C40%2C43%2C44%2C45%2C47%2C211%2C308%2C311&month=1&qual=10',
        'Pitchers - Full Season': 'https://www.fangraphs.com/leaders/major-league?pos=all&lg=all&season=2024&season1=2024&ind=0&sortcol=14&sortdir=desc&stats=sta&v_cr=202301&type=c%2C4%2C5%2C7%2C8%2C13%2C6%2C45%2C15%2C18%2C47%2C48%2C49%2C51%2C120%2C121%2C329%2C324%2C325%2C327%2C328&month=33&qual=30',
        'Pitchers - Last 30': 'https://www.fangraphs.com/leaders/major-league?pos=all&lg=all&season=2024&season1=2024&ind=0&sortcol=14&sortdir=desc&stats=sta&v_cr=202301&type=c%2C4%2C5%2C7%2C8%2C13%2C6%2C45%2C15%2C18%2C47%2C48%2C49%2C51%2C120%2C121%2C329%2C324%2C325%2C327%2C328&month=3&qual=20',
        'Pitchers - Last 14': 'https://www.fangraphs.com/leaders/major-league?pos=all&lg=all&season=2024&season1=2024&ind=0&sortcol=14&sortdir=desc&stats=sta&v_cr=202301&type=c%2C4%2C5%2C7%2C8%2C13%2C6%2C45%2C15%2C18%2C47%2C48%2C49%2C51%2C120%2C121%2C329%2C324%2C325%2C327%2C328&month=2&qual=5',
        'Pitchers - Last 7': 'https://www.fangraphs.com/leaders/major-league?pos=all&lg=all&season=2024&season1=2024&ind=0&sortcol=14&sortdir=desc&stats=sta&v_cr=202301&type=c%2C4%2C5%2C7%2C8%2C13%2C6%2C45%2C15%2C18%2C47%2C48%2C49%2C51%2C120%2C121%2C329%2C324%2C325%2C327%2C328&month=1&qual=1',
        'Probable Starters': 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=0&type=8&season=2024&month=0&season1=2024&ind=0&team=0&rost=0&age=0&filter=&players=p2024-09-18'
        }


# New function to create team logos sheet
def create_team_logos_sheet(writer):
    """
    Creates a new sheet in the Excel workbook containing team abbreviations and their logo URLs.
    
    Parameters:
    writer (pd.ExcelWriter): The Excel writer object to add the sheet to
    """
    # Create DataFrame from team_logos dictionary
    logos_df = pd.DataFrame(list(team_logos.items()), columns=['Team', 'Logo URL'])
    
    # Add the sheet to the workbook
    logos_df.to_excel(writer, sheet_name='Team Logos', index=False)
    
    return logos_df

##### CREATE EXCEL WRITER OBJECT TO POPULATE WORKBOOK WITH DATA #####
excel_path = os.path.join(download_dir, f'Fangraphs_Stats{current_date}.xlsx')

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    sheet_created = False

    # Add placeholder sheet initially
    placeholder_df = pd.DataFrame({"Notice": ["No data available"]})
    placeholder_df.to_excel(writer, sheet_name="Placeholder", index=False)

    # Add the team logos sheet first
    create_team_logos_sheet(writer)
    sheet_created = True

    # Iterate over each key-value pair in the dictionary
    for sheet_name, url in urls.items():
        try:
            print(f"Processing sheet: {sheet_name}, URL: {url}")
            
            # Navigate to the URL
            driver.get(url)
            time.sleep(3)

            if sheet_name == 'Probable Starters':
                scores_tab = driver.find_element(By.XPATH, "//div[@class='menu-item-label' and text()='Scores']")
                
                actions = ActionChains(driver)
                actions.move_to_element(scores_tab).perform()
                time.sleep(3)

                probable_pitchers_link = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Probable Pitchers')]"))
                )
                probable_pitchers_link.click()

            else:
                # Click the 'Export Data' button to download
                export = driver.find_element(By.XPATH, "//a[contains(text(), 'Export Data')]")
                export.click()
                time.sleep(3)

            # Find the latest file in the download directory
            list_of_files = os.listdir(download_dir)
            latest_file = max([os.path.join(download_dir, f) for f in list_of_files], key=os.path.getctime)
            print(f"Latest file found: {latest_file}")
            print(f"File size: {os.path.getsize(latest_file)} bytes")

            # Load the downloaded CSV file into a DataFrame
            df = pd.read_csv(latest_file)
            print(f"DataFrame shape for sheet '{sheet_name}': {df.shape}")

            if df is not None and not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                sheet_created = True
                
                if "Placeholder" in writer.book.sheetnames:
                    writer.book.remove(writer.book["Placeholder"])
                    print(f"Removed 'Placeholder' sheet after creating '{sheet_name}'.")

            os.remove(latest_file)

        except Exception as e:
            print(f"Error processing sheet {sheet_name}: {e}")

    if not sheet_created:
        print("No valid sheets were created; retaining placeholder sheet.")
    else:
        print("Workbook successfully created with valid sheets.")

driver.quit()

print(f"All datasets have been saved to {excel_path}")

# Define columns for formatting as percentages and with specified decimal places
formatting_rules = {
    'Batters - Full Season': {'percentage_columns': ['T', 'U', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'], 'decimal_columns': ['S', 'V', 'W', 'X', 'Y']},
    'Batters - Last 30': {'percentage_columns': ['T', 'U', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'], 'decimal_columns': ['S', 'V', 'W', 'X', 'Y']},
    'Batters - Last 14': {'percentage_columns': ['T', 'U', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'], 'decimal_columns': ['S', 'V', 'W', 'X', 'Y']},
    'Batters - Last 7': {'percentage_columns': ['T', 'U', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'], 'decimal_columns': ['S', 'V', 'W', 'X', 'Y']},
    'Pitchers - Full Season': {'percentage_columns': ['L', 'M', 'N', 'O', 'P', 'Q', 'T', 'V'], 'decimal_columns': ['H', 'I']},
    'Pitchers - Last 30': {'percentage_columns': ['L', 'M', 'N', 'O', 'P', 'Q', 'T', 'V'], 'decimal_columns': ['H', 'I']},
    'Pitchers - Last 14': {'percentage_columns': ['L', 'M', 'N', 'O', 'P', 'Q', 'T', 'V'], 'decimal_columns': ['H', 'I']},
    'Pitchers - Last 7': {'percentage_columns': ['L', 'M', 'N', 'O', 'P', 'Q', 'T', 'V'], 'decimal_columns': ['H', 'I']}
    }

# Create function that drops the last 3 columns from each sheet, converts specified columns to percentages, and changed number of places after decimal for all values
def format_workbook(workbook, formatting_rules, decimal_places=3):
    """
    Formats each sheet in the workbook according to the specified rules.
    
    Parameters:
    workbook (openpyxl.workbook.Workbook): The workbook to process
    formatting_rules (dict): Dictionary containing formatting rules for each sheet
    decimal_places (int): Number of decimal places for decimal columns
    """
    for sheet_name, rules in formatting_rules.items():
        try:
            ws = workbook[sheet_name]

            # Skip the last three columns deletion for Team Logos sheet
            if sheet_name != 'Team Logos':
                # Drop the last three columns
                for _ in range(3):
                    total_columns = ws.max_column
                    ws.delete_cols(total_columns)

            # Format specified columns as percentages
            for col_letter in rules.get('percentage_columns', []):
                for cell in ws[col_letter][1:]:  # Skip header row
                    if cell.value is not None:
                        cell.number_format = '0.00%'

            # Adjust decimal places for specified columns
            decimal_format = f'0.{"0"*decimal_places}'
            for col_letter in rules.get('decimal_columns', []):
                for cell in ws[col_letter][1:]:  # Skip header row
                    if cell.value is not None:
                        cell.number_format = decimal_format
        
        except KeyError:
            print(f"Warning: Sheet '{sheet_name}' not found in workbook")
        except Exception as e:
            print(f"Error formatting sheet '{sheet_name}': {e}")                   
                    
# Create variables to store arguments for function
      


def convert_to_table_and_autofit(workbook):
    """
    Converts each sheet to a table and auto-fits column widths.
    
    Parameters:
    workbook (openpyxl.workbook.Workbook): The workbook to process
    """
    for sheet_name in workbook.sheetnames:
        ws = workbook[sheet_name]

        # Define the table range
        table_range = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
        
        # Create a table object with a unique name (replace spaces and special characters)
        table_name = f"Table_{sheet_name.replace(' ', '_').replace('-', '_')}"
        table = Table(displayName=table_name, ref=table_range)
        
        # Apply a table style
        style = TableStyleInfo(
            name="TableStyleMedium9",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=True
        )
        table.tableStyleInfo = style
        
        # Add the table to the worksheet
        try:
            ws.add_table(table)
        except Exception as e:
            print(f"Warning: Could not create table for sheet '{sheet_name}': {e}")

        # Auto-fit columns
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            # Set the column width (minimum 8, maximum 50)
            adjusted_width = min(max(max_length + 2, 8), 50)
            ws.column_dimensions[column].width = adjusted_width

# Load the workbook and apply formatting
try:
    workbook = load_workbook(excel_path)
    format_workbook(workbook, formatting_rules, decimal_places=3)
    convert_to_table_and_autofit(workbook)
    workbook.save(excel_path)
    print("Workbook formatting completed successfully")
except Exception as e:
    print(f"Error during workbook formatting: {e}")
