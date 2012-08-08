import sys

inj_sev_map = { 'No Injury (O)': 0,  'Possible Injury (C)': 1,
                'Nonincapacitating Evident Injury (B)': 2, 'Incapacitating Injury (A)': 3,
                'Fatal Injury (K)': 4 }

def proc_inj_sev(s):
    return inj_sev_map.get(s, -1)


seat_pos_map = { 'Front Seat. Left side': 1, 'Front Seat. Right side': 2,
                 'Second Seat. Right side': 3, 'Second Seat. Left side': 4,
                 'Non-motorist': 0 };

def proc_seat_pos(s):
    # print repr(s), seat_pos_map.get(s, -1)
    return seat_pos_map.get(s, -1)
