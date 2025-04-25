from datetime import date, timedelta

from browser_use.controller.service import Controller

from agent_zero.data import record
from common_python.utils.date_time import extract_date_parts

tomorrow = date.today() + timedelta(days=1)

expiry_date_object = extract_date_parts(record.Policy_Expiry_Date)
policy_start_date_object = extract_date_parts(tomorrow)

atomic_tasks = [
    {
        # "title": "Log into FG General Partner Portal to access the policy interface",
        # "subtasks": [
        #     f"Enter the username using `fgg_user_name` in the appropriate input field.",
        #     f"Enter the password using `fgg_password` in the password field.",
        #     "Click the login button to authenticate.",
        #     "Wait for the portal dashboard or landing page to fully load before proceeding."
        # ],
        "initial_actions": [
            {"go_to_url": {"url": "https://partners.fggeneral.in/nonlifeadvisor"}},
            {"input_text": {"index": 2, "text": "fgg_user_name"}},
            {"input_text": {"index": 3, "text": "fgg_password"}},
            {"click_element_by_index": {"index": 5}}],
        # "extend_system_message": "After filling credentials and clicking on login button, your task is done."
    },
    {
        "title": "Handle pop-ups, modals, and alerts",
        "subtasks": [
            "If any pop-ups, modals, or alerts appear, close them immediately."
        ],
        "use_vision": True,
    },
    {
        "title": "Select option from ‘Get Quotes For’",
        "subtasks": [
            (
                "The button will be available on top of the viewport."
                "(the items immediately below that heading)"
                "To make decision, use only the following info: "
                f"{record.Vehicle_Class} or {record.Vehicle_Sub_Class}."
            )
        ],
        "controller": Controller(exclude_actions=['scroll_down', 'scroll_up']),
        "use_vision": True,
    },
    {
        "title": "Locate business details section",
        "subtasks": [
            "Scroll to locate the business details section of the form."
        ],
        "use_vision": True,
    },
    {
        "title": "Populate 'Business Type' dropdown",
        "subtasks": [
            f"Set 'Business Type' dropdown to the value of {record.Business_Type}."
            "Mark task done only when you've selected the business type."
        ],
        # "use_vision": True,
    },
    {
        "title": "Enter Product Type",
        "subtasks": [
            "Set 'Product Type' to 'Package'."
            "Mark task done only when you've entered the product type."
        ],
        "use_vision": False,
    },
    {
        "title": "Enter Policy Start Date — Day",
        "subtasks": [
            f"Set the 'Policy Start Date' day fields to {policy_start_date_object['date']}."
            "Mark task done only when you've entered the policy start date - day"

        ],
        "use_vision": True,
    },
    {
        "title": "Enter Policy Start Date — Month",
        "subtasks": [
            f"Set the 'Policy Start Date' month field to {policy_start_date_object['month']}."
            "Mark task done only when you've entered the policy start date - month"
        ],
        "use_vision": True,
    },
    {
        "title": "Enter Policy Start Date — Year",
        "subtasks": [
            f"Set the 'Policy Start Date' year field to {policy_start_date_object['year']}.",
            "Mark task done only when you've entered the policy start date - year"
        ],
        "use_vision": True,
    },
    {
        "title": "Locate Registration Number field",
        "subtasks": [
            "Scroll down to find the 'Registration Number' input field."
        ],
        "use_vision": True,
    },
    {
        "title": "Enter Registration Number",
        "subtasks": [
            f"Enter the registration number: {record.Registration_Number}."
            "Mark task done only when you've entered the registration number."
        ],
        "use_vision": True,
    },
    {
        "title": "Verify Registration Number format",
        "subtasks": [
            "Verify the number for correct format and typos."
        ],
        "use_vision": True,
    },
    {
        "title": "Initiate vehicle lookup",
        "subtasks": [
            "Click the 'Search' button to initiate vehicle lookup.",
            "Avoid clicking any other buttons in this section."
            "Mark this task done only when vehicle details are automatically populated after search"
        ],
        "use_vision": True,
    },
    {
        "title": "Locate policy history section",
        "subtasks": [
            "Scroll down to the section containing policy history fields."
        ],
        "use_vision": True,
    },
    {
        "title": "Enter Policy Expiry Date — Day",
        "subtasks": [
            f"Set the 'Policy Expiry Date' day field to {expiry_date_object['date']}."
            "Mark task done only when you've entered the policy expiry date - day"
        ],
        "use_vision": True,
    },
    {
        "title": "Enter Policy Expiry Date — Month",
        "subtasks": [
            f"Set the 'Policy Expiry Date' month field to {expiry_date_object['month']}."
            "Mark task done only when you've entered the policy expiry date - month"
        ],
        "use_vision": True,
    },
    {
        "title": "Enter Policy Expiry Date — Year",
        "subtasks": [
            f"Set the 'Policy Expiry Date' year field to {expiry_date_object['year']}.",
            "Mark task done only when you've entered the policy expiry date - year"
        ],
        "use_vision": True,
    },
    {
        "title": "Enter previous claim status",
        "subtasks": [
            f"Set the 'Claim in Previous Policy' value to {record.Claim_Status}."
            "Mark task done only when Claim in Previous Policy is set."
        ],
        "use_vision": True,
    },
    {
        "title": "Fill updated Insured Declared Value (IDV)",
        "subtasks": [
            "Scroll to the 'Insured Declared Value' section of the form.",
            f"Enter the value ({0.9 * record.IDV_Value}) in the 'Changed IDV' field.",
            "Ensure that all mandatory fields in this section are completed.",
            "For compound fields (like date or registration number inputs split across multiple boxes), ensure correct and complete input."
        ]
    },
    {
        "title": "Submit the form and retrieve available insurance plans",
        "subtasks": [
            "Scroll to the bottom of the form to locate the 'Get Plans' button.",
            "Click the 'Get Plans' button to submit the form and view options.",
            "If any error or unexpected behavior occurs, seek help from a human operator."
        ]
    }
]

