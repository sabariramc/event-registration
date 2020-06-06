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
WHERE enum_type_name = 'REGISTRATION_TYPE'
) ce ON registration_type = enum_value
%s"""

sql_get_registration = """
SELECT registration_date, reg_uuid, full_name, no_of_ticket, enum_name AS registration_type, mobile_number, email_address, no_of_ticket,id_card_path 
FROM d_event_registration der
JOIN (
SELECT enum_value, enum_name, enum_code
FROM c_enum
WHERE enum_type_name = 'REGISTRATION_TYPE'
) ce ON registration_type = enum_value
WHERE reg_uuid = %(reg_uuid)s"""

sql_count_wrapper = """
SELECT COUNT(*) AS cnt
FROM (%s)x"""

sql_check_registration = """
SELECT COUNT(*) AS cnt
FROM d_event_registration
WHERE mobile_number = %(mobile_number)s OR email_address = %(email_address)s"""

sql_create_registration = """
INSERT INTO `d_event_registration` (`reg_uuid`, `full_name`, `mobile_number`, `email_address`, `registration_date`, `registration_type`, `no_of_ticket`, `id_card_path`) 
VALUES (%(reg_uuid)s, %(full_name)s, %(mobile_number)s, %(email_address)s, %(registration_date)s, %(registration_type)s, %(no_of_ticket)s, %(id_card_path)s)"""
