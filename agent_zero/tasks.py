from datetime import date, timedelta

from browser_use.controller.service import Controller

from agent_zero.data import record
from common_python.utils.date_time import extract_date_parts

tomorrow = date.today() + timedelta(days=1)

expiry_date_object = extract_date_parts(record.Policy_Expiry_Date)
policy_start_date_object = extract_date_parts(record.Policy_Start_Date)

atomic_tasks_2 = [
    {
        "title": "Login to FG General Portal, follow the tasks in order,all the subtasks must be completed in sequence only, mark task done only when all subtasks are completed, remember subtasks completed already and never repeat subtasks",
        "subtasks": [
            "Immediately go to: https://partners.fggeneral.in/nonlifeadvisor",
            "Without delay, locate the username input field labeled 'User ID'"
            "Enter User ID: fgg_user_name.",
            "Enter password: fgg_password.",
            "Immediately click the login button labeled 'Login'",
            "Avoid scrolling or pausing during this sequence"
            "Wait until dashboard or landing page fully loads. "
        ],
        "use_vision": True
    },
    {
        "title": "Close Pop-ups, Modals, and Alerts",
        "subtasks": [
            "Close immediately any visible pop-up, modal, or alert.",
            "Confirm no further pop-ups remain."
            "Do NOT scroll during this action."
        ],
        "use_vision": True
    },
    {
        "title": "Select Vehicle Type",
        "subtasks": [
            "Do NOT scroll during this action."
            "Using Vehicle_Class or Vehicle_Sub_Class, select matching option. based on data: ",
            f"{record.Vehicle_Class}"
        ],
        "use_vision": False
    },
    
    {
        "title": "Select Business Type from Dropdown",
        "subtasks": [
            "Do NOT scroll during this action."
            "Locate 'Business Type' dropdown, located just below Business Type.",
            f"Select from 'Business Type' dropdown: {record.Business_Type}.",
            "Confirm correct selection, if not correct, select the correct option."
        ],
        "use_vision": False
    },
    {
        "title": "Select Product Type from Dropdown",
        "subtasks": [
            "Do NOT scroll during this action."
            "Locate Product Type' dropdown, located just below Business Type.",
            "Select 'Product Type' exactly as: Package.",
            "Confirm correct selection, if not correct, select the correct option"
        ],
        "use_vision": False
    },
        {
        "title": "Enter Registration Number to find your Vehicle",
        "subtasks": [
            "Locate 'Enter Registration Number to find your Vehicle",
            f"Enter exactly: {record.Registration_Number}.",
            "Verify correct formatting and typos."
        ],
        "use_vision": True
    },
      {
        "title": "Initiate Vehicle Lookup",
        "subtasks": [
            "Locate 'Search' button. near Enter Registration Number to find your Vehicle"
            "Click 'Search' button exactly once.",
            "Wait for vehicle details auto-population.",
            "Avoid clicking other buttons."
        ],
        "use_vision": True
    },
       {
    "title": "Locate and clear index 14, 15, 16 fields",

    "use_vision": False
},
    {
    "title": "Locate and Enter 'Policy Start Date'",
    "subtasks": [
        "Once 'Policy Start Date' section is visible, focus on the DD field first.",
        f"Clear any existing value in DD, then enter {policy_start_date_object['date']} carefully.",
        "After entering DD, tab out or click outside to trigger field update.",
        f"Focus on MM field, clear any existing value, and enter {policy_start_date_object['month']}.",
        "After entering MM, tab out or click outside to trigger field update.",
        "Verify that the YYYY field is set to {policy_start_date_object['year']}.",
        "If YYYY is not correct, clear it manually and type the correct year.",
        "After all entries, double-check visually that DD, MM, and YYYY are correctly updated."
    ],
    "use_vision": True
},
    # {
    #     "title": "Locate and Enter 'Policy Expiry Date' in 'Previous Insurance' section",
    #     "subtasks": [
    #         "Scroll Down to locate 'Policy Expiry Date' section.",
    #         f"Set Day: {expiry_date_object['date']}.",
    #         f"Set Month: {expiry_date_object['month']}.",
    #         f"Set Year: {expiry_date_object['year']}.",
    #         "Confirm all entries."
    #     ],
    #     "use_vision": True
    # },

  
    # {
    #     "title": "Enter Policy Expiry Date",
    #     "subtasks": [
    #         "Scroll to 'Policy History' section.",
    #         f"Set Day: {expiry_date_object['date']}.",
    #         f"Set Month: {expiry_date_object['month']}.",
    #         f"Set Year: {expiry_date_object['year']}.",
    #         "Confirm all entries."
    #     ],
    #     "use_vision": False
    # },
    # {
    #     "title": "Set Previous Claim Status",
    #     "subtasks": [
    #         f"Set 'Claim in Previous Policy' dropdown exactly as: {record.Claim_Status}.",
    #         "Confirm selection."
    #     ],
    #     "use_vision": False
    # },
    # {
    #     "title": "Fill Insured Declared Value (IDV)",
    #     "subtasks": [
    #         "Scroll to 'Insured Declared Value' section.",
    #         f"Enter 'Changed IDV' exactly: {0.9 * record.IDV_Value}.",
    #         "Ensure mandatory fields are completed.",
    #         "Verify entries in compound fields thoroughly."
    #     ],
    #     "use_vision": False
    # },
    # {
    #     "title": "Submit Form and Retrieve Plans",
    #     "subtasks": [
    #         "Scroll to bottom of form.",
    #         "Click 'Get Plans' button exactly once.",
    #         "Wait for insurance plans to fully load.",
    #         "If any error occurs, immediately seek human intervention."
    #     ],
    #     "use_vision": False
    # }
]

tasks = atomic_tasks_2
