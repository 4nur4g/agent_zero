from datetime import date, timedelta

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
        "subtasks": [
            # 1) Absolute first rule: never scroll
            "🚫 DO NOT SCROLL THE PAGE—under no circumstances use page.scrollDown or page.keyboard.press('PageDown').",

            # 2) Work only within the visible viewport
            "Perform all actions within the current viewport; all selectable options are already visible.",

            # 3) Handle interruptions
            "If any pop-ups, modals, or alerts appear, close them immediately.",

            # 4) The actual selection task
            (
                "Choose exactly one option from the “Get Quotes For” section "
                "(the items immediately below that heading) based solely on "
                f"{record.Vehicle_Class} or {record.Vehicle_Sub_Class}."
            ),
        ],
        "use_vision": True,
    },
    {
        # "title": "Begin form submission by entering business details",
        "subtasks": [
            "Wait for any loading spinners to disappear before interacting with the form.",
            "Scroll to locate the business details section of the form.",
            f"Set 'Business Type' to the value of {record.Business_Type}.",
            "Set 'Product Type' explicitly to 'Package'.",
            f"Set 'Policy Start Date' to the value of: "
            f"- Date: {policy_start_date_object["date"]}"
            f"- Month: {policy_start_date_object["month"]}"
            f"- Year: {policy_start_date_object["year"]}",
            f"Mark the task done only when you've filled all the mentioned details.",
        ],
        "use_vision": True
    },
    {
        "title": "Identify the vehicle by entering registration and retrieving vehicle info",
        "subtasks": [
            "Scroll down and find the 'Registration Number' input field",
            f"Enter the registration number from {record.Registration_Number}.",
            "Verify the number for correct format and typos.",
            "Click the 'Search' button to initiate vehicle lookup.",
            "Stay away from clicking on any other buttons in this section."
            "Wait for the search results to be fully populated before continuing.",
            f"Mark the task done only when you've filled the registration no and clicked on search button.",
        ]
    },
    {
        "title": "Enter previous policy details and claim history for risk assessment",
        "subtasks": [
            "Scroll down to the section containing policy history fields.",
            f"Fill in the 'Policy Expiry Date' with "
            f"- Date: {expiry_date_object["date"]}"
            f"- Month: {expiry_date_object["month"]}"
            f"- Year: {expiry_date_object["year"]}",
            f"Set the 'Claim in Previous Policy' value to {record.Claim_Status}."
        ]
    },
    {
        "title": "Calculate and fill updated Insured Declared Value (IDV)",
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
tasks = atomic_tasks
