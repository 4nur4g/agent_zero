from datetime import date, timedelta

from browser_use.controller.service import Controller

from agent_zero.data import record
from common_python.utils.date_time import extract_date_parts
import os
tomorrow = date.today() + timedelta(days=1)


fgg_user_name = os.getenv("FGG_USER_ID")
fgg_password = os.getenv("FGG_PASSWORD")
expiry_date_object = extract_date_parts(record.Policy_Expiry_Date)
policy_start_date_object = extract_date_parts(record.Policy_Start_Date)

atomic_tasks_2 = [
    {
        "title": "Login to FG General Portal",
        "subtasks": [
            "Go to https://partners.fggeneral.in/nonlifeadvisor.",
            #"Go to file:///Users/rajivyadav/Desktop/FG_PAGE/Quote%20_%20Get%20Quote.html",
            "Locate the username input field labeled 'User ID'.",
            f"Enter the User ID using the value: {fgg_user_name}.",
            "Locate the password input field.",
            f"Enter the password using the value: {fgg_password}.",
            "Click the login button labeled 'Login'.",
            "Wait for 3 seconds to allow the page redirection to complete.",
            "wait until https://partners.fggeneral.in/home is loaded, that meaned you are logged in",
            "If the URL is not correct, report a login failure. Otherwise, confirm successful login."
        ],
        "use_vision": True
    },
    {
        "title": "Close Pop-ups, Modals, and Alerts",
        "subtasks": [
            "If any pop-up, modal, or alert appears, close it immediately.",
            "After closing, check for additional pop-ups and close them if present.",
            "Do not scroll the page during this process."
        ],
        "use_vision": True
    },
    {
        "title": f"Select Get Quote For Vehicle Type with {record.Vehicle_Class} or {record.Vehicle_Sub_Class}",
        "subtasks": [
            "Without scrolling, locate the 'Get Quotes For' section at the top of the page. work only in middle portion",
            f"Select the option that matches the vehicle class or subclass: {record.Vehicle_Class} or {record.Vehicle_Sub_Class}.",
            "Confirm the correct option is selected before proceeding."
        ],
        "use_vision": True
    },
    {
        "title": "Select Business Type from Dropdown",
        "subtasks": [
            "Without scrolling, locate the 'Business Type' dropdown.",
            f"Select the business type: {record.Business_Type}.",
            "Verify that the correct business type is selected. If not, select the correct option."
        ],
        "use_vision": True
    },
    {
        "title": "Select Product Type from Dropdown",
        "subtasks": [
            "Without scrolling, locate the 'Product Type' dropdown, just below 'Business Type'.",
            "Select 'Package' as the product type.",
            "Verify that 'Package' is selected. If not, select it again."
        ],
        "use_vision": True
    },
   {
    "title": "Update 'Policy Start Date' (clear old values first)",
    "subtasks": [
        "Scroll, if necessary, until the section labelled 'Policy Start Date *' is fully visible.",
        "For each of DD, MM, YYYY fields:",
        "  1. Click inside the field.",
        "  2. Send Ctrl+A, then Backspace to clear.",
        f"  3. Type the correct value: DD='{policy_start_date_object['date']}', MM='{policy_start_date_object['month']}', YYYY='{policy_start_date_object['year']}'.",
        "  4. Press Tab to trigger the blur/on-change event.",
        "  5. Wait 0.5s.",
        "  6. Visually verify the value in the field matches what was typed.",
        "If any field does not show the correct value, repeat the steps for that field.",
        "After all fields are set, click outside the date area and verify the full date is displayed as '{policy_start_date_object['date']} / {policy_start_date_object['month']} / {policy_start_date_object['year']}'."
    ],
    "use_vision": True
},


    {
        "title": "Enter Registration Number to Find Your Vehicle",
        "subtasks": [
            "Locate the input field labeled 'Enter Registration Number to find your Vehicle'.",
            f"Enter the registration number exactly as: {record.Registration_Number}.",
            "Check for correct formatting and ensure there are no typos."
        ],
        "use_vision": True
    }
    ,
    
    {
        "title": "Initiate Vehicle Lookup",
        "subtasks": [
            "Locate the 'Search' button near the registration number input field.",
            "Click the 'Search' button exactly once.",
            "Wait until the vehicle details are automatically populated.",
            "Do not click any other buttons during this step."
        ],
        "use_vision": True
    },
       {
    "title": "Update 'Policy Expiry Date' (clear old values first)",
    "subtasks": [
        "Scroll, if necessary, until the section labelled 'Policy Expiry Date *' is fully visible.",
        "For each of DD, MM, YYYY fields:",
        "  1. Click inside the field.",
        "  2. Send Ctrl+A, then Backspace to clear.",
        f"  3. Type the correct value: DD='{expiry_date_object['date']}', MM='{expiry_date_object['month']}', YYYY='{expiry_date_object['year']}'.",
        "  4. Press Tab to trigger the blur/on-change event.",
        "  5. Wait 0.5s.",
        "  6. Visually verify the value in the field matches what was typed.",
        "If any field does not show the correct value, repeat the steps for that field.",
        "After all fields are set, click outside the date area and verify the full date is displayed as '{expiry_date_object['date']} / {expiry_date_object['month']} / {expiry_date_object['year']}'."
    ],
    "use_vision": True
},
   
   
    # {
    #     "title": "Set Previous Claim Status",
    #     "subtasks": [
    #         f"Set 'Claim in Previous Policy' dropdown exactly as: {record.Claim_Status}.",
    #         "Confirm selection."
    #     ],
    #     "use_vision": True
    # },
    {
        "title": "Fill Insured Declared Value (IDV)",
        "subtasks": [
            "Scroll to 'Insured Declared Value' section.",
            f"Enter 'Changed IDV' exactly: {0.8 * record.IDV_Value}.",
            "Ensure mandatory fields are completed.",
            "Verify entries in compound fields thoroughly."
        ],
        "use_vision": True
    },
    {
        "title": "Submit Form and Retrieve Plans",
        "subtasks": [
            "Scroll to bottom of form where 'Get Plans' button is located.",
            "Click 'Get Plans' button exactly once.",
            "Wait for insurance plans to fully load. When Save Quote button is visible on screen finsih the task",
            "If any error occurs, immediately seek human intervention."
        ],
        "use_vision": True
    }
]

ask_question = [
    {
        "title": "Ask user about his/her whereabouts after visiting youtube.com",
        "subtasks": [
            "Visit youtube.com and then"
            "Ask user how is he/she."
        ]
    }
]

tasks = ask_question
