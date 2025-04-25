from datetime import date, timedelta

from agent_zero.data import record

tomorrow = date.today() + timedelta(days=1)

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
        "extend_system_message": "After filling credentials and clicking on login button, your task is done."
    },
    {
        "title": "Select vehicle type",
        "subtasks": [
            "Check for any pop-up notifications, modals, or alerts and close them.",
            f"Based on the parameter availability, choose either {record.Vehicle_Class} or {record.Vehicle_Sub_Class}."
        ],
        "use_vision": True
    },
    {
        "title": "Begin form submission by entering business details",
        "subtasks": [
            "Wait for any loading spinners to disappear before interacting with the form.",
            "Scroll to locate the business details section of the form.",
            f"Set 'Business Type' to the value of {record.Business_Type}.",
            "Set 'Product Type' explicitly to 'Package'.",
            f"Set 'Policy Start Date' to the value of {tomorrow}.Beware, the input is split into three fields"
            f"First fill the date, then month, then the year.",
        ]
    },
    {
        "title": "Identify the vehicle by entering registration and retrieving vehicle info",
        "subtasks": [
            "Find the 'Registration Number' input field.",
            f"Enter the registration number from {record.Registration_Number}.",
            "Verify the number for correct format and typos.",
            "Click the 'Search' button to initiate vehicle lookup.",
            "Wait for the search results to be fully populated before continuing."
        ]
    },
    {
        "title": "Enter previous policy details and claim history for risk assessment",
        "subtasks": [
            "Scroll down to the section containing policy history fields.",
            f"Fill in the 'Policy Expiry Date' with {record.Policy_Expiry_Date}. Beware, the input is split into three fields"
            f"First fill the date, then month, then the year.",
            f"Set the 'Claim in Previous Policy' value to {record.Claim_Status}."
        ]
    },
    {
        "title": "Calculate and fill updated Insured Declared Value (IDV)",
        "subtasks": [
            "Scroll to the 'Insured Declared Value' section of the form.",
            f"Compute 90% of the value in {record.IDV_Value}.",
            f"Enter the computed value ({0.9 * record.IDV_Value}) in the 'Changed IDV' field.",
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
tasks = atomic_tasks
