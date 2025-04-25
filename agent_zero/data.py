from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class InsuranceQuoteRequest:
    Id: int
    PB_ticket_id: int
    Registration_Number: str
    Vehicle_Class: str
    Vehicle_Sub_Class: str
    Address: str
    Registration_Date: str
    RTO_Code: str
    Chassis_Number: str
    Engine_Number: str
    Owner_Name: str
    Make: str
    Model: str
    Variant: str
    Cubic_Capacity: int
    Seating_Capacity: int
    GVW: int
    Business_Type: str
    Fuel_Type: str
    Claim_Status: bool
    Last_Year_NCB: int
    Additional_Discount_NA: Optional[str]
    Previous_Insurer_Name: str
    Previous_Policy_Number: str
    PYP_Policy_Type: str
    Policy_Expiry_Date: str
    Third_Party_End_Date: str
    Own_Damage_End_Date: str
    Add_On_Cover_Availed_In_The_Previous_Policy: Optional[str]
    Customer_Type: str
    RTO_City_Location: str
    Manufacturing_Year: str
    Body_Type: str
    Third_Party_Policy_No: str
    Third_Party_Policy_Start_Date: str
    No_of_Wheels: int
    Mobile_Number: str
    Email: str
    Insurer: str
    Policy_Type: str
    RC_Permit_Type: Optional[str]
    RC_Body_Type: Optional[str]
    Automobile_Association_Membership: Optional[bool]
    IDV_Value: int
    Geographical_Extension: int
    CNG_Value: Optional[int]
    LPG_Value: Optional[int]
    Non_elect_ace_Amount: Optional[int]
    Elect_ace_Amount: Optional[int]
    Compulsory_PA_to_owner_driver: Optional[bool]
    CPA_Term: Optional[str]
    Nominee_Name: Optional[str]
    Nominee_Age: Optional[int]
    Nominee_Relationship: Optional[str]
    PA_to_Paid_Driver: Optional[bool]
    No_of_Paid_Drivers: Optional[int]
    PA_Sum_Insured: Optional[bool]
    PA_to_Unnamed_Passenger: Optional[bool]
    Sum_Insured_for_Unnamed_Passengers: Optional[bool]
    Legal_Liability_to_Paid_Drivers: Optional[bool]
    No_of_Drivers_Employees: Optional[int]
    Limited_Liability_to_Employees: Optional[bool]
    No_Addon_Required: Optional[bool]
    Zero_Dep: Optional[bool]
    Consumables: Optional[bool]
    Engine_Protector: Optional[bool]
    Tyre: Optional[bool]
    RTI: Optional[bool]
    Key_Replacement: Optional[bool]
    RSA: Optional[bool]
    Gear: Optional[bool]
    NCB_Protector: Optional[bool]
    RIM_Damage_Cover: Optional[bool]
    Daily_Allowance: Optional[bool]
    Invoice_Price: Optional[bool]
    Loss_of_Personal_Belongings: Optional[bool]
    Tyre_Protector: Optional[bool]
    Electrical_Accessories: Optional[bool]
    Non_Electrical_Accessories: Optional[bool]
    External_Bi_Fuel_Kit: Optional[bool]
    IMT_13: Optional[bool]
    IMT_34: Optional[bool]
    IMT_47: Optional[bool]
    IMT_23: Optional[bool]
    TPPD: Optional[bool]
    Trailer_IDV: Optional[int]
    Trailer_Reg_No: Optional[str]
    Status: str
    Remarks: Optional[str]
    Screenshot_Byte: Optional[str]
    Error_Byte: Optional[str]
    CreatedOn: datetime
    UpdatedOn: datetime
    Trailer: Optional[str]
    Non_Electical_Accessories_Desc: Optional[str]
    Electical_Accessories_Desc: Optional[str]
    No_of_Unnamed_Passenger: Optional[int]
    Trailer_MfgYear: Optional[str]
    Trailer_ChassisNo: Optional[str]
    Ownership: Optional[str]
    Trailer_Make_Model: Optional[str]
    RTO_city: Optional[str]
    Pincode: Optional[int]
    PDF_byte: Optional[str]
    InsurerId: Optional[int]

from datetime import datetime

