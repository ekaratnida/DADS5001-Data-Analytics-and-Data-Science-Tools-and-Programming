
**Title: Developing a Python GUI App to Manipulate a Real-Time Supabase Database**

**Objective:** Create a Python desktop GUI application that interacts with a real-time database in Supabase. We will use PySimpleGUI for the GUI, and the `supabase-py` library for connecting and interacting with the Supabase database.

### Prerequisites

1. **Python Installed**: Make sure Python 3.8+ is installed.
2. **Supabase Account**: You must have a Supabase project already set up.
3. **Install Required Libraries**:

   Run the following command to install the necessary packages:
   ```bash
   pip install PySimpleGUI supabase-py
   ```
4. **Supabase Setup**: Your Supabase URL and API key, which can be found in the Supabase dashboard, are required.

### Step 1: Setting Up Supabase Connection

First, you need to set up a connection to your Supabase database using the `supabase-py` library.

```python
from supabase import create_client, Client

# Add your Supabase credentials here
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_API_KEY = "your-supabase-api-key"

# Create a Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
```

### Step 2: Create the GUI Layout with PySimpleGUI

We will create a simple GUI with PySimpleGUI that has options to add, update, and delete records from the Supabase database.

```python
import PySimpleGUI as sg

def add_record():
    name = values['-NAME-']
    age = values['-AGE-']
    if name and age:
        try:
            # Insert record into Supabase database
            response = supabase.table("users").insert({"name": name, "age": age},count="exact").execute()
            print(response)
            if response.count > 0:
                sg.popup("Success", "Record added successfully!")
            else:
                sg.popup("Error", "Failed to add record.")
        except Exception as e:
            sg.popup("Exception", str(e))
    else:
        sg.popup("Input Error", "Please provide both name and age.")

# Define the window layout
layout = [
    [sg.Text("Name"), sg.InputText(key='-NAME-')],
    [sg.Text("Age"), sg.InputText(key='-AGE-')],
    [sg.Button("Add Record", key='-ADD-')],
    [sg.Button("Fetch Records", key='-FETCH-')],
    [sg.Text("Records:")],
    [sg.Multiline(size=(40, 10), key='-OUTPUT-')],
   # [sg.Text("Record ID"), sg.InputText(key='-RECORD_ID-')],
    [sg.Button("Delete Record", key='-DELETE-')]
]

# Create the window
window = sg.Window("Supabase GUI Application", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == '-ADD-':
        add_record()
    elif event == '-FETCH-':
        try:
            # Fetch records from Supabase
            response = supabase.table("users").select("*").execute()
            records = response.data
            print(records)
            if records:
                display_text = "\n".join([f" {record['name']} - {record['age']}" for record in records])
                window['-OUTPUT-'].update(display_text)
            else:
                window['-OUTPUT-'].update("No records found.")
        except Exception as e:
            sg.popup("Exception", str(e))
    elif event == '-DELETE-':
        #record_id = values['-RECORD_ID-']
        name = values['-NAME-']
        if name:
            try:
                # Delete record from Supabase
                response = supabase.table("users").delete(count="exact").eq("name", name).execute()
                print(response)
                if response.count > 0:
                    sg.popup("Success", "Record deleted successfully!")
                else:
                    sg.popup("Error", "Failed to delete record.")
            except Exception as e:
                sg.popup("Exception", str(e))
        else:
            sg.popup("Input Error", "Please provide a name.")

# Close the window
window.close()
```

### Summary

1. **Connect** to the Supabase using the `supabase-py` client.
2. **Create a PySimpleGUI GUI** with options to add, update, delete, and fetch records from the real-time database.
3. **Interact** with the database through the GUI for real-time manipulation.

### Next Steps

- **Improve Error Handling**: Add more detailed error messages for different scenarios.
- **Data Validation**: Ensure that the inputs are sanitized.
- **Styling**: Improve the appearance of the PySimpleGUI GUI.

This tutorial should give you a solid foundation for creating a Python desktop app that works with a Supabase database. Feel free to customize the app with more fields or different types of data interactions!

![image](https://github.com/user-attachments/assets/cf062c6e-a266-4349-9f1e-1ce34aa6ed92)