atomic_tasks_2 = [
    {
        "title": "Log into FG General Partner Portal",
        "subtasks": [
            "Go to URL: https://partners.fggeneral.in/nonlifeadvisor.",
            "Enter username: fgg_user_name.",
            "Enter password: fgg_password.",
            "Click the login button",
            "Wait until dashboard or landing page fully loads."
        ],
        "use_vision": False
    },
    {
        "title": "Handle Pop-ups, Modals, and Alerts",
        "subtasks": [
            "Close immediately any visible pop-up, modal, or alert.",
            "Confirm no further pop-ups remain."
        ],
        "use_vision": True
    },
    {
        "title": "Select Correct Option in 'Get Quotes For' Section",
        "subtasks": [
            "Identify 'Get Quotes For' section at top viewport area.",
            "Using Vehicle_Class or Vehicle_Sub_Class, select matching option. based on data: ",
            f"{record.Vehicle_Class} or {record.Vehicle_Sub_Class}."
            "Do NOT scroll during this action."
        ],
        "use_vision": True
    },
    {
        "title": "Populate Business Details",
        "subtasks": [
            "Scroll until 'Business Details' section is clearly visible.",
            f"Select from 'Business Type' dropdown: {record.Business_Type}.",
            "Confirm correct selection."
        ],
        "use_vision": True
    },
    {
        "title": "Set Product Type",
        "subtasks": [
            "Enter 'Product Type' exactly as: Package.",
            "Confirm entry."
        ],
        "use_vision": False
    },
    {
        "title": "Enter Policy Start Date",
        "subtasks": [
            "Scroll to 'Policy Start Date' section.",
            f"Set Day: {policy_start_date_object['date']}.",
            f"Set Month: {policy_start_date_object['month']}.",
            f"Set Year: {policy_start_date_object['year']}.",
            "Confirm all entries."
        ],
        "use_vision": True
    },
    {
        "title": "Enter Registration Number",
        "subtasks": [
            "Scroll to find 'Registration Number' field.",
            f"Enter exactly: {record.Registration_Number}.",
            "Verify correct formatting and typos."
        ],
        "use_vision": True
    },
    {
        "title": "Initiate Vehicle Lookup",
        "subtasks": [
            "Click 'Search' button exactly once.",
            "Wait for vehicle details auto-population.",
            "Avoid clicking other buttons."
        ],
        "use_vision": True
    },
    {
        "title": "Enter Policy Expiry Date",
        "subtasks": [
            "Scroll to 'Policy History' section.",
            f"Set Day: {expiry_date_object['date']}.",
            f"Set Month: {expiry_date_object['month']}.",
            f"Set Year: {expiry_date_object['year']}.",
            "Confirm all entries."
        ],
        "use_vision": True
    },
    {
        "title": "Set Previous Claim Status",
        "subtasks": [
            f"Set 'Claim in Previous Policy' dropdown exactly as: {record.Claim_Status}.",
            "Confirm selection."
        ],
        "use_vision": True
    },
    {
        "title": "Fill Insured Declared Value (IDV)",
        "subtasks": [
            "Scroll to 'Insured Declared Value' section.",
            f"Enter 'Changed IDV' exactly: {0.9 * record.IDV_Value}.",
            "Ensure mandatory fields are completed.",
            "Verify entries in compound fields thoroughly."
        ],
        "use_vision": True
    },
    {
        "title": "Submit Form and Retrieve Plans",
        "subtasks": [
            "Scroll to bottom of form.",
            "Click 'Get Plans' button exactly once.",
            "Wait for insurance plans to fully load.",
            "If any error occurs, immediately seek human intervention."
        ],
        "use_vision": True
    }
]

tasks = atomic_tasks_2
