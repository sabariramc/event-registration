#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 31-May-2020
"""

sql_get_registration_list = """
SELECT registration_date, reg_uuid, full_name, no_of_ticket, enum_name AS registration_type
FROM d_event_registration der
JOIN (
SELECT enum_value, enum_name, enum_code
FROM c_enum
WHERE enum_type_code = 'REGISTRATION_TYPE'
) ce ON registration_type = enum_value
{}  """
