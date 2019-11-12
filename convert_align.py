"""
Given a GENTLE alignment for an entire video, creates a new alignment file in the format
that LipNet expects
"""

import json
import sys
in_fname = sys.argv[1]
out_fname = sys.argv[2]
print('----')
print(in_fname)
print('----')

with open(in_fname) as g_json:
    g_align = json.load(g_json)
    
l_align = {}

current_time = 0
end_time = g_align['words'][-1]
phone_info = []

for word in g_align['words']:
    start_word = word['start']
    # Add silence between end of last word and start of next work
    silence = {
        'duration': "%.2f" % (start_word - current_time),
        'offset': "%.2f" % current_time,
        'phone': 'SIL',
    }

    phone_info.append(silence)

    current_time = start_word

    for phone in word['phones']:
        phoneme = {
            'duration': "%.2f" % phone['duration'],
            'offset': "%.2f" % current_time,
            'phone': phone['phone']
        }
        phone_info.append(phoneme)
        current_time += phone['duration']


l_align[in_fname] = phone_info

with open(out_fname, 'w') as out_json:
    json.dump(l_align, out_json)
