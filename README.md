# Wikipedia Death Tracker

This is a small Python script that checks if a person (with a Wikipedia article) has passed away by scraping their infobox.

## Features
- Fetches and parses Wikipedia pages for given names.
- Extracts the **Died** field if present in the infobox.
- Saves results (date, age, location) in a JSON file.
- Handles cases where the person is still alive.

## Requirements
- Python 3.x
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
1. Clone the repository
   ```bash
   git clone https://github.com/Alfrazgit/Obituary-Chronicle.git
   cd wikipedia-death-tracker
   ```

2. Run the script
   ```bash
   python main.py
   ```

3. Enter a name (capitalization handled automatically).  
   Example:
   ```
   Whose death do you wish to know of? $>adolf hitler
   30 April 1945(1945-04-30)(aged 56)Berlin, Germany
   ```

If no **Died** field exists, the program will print:
```
NOT DEAD YET THANK YOU VERY MUCH!
```
###### and stores the data fields as `null`

## Notes
- This script is for educational purposes only.  
- Be mindful of Wikipedia’s terms of use and scraping etiquette.  
- Use caching to avoid repeated unnecessary requests.