record = InsuranceQuoteRequest(
    Id=21511,
    PB_ticket_id=74100,
    Registration_Number="HR26DC8954",
    Vehicle_Class="Private car",
    Vehicle_Sub_Class="Motor Car(LMV)",
    Address="C/1601 UNIQUE AURUM CHS LTD CHANDAN SHANTI ROAD SHIKHA MART POONAM GARDEN MIRA BHAYANDER Thane Maharashtra 401107",
    Registration_Date="2017-08-19",
    RTO_Code="MH01",
    Chassis_Number="MAKGM653CHN300145",
    Engine_Number="L15Z14400638",
    Owner_Name="PRAKASH LAVJIBHAI PARMAR ",
    Make="HONDA",
    Model="AMAZE",
    Variant="1.2 VX I-VTEC BS-VI",
    Cubic_Capacity=1497,
    Seating_Capacity=5,
    GVW=1433,
    Business_Type="RollOver",
    Fuel_Type="PETROL",
    Claim_Status=False,
    Last_Year_NCB=0,
    Additional_Discount_NA=None,
    Previous_Insurer_Name="Reliance General Insurance",
    Previous_Policy_Number="34423454536456",
    PYP_Policy_Type="34423454536456",
    Policy_Expiry_Date="2025-04-10",
    Third_Party_End_Date="2025-04-10",
    Own_Damage_End_Date="2025-04-10",
    Add_On_Cover_Availed_In_The_Previous_Policy=None,
    Customer_Type="Corporate",
    RTO_City_Location="MUMBAI,Maharashtra",
    Manufacturing_Year="03/2017",
    Body_Type="SALOON",
    Third_Party_Policy_No="34423454536456",
    Third_Party_Policy_Start_Date="2024-04-10",
    No_of_Wheels=4,
    Mobile_Number="9999999999",
    Email="abc@gmail.com",
    Insurer="Future Generali",
    Policy_Type="Comprehensive",
    RC_Permit_Type=None,
    RC_Body_Type=None,
    Automobile_Association_Membership=None,
    IDV_Value=380000,
    Geographical_Extension=0,
    CNG_Value=None,
    LPG_Value=None,
    Non_elect_ace_Amount=None,
    Elect_ace_Amount=None,
    Compulsory_PA_to_owner_driver=True,
    CPA_Term=None,
    Nominee_Name="Legal heir",
    Nominee_Age=21,
    Nominee_Relationship="Spouse",
    PA_to_Paid_Driver=True,
    No_of_Paid_Drivers=None,
    PA_Sum_Insured=False,
    PA_to_Unnamed_Passenger=None,
    Sum_Insured_for_Unnamed_Passengers=False,
    Legal_Liability_to_Paid_Drivers=False,
    No_of_Drivers_Employees=None,
    Limited_Liability_to_Employees=False,
    No_Addon_Required=False,
    Zero_Dep=False,
    Consumables=False,
    Engine_Protector=False,
    Tyre=False,
    RTI=False,
    Key_Replacement=False,
    RSA=False,
    Gear=False,
    NCB_Protector=False,
    RIM_Damage_Cover=False,
    Daily_Allowance=False,
    Invoice_Price=False,
    Loss_of_Personal_Belongings=False,
    Tyre_Protector=False,
    Electrical_Accessories=False,
    Non_Electrical_Accessories=False,
    External_Bi_Fuel_Kit=False,
    IMT_13=False,
    IMT_34=False,
    IMT_47=False,
    IMT_23=False,
    TPPD=False,
    Trailer_IDV=0,
    Trailer_Reg_No=None,
    Status="Failed",
    Remarks=None,
    Screenshot_Byte="",
    Error_Byte="68022626ae40ba6c800ecec8",
    CreatedOn=datetime.strptime("2025-04-11 10:59:47", "%Y-%m-%d %H:%M:%S"),
    UpdatedOn=datetime.strptime("2025-04-11 11:00:13", "%Y-%m-%d %H:%M:%S"),
    Trailer=None,
    Non_Electical_Accessories_Desc=None,
    Electical_Accessories_Desc=None,
    No_of_Unnamed_Passenger=0,
    Trailer_MfgYear=None,
    Trailer_ChassisNo=None,
    Ownership=None,
    Trailer_Make_Model=None,
    RTO_city=None,
    Pincode=201010,
    PDF_byte="",
    InsurerId=11
)