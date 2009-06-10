#!/usr/bin/python

# Thermodyne2XML - Converts Thermodynamic Database for Combustion and
# Air-Pollution Use, by Alexander Burcat - and Branko Ruscic - to an XML file
# Copyright (C) 2004, Eitan Burcat, burcat@bigfoot.com
# Copyright (C) 2005, Reinhardt Pinzon, reinhardtpinzon@yahoo.com, ANL
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA	 02111-1307, USA.

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxx - Vanilla Python Code - xxxxxxxxxxxxxxx
# Thermodyne2XML/code vanilla added -Converts Thermodynamic Database
# for Combustion and Air-Pollution, by Alexander Burcat - and Branko Ruscic- to an XML file
# Copyright (C) 2004, Eitan Burcat, burcat@bigfoot.com
# Copyright (C) 2005, Reinhardt Pinzon, reinhardtpinzon@yahoo.com, ANL
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
import re
from re import *
import sys
from sys import *
import difflib
from difflib import *
import textwrap
from textwrap import *
import string
from string import *
#####################################################################
#  List of Main Patterns - Alex Burcat Data File
#####################################################################
ref_0=r'(?:[a-zA-Z0-9\n?\s\.\(\)\;\"\"\-\&\+\,\/\[\]]*)'
pattern_sigma='(?P<sigma>(?<=SIGMA=)\d+|(?<=SIGMA=)\s*\d+|(?<=SIGMA)(?:\([A-Z]*\)=)*\d+|(?<=SIGMA =)\s+\d+|(?<=SIGMA =)\s+\d+|(?<=SIGMA)(?:\([A-Z]*\)\s+=)*\s+\d+)'
pattern_statwt='(?P<statwt>(?<=STATWT=)\d+|(?<=STATWT=)\s*\d+|(?<=STATWT =)\s*\d+|(?<=STATWT =)\d+)'
pattern_t0_statwt='(?P<t0_statwt>(?<=T0\(STATWT\)\=)(?:[0-9\(\,\)\s]*)|(?<=T0\(STATWT\)\=)(?:\d+\(\d+\))|(?<=T0\=)(?:\d+\s+|\d+\.\s+|\d+\.\d+\s+)(?:STATWT\=)\d+|(?<=T0\=)(?:\d+\s+|\d+\.\s+|\d+\.\d+\s+|\d+\(\d+\)\,\d+\(\d+\)|(?:\d+|\d+.\d+)\(\d+\)))'
pattern_be='(?P<be>(?<=BE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?<=BE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?<=BE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?<=BE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?<=BE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?<=BE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?(?:\s+CM\-\d+|CM\-\d+|))'
pattern_we='(?P<we>(?<=WE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){3,7}?|(?<=WE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){3,7}?|(?<=WE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){3,7}|(?<=WE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?|(?<=WE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?|(?<=WE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7})'
pattern_wexe='(?P<wexe>(?<=WEXE=)(?:[\[\d+\.\]]*)|(?<=WEXE =)(?:[\[\d+\.\]]*)|(?<=WEXE = )(?:[\[\d+\.\]]*))'
pattern_alfae='(?P<alfae>(?<=ALFAE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?<=ALFAE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?<=ALFAE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?<=ALPHAE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?<=ALPHAE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?<=ALPHAE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?<=ALFAE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?<=ALFAE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?<=ALFAE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?<=ALPHAE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?<=ALPHAE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?<=ALPHAE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7})'
pattern_IA='(?P<ia>(?<=IA\=)\d+.\d+|(?<=IA\=)\s*\d+.\d+|(?<=IA =)\s*\d+.\d+|(?<=IA\=).\d+|(?<=IA \=).\d+|(?<=IA\=)\s+.\d+|(?<=IA \=)\s*.\d+)'
pattern_IB='(?P<ib>(?<=IB\=)\d+.\d+|(?<=IB\=)\s*\d+.\d+|(?<=IB =)\s*\d+.\d+|(?<=IB\=).\d+|(?<=IB \=).\d+|(?<=IB\=)\s+.\d+|(?<=IB \=)\s*.\d+)'
pattern_IC='(?P<ic>(?<=IC\=)\d+.\d+|(?<=IC\=)\s*\d+.\d+|(?<=IC =)\s*\d+.\d+|(?<=IC\=).\d+|(?<=IC \=).\d+|(?<=IC\=)\s+.\d+|(?<=IC \=)\s*.\d+)'
pattern_IAIBIC='(?P<iaibic>(?<=IAIBIC\=)(?:\d+.\d+E(?:\+|-|\s|)(?:\d{3}|\d+.))|(?<=IAIBIC\=)(?:\d+.E(?:\+|-|\s|)\d{3})|(?<=IAIBIC\=)(?:\d+E(?:\+|-|\s|)\d{3})|(?<=IAIBIC\=)(?:\d+.\d+\s+E(?:\+|-|\s|)\d{3})|(?<=IAIBIC\=)(?:\d+.\s+E(?:\+|-|\s|)(?:\d{3}|\d+.\d+))|(?<=IAIBIC\=)(?:\d+\s+E(?:\+|-|\s|)\d{3})|(?<=IAIBIC\=)(?:[0-9\.]*))'
pattern_IA_IB='(?P<ia_ib>(?<=IA=IB=)(?:\d+.\d+)|(?<=IA=IB=)(?:.\d+))'
pattern_IA_IB_IC='(?P<ia_ib_ic>(?<=IA=IB=IC=)(?:\d+.\d+))'
pattern_A_B='(?P<a_b>(?<=A=B=)(?:\d+.\d+))'
pattern_C='(?P<c>(?<=C\=)(?:\d+.\d+))'
pattern_A0='(?P<a0>(?<=A0=)(?:\d+.\d+|.\d+))'
pattern_B0='(?P<b0>(?<=B0=)\d+.\d+(?:\s+|)CM\-\d+|(?<=B0=)\s+\d+.\d+\s*CM\-\d+|(?<=B0=)\d+.\d+CM\-\d+|(?<=B0=)\d+.\d+\s+|(?<=B0=)\d+.\d+|(?<=B0=).\d+|(?<=B0=)\d+)'
pattern_C0='(?P<c0>(?<=C0=)(?:\d+.\d+|.\d+))'
pattern_A0_B0='(?P<a0_b0>(?<=A0=B0=)(?:\d+.\d+|.\d+))'
pattern_Ir='(?P<ir>(?<=IR=)(?:\+|\-|\~|)\d+.\d+|(?<=IR=).\d+|(?<=IR)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|\~|)\d+.\d+|(?<=IR = )(?:\+|\-|\~|)\d+.\d+|(?<=IR = )(?:\+|\-|\~|).\d+|(?<=IR)(?:\([A-Z0-9\-\*]*\)\s+=)*(?:\+|\-|\~|)\s+\d+.\d+)'
pattern_rosym='(?P<rosym>(?<=ROSYM=)\d+|(?<=ROSYM=)\s*\d+|(?<=ROSYM)(?:\([A-Z0-9\-]*\)=)*\d+|(?<=ROSYM =)\s+\d+|(?<=ROSYM =)\s+\d+|(?<=ROSYM)(?:\([A-Z0-9\-]*\)\s+=)*\s+\d+|(?<=ROSYM=)\d+.)'
pattern_v1=r'(?P<v1>\bV(?:[A-Z0-9\-\(\)\s]*)(?:1|2|\(1\)|\(2\)|3|\(3\)|\))(?:\=|\s|)(?:[A-Z0-9\.\-\(\)]*)(?:[+CM|CM|\s+CM\s+|CM\s+|KCAL|\s+KCAL|\s+KCAL\s+|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|\KJ|\s+KJ|\s|1\/CM\s\/\-\.0-9]*)(?=(?:\s| )))'
pattern_v2=r'(?P<v2>\bV(?:[A-Z0-9\-\(\)\s]*)(?:1|2|\(1\)|\(2\)|3|\(3\)|\))(?:\=|\s|)(?:[A-Z0-9\.\-\(\)]*)(?:[+CM|CM|\s+CM\s+|CM\s+|KCAL|\s+KCAL|\s+KCAL\s+|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|\KJ|\s+KJ|\s|1\/CM\s\/\-\.0-9]*)(?=(?:\s| )))'
pattern_v3=r'(?P<v3>\bV(?:[A-Z0-9\-\(\)\s]*)(?:1|2|\(1\)|\(2\)|3|\(3\)|\))(?:\=|\s|)(?:[A-Z0-9\.\-\(\)]*)(?:[+CM|CM|\s+CM\s+|CM\s+|KCAL|\s+KCAL|\s+KCAL\s+|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|\KJ|\s+KJ|\s|1\/CM\s\/\-\.0-9]*)(?=(?:\s| )))'
pattern_nu='(?P<nu>(?<=NU=)(?:[\d+\(\d+\)\,\s+\.\d+\(\d+\)]*)|(?<=NU =)(?:[\d+\(\d+\)\,\s+\.\d+\(\d+\)]*))'
pattern_x='(?P<x>(?:X\d+=)(?:\+|\-|\s+|\~|)(?:[0-9\.]*))'
pattern_y='(?P<y>(?:Y\d+=)(?:\+|\-|\s+|\~|)(?:[0-9\.]*))'
pattern_Max_Lst_Error='(?P<max_error>(?<=MAX\sLST\sSQ\sERROR\s)(?:[0-9\,\;\*\s+\-CP AND\&\.\@ K\%\=\(\) H-HREF WARNING]*)(?<![A-Z0-9\.\s\+\=]))'
#pattern_Max_Lst_Error='(?P<max_error>(?<=MAX\sLST\sSQ\sERROR\s)(?:[0-9\,\*\s\-CP AND\&\.\@ K \%\=\(\) H-HREF WARNING]*)(?:\s|)|(?<=MAX\sLST\sSQ\sERROR\s)(?:[0-9\,\*\s\-CP AND\&\.\@ K \%\=\(\) H-HREF WARNING]*)(?<![A-Z0-9\.\s\+\=]))'
pattern_REF='(?P<ref>(?<=REF=)(?:[A-Z0-9\s\.\(\)\'\"\-\&\+\,\/\[\]\;]*)(?=\s|)|(?<=REF = )(?:[A-Z0-9\s\.\(\)\'\"\-\&\+\,\/\[\]\;]*)(?=\s|))'
pattern_add_info='(?P<add_info>(?<={)(?:[A-Z0-9\s\#\.\(\)"\-\&\+\,\;\/\[\]\=]*)(?=\}))'
#pattern_add_info='(?P<add_info>(?<={)(?:.?.?.?|HF298=.?.?.?.?.?.?.?.?.?.?|HF0=.?.?.?.?.?.?.?.?.?.?|REF=)??(?:[a-zA-Z0-9?\s\.\(\)"\-\&\+\,\/\[\]\=]).*(?=\}))'
pattern_HF298=r'(?P<h298>(?<=HF298=)(?:\+|\-|)(?:\d+.\d+|\d+.)(?:\s+|)(?:\+|\s+|)(?:\/|\s+|)(?:\s+|)(?:\-|\s+|)(?:\s+|)(?:\d+.\d+\s+|\d+.|\d+|\s+|)(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ|\s+KCAL|\s+CAL|\s+KCAL\/MOLE|\s+KJ\/MOLE| )|(?<=HF298=)\d+.\d+\+\/\-\d+.\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\s+|)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\+\/\-\d+.\d+|(?<=HF298=)\d+\+\/\-\d+(?:\s+KJ|\s+KCAL|KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ\/MOLE|\s+KCAL\/MOLE|)|(?<=HF298=)\d+.\d+|(?<=HF298=)\d+.|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+(?:\s+|)\+\/\-(?:\s+|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|))'
#pattern_HF298=r'(?P<h298>(?<=HF298=)(?:\+|\-|)(?:\d+.\d+|\d+.).?(?:\s+|)(?:\+|\s+|)(?:\/|\s+|)(?:\s+|)(?:\-|\s+|)(?:\s+|)(?:\d+.\d+\s+|\d+.|\d+|\s+|).?(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ|\s+KCAL|\s+CAL|\s+KCAL\/MOLE|\s+KJ\/MOLE|).?|(?<=HF298=)\d+.\d+\+\/\-\d+.\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)(?:\s+|)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298=)\d+.\d+\+\/\-\d+.\d+|(?<=HF298=)\d+\+\/\-\d+(?:\s+KJ|\s+KCAL|KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ\/MOLE|\s+KCAL\/MOLE|)|(?<=HF298=)\d+.\d+|(?<=HF298=)\d+.|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+(?:\s+|)\+\/\-(?:\s+|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|))'
pattern_HF0=r'(?P<h0>(?<=HF0=)(?:\+|\-|)\d+.\d+(?:\s+|)\+\/\-(?:\s+|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)\d+.\d+\+\/\-\d+.\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)(?:\+|-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)(?:\+|-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0=)\d+.\d+\+\/\-\d+.\d+|(?<=HF0=)\d+\+\/\-\d+(?:\s+KJ|\s+KCAL|KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ/MOLE|\s+KCAL/MOLE|)|(?<=HF0=)\d+.\d+|(?<=HF0=)\d+.|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/CAL|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|)|(?<=HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|))'
pattern_max_error_value='(?P<max_error_value>(?:\s+\d+(?:K|k|\s+K|\s+k)\s+(?:\d+.\d+\%|\d+.\d+\s+\%|.\d+\s+\%|.\d+\%|\d+.\%|\d+\.\d+\s+\%\.)|(?:\*+|\*+\s+WARNING\s+)d+.\d+\%\*+|(?:\*+|\*+\s+WARNING\s+)\d+.\d+\s+\%\*+|(?:\*+|\*+\s+WARNING\s+).\d+\%\*+|(?:\*+|\*+\s+WARNING\s+)\d+.\%\*+|(?:\*+|\*+\s+WARNING\s+)\d+.\d+\%|(?:\*+|\*+\s+WARNING\s+)\d+\.\d+\s+\%\*+\.|\s+\d+.\d+\%\s+\@\s+\d+(?:K|k|\s+K|\s+k)).*)'
pattern_formula_name_structure='(?P<for_na_struc>(?<=inicio)(?:.)+?(?=\s+final))'
########################################################################################################################
# These patterns are used to delete information once it had been found.
###################################################################################################
pattern_sigma_d='(?P<sigma_d>(?:SIGMA=)\d+|(?:SIGMA=)\s*\d+|(?:SIGMA)(?:\([A-Z]*\)=)*\d+|(?:SIGMA =)\s+\d+|(?:SIGMA =)\s+\d+|(?:SIGMA)(?:\([A-Z]*\)\s+=)*\s+\d+)'
pattern_statwt_d='(?P<statwt_d>(?:STATWT=)\d+|(?:STATWT=)\s*\d+|(?<=STATWT =)\s*\d+|(?<=STATWT =)\d+)'
pattern_t0_statwt_d='(?P<t0_statwt_d>(?:T0\(STATWT\)\=)(?:[0-9\(\,\)\s]*)|(?:T0\(STATWT\)\=)(?:\d+\(\d+\))|(?:T0\=)(?:\d+\s+|\d+\.\s+|\d+\.\d+\s+)(?:STATWT\=)\d+|(?:T0\=)(?:\d+\s+|\d+\.\s+|\d+\.\d+\s+|\d+\(\d+\)\,\d+\(\d+\)|(?:\d+|\d+.\d+)\(\d+\)))'
pattern_be_d='(?P<be_d>(?:BE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?:BE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?:BE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?:BE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?:BE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?(?:\s+CM\-\d+|CM\-\d+|)|(?:BE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?(?:\s+CM\-\d+|CM\-\d+|))'
pattern_we_d='(?P<we_d>(?:WE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){3,7}?|(?:WE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){3,7}?|(?:WE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){3,7}|(?:WE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?|(?:WE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}?|(?:WE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7})'
pattern_wexe_d='(?P<wexe_d>(?:WEXE=)(?:[\[\d+\.\]]*)|(?:WEXE =)(?:[\[\d+\.\]]*)|(?:WEXE = )(?:[\[\d+\.\]]*))'
pattern_alfae_d='(?P<alfae_d>(?:ALFAE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?:ALFAE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?:ALFAE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?:ALPHAE=)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?:ALPHAE =)(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?:ALPHAE = )(?:\d+|\d+\.|\s+\d+|\s+\d+\.|\d+.\d+){2,7}?|(?:ALFAE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?:ALFAE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?:ALFAE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?:ALPHAE=)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?:ALPHAE =)(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7}|(?:ALPHAE = )(?:\[\d+\]|\[\d+\.\]|\[\s+\d+\]|\[\s+\d+\.\]|\[\d+.\d+\]){1,7})'
pattern_IA_d='(?P<ia_d>(?:IA\=)\d+.\d+|(?:IA\=)\s*\d+.\d+|(?:IA =)\s*\d+.\d+|(?:IA\=).\d+|(?:IA \=).\d+|(?:IA\=)\s+.\d+|(?:IA \=)\s*.\d+)'
pattern_IB_d='(?P<ib_d>(?:IB\=)\d+.\d+|(?:IB\=)\s*\d+.\d+|(?:IB =)\s*\d+.\d+|(?:IB\=).\d+|(?:IB \=).\d+|(?:IB\=)\s+.\d+|(?:IB \=)\s*.\d+)'
pattern_IC_d='(?P<ic_d>(?:IC\=)\d+.\d+|(?:IC\=)\s*\d+.\d+|(?:IC =)\s*\d+.\d+|(?:IC\=).\d+|(?:IC \=).\d+|(?:IC\=)\s+.\d+|(?:IC \=)\s*.\d+)'
pattern_IAIBIC_d='(?P<iaibic_d>(?:IAIBIC\=)(?:\d+.\d+E(?:\+|-|\s|)(?:\d{3}|\d+.))|(?:IAIBIC\=)(?:\d+.E(?:\+|-|\s|)\d{3})|(?:IAIBIC\=)(?:\d+E(?:\+|-|\s|)\d{3})|(?:IAIBIC\=)(?:\d+.\d+\s+E(?:\+|-|\s|)\d{3})|(?:IAIBIC\=)(?:\d+.\s+E(?:\+|-|\s|)(?:\d{3}|\d+.\d+))|(?:IAIBIC\=)(?:\d+\s+E(?:\+|-|\s|)\d{3})(?:IAIBIC\=)(?:[0-9\.]*))'
pattern_IA_IB_d='(?P<ia_ib_d>(?:IA\=IB\=)(?:\d+.\d+)|(?:IA=IB=)(?:.\d+))'
pattern_IA_IB_IC_d='(?P<ia_ib_ic_d>(?:IA\=IB\=IC\=)(?:\d+.\d+))'
pattern_A_B_d='(?P<a_b_d>(?:A\=B\=)(?:\d+.\d+))'
pattern_C_d='(?P<c_d>(?:C=)(?:\d+.\d+))'
pattern_A0_d='(?P<a0_d>(?:A0=)(?:\d+.\d+|.\d+))'
pattern_B0_d='(?P<b0_d>(?:B0=)\d+.\d+(?:\s+|)CM\-\d+|(?:B0=)\s+\d+.\d+\s*CM\-\d+|(?:B0=)\d+.\d+CM\-\d+|(?:B0=)\d+.\d+\s+|(?:B0=)\d+.\d+|(?:B0=).\d+|(?:B0=)\d+)'
pattern_C0_d='(?P<c0_d>(?:C0=)(?:\d+.\d+|.\d+))'
pattern_A0_B0_d='(?P<a0_b0_d>(?:A0=B0=)(?:\d+.\d+|.\d+))'
pattern_Ir_d='(?P<ir_d>(?:IR=)(?:\+|\-|\~|)\d+.\d+|(?:IR=).\d+|(?:IR)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|\~|)\d+.\d+|(?:IR = )(?:\+|\-|\~|)\d+.\d+|(?:IR = )(?:\+|\-|\~|).\d+|(?:IR)(?:\([A-Z0-9\-\*]*\)\s+=)*(?:\+|\-|\~|)\s+\d+.\d+)'
#pattern_Ir_d='(?P<ir_d>(?:IR=)\d+.\d+|(?:IR=).\d+|(?:IR)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+|(?<=IR = )\d+.\d+|(?:IR = ).\d+|(?:IR)(?:\([A-Z0-9\-\*]*\)\s+=)*\s+\d+.\d+)'
pattern_rosym_d='(?P<rosym_d>(?:ROSYM=)\d+|(?:ROSYM=)\s*\d+|(?:ROSYM)(?:\([A-Z0-9\-]*\)=)*\d+|(?:ROSYM =)\s+\d+|(?:ROSYM =)\s+\d+|(?:ROSYM)(?:\([A-Z0-9\-]*\)\s+=)*\s+\d+|(?:ROSYM=)\d+.)'
pattern_v1_d=r'(?P<v1_d>\bV(?:[A-Z0-9\-\(\)\s]*)(?:1|2|\(1\)|\(2\)|3|\(3\)|\))(?:\=|\s|)(?:[A-Z0-9\.\-\(\)]*)(?:[+CM|CM|\s+CM\s+|CM\s+|KCAL|\s+KCAL|\s+KCAL\s+|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|\KJ|\s+KJ|\s|1\/CM\s\/\-\.0-9]*)(?=(?:\s| )))'
pattern_v2_d=r'(?P<v2_d>(?:))'
pattern_v3_d=r'(?P<v3_d>(?:))'
pattern_nu_d='(?P<nu_d>(?:NU=)(?:[\d+\(\d+\)\,\s+\.\d+\(\d+\)]*)|(?:NU =)(?:[\d+\(\d+\)\,\s+\.\d+\(\d+\)]*))'
pattern_x_d='(?P<x_d>(?:X\d+=)(?:\+|\-|\s+|\~|)(?:[0-9\.]*))'
pattern_y_d='(?P<y_d>(?:Y\d+=)(?:\+|\-|\s+|\~|)(?:[0-9\.]*))'
pattern_Max_Lst_Error_d='(?P<max_error_d>(?:MAX\sLST\sSQ\sERROR\s)(?:[0-9\,\*\s+\-CP \;AND\&\.\@ K\%\=\(\) H-HREF WARNING]*)(?<![A-Z0-9\.\s\+\=]))'
#pattern_Max_Lst_Error_d='(?P<max_error_D>(?:MAX\sLST\sSQ\sERROR\s)(?:[0-9\,\*\s\-CP AND\&\.\@ K \%\=\(\) H-HREF WARNING]*)(?:\s|)|(?:MAX\sLST\sSQ\sERROR\s)(?:[0-9\,\*\s\-CP AND\&\.\@ K \%\=\(\) H-HREF WARNING]*)(?<![A-Z0-9\.\s\+\=]))'
pattern_REF_d='(?P<ref_d>(?:REF=)(?:[A-Z0-9\s\.\(\)\'\"\-\&\+\,\/\[\]\;]*)(?=\s|)|(?:REF = )(?:[A-Z0-9\s\.\(\)\'\"\-\&\+\,\/\[\]\;]*)(?=\s|))'
pattern_add_info_d='(?P<add_info_d>(?:{)(?:[A-Z0-9\s\#\.\(\)"\-\&\+\,\;\/\[\]\=]*)(?=\}))'
#pattern_add_info_d='(?P<add_info_d>(?:{)(?:.?.?.?|HF298=.?.?.?.?.?.?.?.?.?.?|HF0=.?.?.?.?.?.?.?.?.?.?|REF=)??(?:[a-zA-Z0-9?\s\.\(\)"\-\&\+\,\/\[\]\=]).*(?:\}))'
pattern_HF298_d=r'(?P<h298_d>(?:HF298=)(?:\+|\-|)(?:\d+.\d+|\d+.)(?:\s+|)(?:\+|\s+|)(?:\/|\s+|)(?:\s+|)(?:\-|\s+|)(?:\s+|)(?:\d+.\d+\s+|\d+.|\d+|\s+|)(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ|\s+KCAL|\s+CAL|\s+KCAL\/MOLE|\s+KJ\/MOLE| )|(?:HF298=)\d+.\d+\+\/\-\d+.\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\s+|)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\+\/\-\d+.\d+|(?:HF298=)\d+\+\/\-\d+(?:\s+KJ|\s+KCAL|KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|)|(?:HF298=)\d+.\d+|(?:HF298=)\d+.|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+(?:\s+|)\+\/\-(?:\s+|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|))'
#pattern_HF298_d=r'(?P<h298_d>(?:HF298=)(?:\+|\-|)(?:\d+.\d+|\d+.).?(?:\s+|)(?:\+|\s+|)(?:\/|\s+|)(?:\s+|)(?:\-|\s+|)(?:\s+|)(?:\d+.\d+\s+|\d+.|\d+|\s+|).?(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KJ|\s+KCAL|\s+CAL|\s+KCAL\/MOLE|\s+KJ\/MOLE|).?|(?:HF298=)\d+.\d+\+\/\-\d+.\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)(?:\s+|)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298=)\d+.\d+\+\/\-\d+.\d+|(?:HF298=)\d+\+\/\-\d+(?:\s+KJ|\s+KCAL|KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|)|(?:HF298=)\d+.\d+|(?:HF298=)\d+.|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+(?:\s+|)\+\/\-(?:\s+|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF298\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|))'
pattern_HF0_d=r'(?P<h0_d>(?:HF0=)(?:\+|\-|)\d+.\d+(?:\s+|)\+\/\-(?:\s+|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)\d+.\d+\+\/\-\d+.\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)(?:\+|-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)(?:\+|-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)\d+.\d+\+\/\-\d+.\d+|(?:HF0=)\d+\+\/\-\d+(?:\s+KJ|\s+KCAL|KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0=)\d+.\d+|(?:HF0=)\d+.|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(S\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KCAL\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(L\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(SOLID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0\(LIQUID\)=)(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\s+\+\/\-\s+\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+\+\/\-\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+\+\/\-\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|-|)\d+.\d+\s+\+\/\-\s+\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|)|(?:HF0)(?:\([A-Z0-9\-\*]*\)=)*(?:\+|\-|)\d+.\d+\s+(?:KJ|KCAL|CAL|KCAL\/MOLE|KJ\/MOLE|))'
pattern_max_error_value_d='(?P<max_value_error_d>(?:\s+\d+(?:K|k|\s+K|\s+k)\s+(?:\d+.\d+\%|\d+.\d+\s+\%|.\d+\s+\%|.\d+\%|\d+.\%|\d+\.\d+\s+\%\.)|(?:\*+|\*+\s+WARNING\s+)d+.\d+\%\*+|(?:\*+|\*+\s+WARNING\s+)\d+.\d+\s+\%\*+|(?:\*+|\*+\s+WARNING\s+).\d+\%\*+|(?:\*+|\*+\s+WARNING\s+)\d+.\%\*+|(?:\*+|\*+\s+WARNING\s+)\d+.\d+\%|(?:\*+|\*+\s+WARNING\s+)\d+\.\d+\s+\%\*+\.|\s+\d+.\d+\%\s+\@\s+\d+(?:K|k|\s+K|\s+k)).*)'
pattern_formula_name_structure_d='(?P<for_na_struc_d>(?:\d+-\d+-\d+|N/A|\d+-\d+-\d+\?+|\d+-\d+-\d+\s+\?+)(?:[A-Z0-9\-\s\(\)\+\=]*))'
#pattern_formula_name_structure_d='(?P<for_na_struc_d>(?:inicio)(?:.)+?(?=\s+final))'
########################################################################################################################
dummy_1=['max_error','add_info','h298','h0','y','x','nu','v3','v2','v1','rosym','ir','a0_b0','c0','b0','a0','c','a_b','ia_ib_ic','ia_ib','iaibic','ic','ib','ia','alphae','wexe','we','be','t0_statwt','statwt','sigma','ref','for_na_struc']
dummy_2_0=['Max_Lst_Sq_Error','ADDITIONAL_INFORMATION','HF298','HF0','Y','X','NU','V3','V2', 'V1','ROSYM','Ir','A0=B0','C0','B0','A0','C','A=B','IA=IB=IC','IA=IB','IAIBIC','IC','IB','IA','ALPHAE','WEXE','WE','BE','T0_STATWT','STATWT','SIGMA','REFERENCE','FORMULA_NAME_STRUCTURE']
dummy_2=['Max_Lst_Sq_Error','ADDITIONAL_INFORMATION','HF298','HF0','Y','X','NU','V3','V2', 'V1','ROSYM','Ir','A0=B0','C0','B0','A0','C','A=B','IA=IB=IC','IA=IB','IAIBIC','IC','IB','IA','ALPHAE','WEXE','WE','BE','T0_STATWT','STATWT','SIGMA','REFERENCE','FORMULA_NAME_STRUCTURE']
dummy_3=[pattern_Max_Lst_Error,pattern_add_info,pattern_HF298,pattern_HF0,pattern_y,pattern_x,pattern_nu,pattern_v3,pattern_v2,pattern_v1,pattern_rosym,pattern_Ir,pattern_A0_B0,pattern_C0,pattern_B0,pattern_A0,pattern_C,pattern_A_B,pattern_IA_IB_IC,pattern_IA_IB,pattern_IAIBIC,pattern_IC,pattern_IB,pattern_IA,pattern_alfae,pattern_wexe,pattern_we,pattern_be,pattern_t0_statwt,pattern_statwt,pattern_sigma,pattern_REF,pattern_formula_name_structure]
dummy_3_d=[pattern_Max_Lst_Error_d,pattern_add_info_d,pattern_HF298_d,pattern_HF0_d,pattern_y_d,pattern_x_d,pattern_nu_d,pattern_v3_d,pattern_v2_d,pattern_v1_d,pattern_rosym_d,pattern_Ir_d,pattern_A0_B0_d,pattern_C0_d,pattern_B0_d,pattern_A0_d,pattern_C_d,pattern_A_B_d,pattern_IA_IB_IC_d,pattern_IA_IB_d,pattern_IAIBIC_d,pattern_IC_d,pattern_IB_d,pattern_IA_d,pattern_alfae_d,pattern_wexe_d,pattern_we_d,pattern_be_d,pattern_t0_statwt_d,pattern_statwt_d,pattern_sigma_d,pattern_REF_d,pattern_formula_name_structure_d]

coef_4_re=r"(?:SRUCTURE FOR AUTOMATIC FORMULA CALCULATION SHOULD BE|STRUCTURE FOR AUTOMATIC FORMULA CALCULATION SHOULD BE)"
coef_5_re=r"(?:HF\d+(?:\(S|s\))|HF\d+|REF\=).*"
pv1= re.compile('(?:V\(1\)|V1|V\(1\)|V1|V\([A-Z0-9\-]*\)1|V\([A-Z0-9\-]*\)1)')
pv2= re.compile('(?:V\(2\)|V2|V\(2\)|V2|V\([A-Z0-9\-]*\)2|V\([A-Z0-9\-]*\)2)')
pv3= re.compile('(?:V\(3\)|V3|V\(3\)|V3|V\([A-Z0-9\-]*\)3|V\([A-Z0-9\-]*\)3)')
dummy_v3_final=r'(?P<v3_d>\bV(?:[A-Z0-9\-\(\)\s]*)(?:1|2|\(1\)|\(2\)|3|\(3\)|\))(?:\=|\s|)(?:[A-Z0-9\.\-\(\)]*)(?:[+CM|CM|\s+CM\s+|CM\s+|KCAL|\s+KCAL|\s+KCAL\s+|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|\KJ|\s+KJ|\s|1\/CM\s\/\-\.0-9]*)(?=(?:\s| )))'
dummy_v2_final=r'(?P<v2_d>\bV(?:[A-Z0-9\-\(\)\s]*)(?:1|2|\(1\)|\(2\)|3|\(3\)|\))(?:\=|\s|)(?:[A-Z0-9\.\-\(\)]*)(?:[+CM|CM|\s+CM\s+|CM\s+|KCAL|\s+KCAL|\s+KCAL\s+|CAL|KCAL\/MOLE|KJ\/MOLE|\s+KCAL\/MOLE|\s+KJ\/MOLE|\KJ|\s+KJ|\s|1\/CM\s\/\-\.0-9]*)(?=(?:\s| )))'
dummy_3_vector=len(dummy_3)
#########################################################################################
# Some XML Tags
##################################################################################
dummy_xml_version='<?xml version="1.0" encoding="ISO-8859-1"?>\n'
dummy_comments_code_1='<!-- Thermodyne2XML - Converts Thermodynamic Database for Combustion and -->'+ '\n' + \
'<!-- Air-Pollution Use, by Alexander Burcat - and Branko Ruscic - to an XML file -->'
dummy_comments_code_2='<!-- Copyright (C) 2004, Eitan Burcat, burcat@bigfoot.com -->' +	 '\n' + \
'<!-- Copyright (C) 2005, Reinhardt Pinzon, reinhardtpinzon@yahoo.com, ANL -->\n'
dummy_comments_code_3='<!-- DATE origin and Reference codes: -->' + '\n' + \
'<!-- A-ARGONNE NAT.LABS. -->' + '\n' + \
'<!-- ATcT A- Branko Ruscic, unpublished results from Active Thermochemical Tables v.1.25 using the Core (Argonne) Thermochemical Network v. 1.049 (May 2005).	-->' + '\n' + \
'<!-- B-Ihsan Barin database. -->\n' + \
'<!-- CODA- CODATA Tables. -->\n' + \
'<!-- D-Delaware University. -->\n' + \
'<!-- F-THERGAS calculations. -->\n' + \
'<!-- IU-IUPAC data. -->\n' + \
'<!-- J-JANAF tables.  -->\n' + \
'<!-- G(L)-NASA Glen(former Lewis) Research Center.	 -->\n' + \
'<!-- P- Thermodynamic Research Center (Formerly American Petroleum Institute).	  -->\n' + \
'<!-- R-or Rus or TPIS	Russian Tables (TSIV/TPIS), Gurvich. -->\n' + \
'<!-- S-Louisiana State University (LSU). -->\n' + \
'<!-- T- Technion-Israel Inst. Technology.	-->\n' + \
'<!-- TT-New HF298 adjusted on old polynomial. -->\n'
dummy_reference_xml_tag=['<reference>','<reference_','</reference>']
##################################################################################################
# regular expressions

# Find a CAS, then a new line, then any char until you bump into a new CAS (not-including it).
specie_re = r'(?:\d+-\d+-\d+|N/A).*\n(?:.|\n)*?(?=\d+-\d+-\d+(?:\s|)|N/A)(?!\d+-\d+-\d+-)'
CAS_re = r'(\d+-\d+-\d+|\d+-\d+-\d+\?+|\d+-\d+-\d+\s+\?+|N/A)\s'
phase_re = r".+1\s+\n?.+2\s+\n?.+\s3\s+\n?.+\s4\s"
first_line_re = '(?P<formula>.{17}.?)' + \
'(?P<source>TT?|tt?|RUS|rus|IU|P|p|G|g|J|j|B|b|L|l|CODA|coda|R|r|S|s|HF|hf|D|d|ATCT|ATcT|A|a|F|f|E|e|[TIPS]*|[tips]*)' + \
'\s*' + \
'(?P<date>(?:/)?(?:\d\d|\d)?(?:/?)(?:\d\d|A))' + \
'\s*' + \
'(?:((?:\s*|\*+|\s*\*+)WARNING(?:!|\*+)\s*0?\.?)|' + \
'(?P<elem1>[A-Z]{1,2})\s*(?P<num_atoms1>-?\d+)(?:\.|\s)?(?:\s|\d+)?' + \
'(?P<elem2>[A-Z]{0,2})\s*(?P<num_atoms2>-?\d+)(?:\.|\s)?(?:\s|\d+)?' + \
'(?P<elem3>[A-Z]{0,2})\s*(?P<num_atoms3>-?\d+)(?:\.|\s)?(?:\s|\d+)?' + \
'(?P<elem4>[A-Z]{0,2})\s*(?P<num_atoms4>-?\d+)(?:\.|\s)?(?:\s|\d+)?' + \
')' + \
'(?P<phase>G|L|S|C)\s*' + \
'(?P<t_low>\d*\.\d*)\s*' + \
'(?P<t_high>\d*\.\d*)\s*' + \
'(?P<calc_quality>A|B|C|D|E|F)?\s*' + \
'(?P<molecular_weight>\d*\.\d*)\s*'
# (?P<formula>.{17}.?.?)(?P<source>TT?|RUS|IU|P|G|J|B|L|CODA|R|S|HF|D|A|E|F)\s*(?P<date>(?:/)?(?:\d\d|\d)?(?:/?)(?:\d\d))\s*(?:(\s*WARNING!\s*0?\.?)|(?P<elem1>[A-Z]{1,2})\s*(?P<num_atoms1>-?\d+)\.?(?P<elem2>[A-Z]{0,2})\s*(?P<num_atoms2>-?\d+)\.?(?P<elem3>[A-Z]{0,2})\s*(?P<num_atoms3>-?\d+)\.?(?P<elem4>[A-Z]{0,2})\s*(?P<num_atoms4>-?\d+)\.?)(?P<phase>G|L|S|C)\s*(?P<t_low>\d*\.\d*)\s*(?P<t_high>\d*\.\d*)\s*(?P<calc_quality>A|B|C|D|E|F)?\s*(?P<molecular_weight>\d*\.\d*)\s*
###########################################################################################################
#						   Data preparation:
if (sys.platform[:3] == "win"):
   ############### USE THESE COMMANDS IN WINDOWS SYSTEM #######################################
   #						  Open Input File
   try:
	  data = open('BURCAT_THR.txt', "r+").read()
	  data += '\n0-0-0 ' # this was added due to the way we recognise species	
   except IOError:
	  print >> sys.stderr, "File could not be opened"
	  sys.exit( 1 )
   #						  Open XML Output File
   #try:
   #   file = open('BURCAT_THR.xml', "w")
	  #data += '\n0-0-0 ' # this was added due to the way we recognise species	 
   #except IOError:
   #   print >> sys.stderr, "File could not be opened"
   #   sys.exit( 1 )
else:
   ############### USE THESE COMMANDS IN UNIX SYSTEM ############################################
   if len(sys.argv) != 2:
	  print "Usage: ./Thermodyn2XML.py filename"
	  sys.exit()
   data = open(sys.argv[1], "r").read()
   # data = open(r'1.txt', "r").read() <-It is commented in the original code.
   data += '\n0-0-0' # this was added due to the way we recognise species


#						   Open XML Output File
try:
   file = open('BURCAT_THR.xml', "w")
   #data += '\n0-0-0 ' # this was added due to the way we recognise species	  
except IOError:
   print >> sys.stderr, "File could not be opened"
   sys.exit( 1 )
##############################################################################################

first_line = re.compile(first_line_re)

coef_re = r"(?:\+|-)?\d+.\d+(?:E|\s+|\s+E|D|\s+D)(?:\+|-|\s)(?:\d{2}|\s+)"
coef = re.compile(coef_re)

class phase_desc:
	description = None
	coefs_list = None

class xml_generator:
	def __cas_element__(self, CASs_list):
		result = '<specie'
		if CASs_list != []:
			result += ' CAS="' + ' '.join(CASs_list) + '"'
		result += '>\n'
		return result
		
	def __phase_element__(self, phase):
		result = '<phase>\n'
		result += '	 <formula>' + re.sub('&', '&amp;',phase.description.group('formula')).rstrip(' ') + '</formula>\n'
		result += '	 <source>' + phase.description.group('source') + '</source>\n'
		result += '	 <date>' + phase.description.group('date') + '</date>\n'
		result += '	 <elements>\n'
		for elem_idx in [1, 2, 3, 4]:
			if phase.description.group('elem' + str(elem_idx)) != None:
				if phase.description.groupdict()['elem' + str(elem_idx)] != "":
					result += '	   <element name="' + phase.description.groupdict()['elem' + str(elem_idx)] + '"'
					result += ' num_of_atoms="' + phase.description.group('num_atoms' + str(elem_idx)) + '"/>\n' 
		result += '	 </elements>\n'
		result += '	 <phase>' + phase.description.group('phase') + '</phase>\n'
		result += '	 <temp_limit low="' + phase.description.group('t_low') + '" high="' + phase.description.group('t_high') + '"/>\n'
		if phase.description.group('calc_quality') != None:
			result += '	 <calc_quality>' + phase.description.group('calc_quality') + '</calc_quality>\n'
		result += '	 <molecular_weight>' + phase.description.group('molecular_weight') + '</molecular_weight>\n'
		result += '	 <coefficients>\n'
		result += '	   <range_1000_to_Tmax>\n'
		for i in range(7):
			result += '		 <coef name="a' + str(i+1) + '">' + phase.coefs_list[i] + '</coef>\n'
		result += '	   </range_1000_to_Tmax>\n'
		result += '	   <range_Tmin_to_1000>\n'
		for i in range(7):
			result += '		 <coef name="a' + str(i+1) + '">' + phase.coefs_list[7+i] + '</coef>\n'
		result += '	   </range_Tmin_to_1000>\n'
		result += '	   <hf298_div_r>'+phase.coefs_list[14]+'</hf298_div_r>\n'
		result += '	 </coefficients>\n'
		result += '</phase>\n'
		
		return result

	def add_specie(self, CASs_list, result_properties,phases_list):
		result = ''
		result += self.__cas_element__(CASs_list)
		if len(strip(result_properties)) !=0:
		   result=rstrip(result)
		   result +=result_properties
		for phase in phases_list:
			result += self.__phase_element__(phase)

		result += '</specie>\n'
		return result
	
def dashrepl(matchobj):
	matchobj=re.sub(r'-','_',matchobj.group(0))
	return matchobj
	
def dashrepl_b(matchobj):
	matchobj=re.sub(r'_','-',matchobj.group(0))
	return matchobj	   

def dashrepl_c(matchobj):
	matchobj=re.sub(r'(2003-024-1-100)','',matchobj.group(0))
	return matchobj

data = re.sub("(?:FC-\d+-\d+-\d+)", dashrepl, data)
data = re.sub("(?:\(\d+-\d+-\d{1}-\d+\))", dashrepl_c, data)

species = re.compile(specie_re).findall(data)
gen = xml_generator()

##########################################################
#				 Output Files : On Screen and saved in a XML File
###########################################################
print dummy_xml_version
print dummy_comments_code_1
print dummy_comments_code_2
print dummy_comments_code_3
print '<database>'
print >> file,dummy_xml_version
print >> file,dummy_comments_code_1
print >> file,'\n'
print >> file,dummy_comments_code_2
print >> file,'\n'
print >> file,dummy_comments_code_3
print >> file,'\n'
print >> file,'<database>'
print >> file,'\n'
############################################################
for specie in species:
	CASs = re.compile(CAS_re).findall(specie)
	phases = re.compile(phase_re).findall(specie)
	phde_list = []
	label_number_string_reference=[]
	length_string_reference=0
	resultados=[]
	index_insert_reference=0
###############################################################################
	range_ik=[]
	specie_new=re.sub(phase_re,'', specie)	   
	specie_new=upper(specie_new)
	specie_new=fill(specie_new,width=len(specie_new))
	specie_new=re.sub(r'\s+',r' ',specie_new)
	specie_new=re.sub(r'(?:\s+=\s+|\s+=)', '=',specie_new)
	specie_new=re.sub(r'(?:LEAST|LIST|LST\.)', 'LST',specie_new)
	specie_new=re.sub(r'(?:MAX\.)', 'MAX',specie_new)
	specie_new=re.sub(r'(?:SQ\.)', 'SQ',specie_new)
	specie_new_fornastru=re.sub(r'(?:\d+-\d+-\d+|N/A|\d+-\d+-\d+\s+OR\s+-\d+-\d+|\d+-\d+-\d+\s+AND\s+-\d+-\d+|\d+-\d+-\d+\s+AND\s+\d+-\d+-\d+\s+OR\s+\d+-\d+-\d+|\d+-\d+-\d+\?+|\d+-\d+-\d+\s+\?+|\d+-\d+-\d+\s+OR\d+-\d+-\d+|\d+-\d+-\d+\s+AND\s+\d+-\d+-\d+\s+AND\s+\d+-\d+-\d+|\d+-\d+-\d+\s+AND\/OR\s+\d+-\d+-\d+)','inicio', specie_new)
	#specie_new_fornastru=re.sub(r'(?:\d+-\d+-\d+|N/A|\d+-\d+-\d+\s+OR\s+-\d+-\d+|\d+-\d+-\d+\s+AND\s+-\d+-\d+|\d+-\d+-\d+\s+AND\s+\d+-\d+-\d+\s+OR\s+\d+-\d+-\d+|\d+-\d+-\d+\?+|\d+-\d+-\d+\s+\?+|\d+-\d+-\d+\s+OR\d+-\d+-\d+|\d+-\d+-\d+\s+AND\s+\d+-\d+-\d+\s+AND\s+\d+-\d+-\d+|\d+-\d+-\d+\s+AND\/OR\s+\d+-\d+-\d+)','inicio', specie_new)
	specie_new_fornastru=re.sub(r'inicio\s+OR\s+inicio|inicio\s+AND\s+inicio|inicio\s+AND\s+inicio\s+OR\s+inicio|ORinicio|inicio\s+ORinicio|inicio\s+AND\s+inicio\s+AND\s+inicio','inicio', specie_new_fornastru)
	#specie_new_fornastru=re.sub(r'inicio\s+OR\s+inicio|inicio\s+AND\s+inicio|inicio\s+AND\s+inicio\s+OR\s+inicio|ORinicio','inicio', specie_new_fornastru)
	specie_new_fornastru=re.sub(r'inicio\s+OR\s+inicio|inicio\s+AND\s+inicio|inicio\s+AND/OR\s+inicio','inicio', specie_new_fornastru)
	specie_new_fornastru=re.sub("(?:FC_\d+_\d+_\d+)", dashrepl_b, specie_new_fornastru)
	#print 'specie_new_fornastru',specie_new_fornastru
	#specie_new_fornastru=re.sub(r'inicio\s+OR\s+inicio','inicio', specie_new_fornastru)
	result_vector=[]
	result_properties=''
	for ik in range(len(dummy_3)):
			p=[]
			op0=[]
			pp1=None
			pp2=None
			pp3=None
			op00=''
			if dummy_2[ik]=='A0=B0':
				p=re.findall(r'(?:\bA0=B0=|\bA0=B0\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
				   dummy_xml_propierty=re.sub('=', '_',dummy_xml_propierty)
			elif dummy_2[ik]=='C0' :
				p=re.findall(r'(?:\bC0=|\bC0\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='B0' :
				p=re.findall(r'(?:\bB0=|\bB0\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='A0' :
				p=re.findall(r'(?:\bA0=|\bA0\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='C' :
				p=re.findall(r'\bC\=|\bC \=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='A=B' :
				p=re.findall(r'\bA=B=|\bA=B\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
				   dummy_xml_propierty=re.sub('=', '_',dummy_xml_propierty)
			elif dummy_2[ik]=='IA=IB=IC' :
				p=re.findall(r'\bIA=IB=IC=|\bIA=IB=IC\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
				   dummy_xml_propierty=re.sub('=', '_',dummy_xml_propierty)
			elif dummy_2[ik]=='IA=IB' :
				p=re.findall(r'\bIA=IB=|\bIA=IB\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
				   dummy_xml_propierty=re.sub('=', '_',dummy_xml_propierty)
			elif dummy_2[ik]=='IAIBIC' :
				p=re.findall(r'\bIAIBIC=|\bIAIBIC\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='IC' :
				p=re.findall(r'\bIC=|\bIC\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='IB' :
				p=re.findall(r'\bIB=|\bIB\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='IA' :
				p=re.findall(r'\bIA=|\bIA\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='H0' :
				p=re.findall(r'\bH0=|\bH0\s+=',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='ALPHAE' :
				p=re.findall(r'(?:\bALFAE=|\bALPHAE=|\bALFAE\s+=|\bALPHAE\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='WEXE' :
				p=re.findall(r'(?:\bWEXE=|\bWEXE\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='WE' :
				p=re.findall(r'(?:\bWE=|\bWE\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='BE' :
				p=re.findall(r'(?:\bBE=|\bBE\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='Y' :
				p=re.findall(r'(?:\bY\d+=|\bY\d+\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='X' :
				p=re.findall(r'(?:\bX\d+=|\bX\d+\s+=)',specie_new)
				if p != []:
				   p=re.findall(dummy_3[ik],specie_new)
				   dummy_group_name=dummy_1[ik]
				   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]=='V1' :
				   p=re.findall(dummy_3[ik],specie_new)
				   if  p != []:
						 for i in range(len(p)):
							 pp1=pv1.match(strip(str(p[i])))
							 if pp1 !=None :
								op0.append(p[i])
						 if op0 !=[]:
							op00=join(op0)
							op00=fill(op00,width=len(op00))
							op00=strip(op00)
							op00=re.sub(r'\s+',' ',op00)
							op_dummy_v1=re.findall(r'(?<=V1\=)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',op00)
							op00=re.sub(r'(?:V1\=)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',' ',op00)
							op00=re.sub(r'(?:\sV)','   V',op00)
							op_dummy_v1_=re.findall(r'(?<=V1)(?:[A-Z0-9\=\(\)]*)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s\s|)',op00)
							op00=re.sub(r'(?:V1)(?:[A-Z0-9\=\(\)]*)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s\s|)',' ',op00)
							op_dummy_v_1_=re.findall(r'(?<=V\(1\)\=)(?:[A-Z0-9\.\-]*\s|[0-9\-\.\s\(\)]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',op00)
							op00=re.sub(r'(?:V\(1\)\=)(?:[A-Z0-9\.\-]*\s|[0-9\-\.\s\(\)]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',' ',op00)
							op_dummy_v_1_ii=re.findall(r'(?<=V\(1\))(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',op00)
							op00=re.sub(r'(?:V\(1\))(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',' ',op00)
							op00=strip(op00)
							op_dummyv1=re.findall(r'(?<=V)(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',op00)
							op_dummy_v1.extend(op_dummy_v1_)
							op_dummy_v1.extend(op_dummy_v_1_)
							op_dummy_v1.extend(op_dummy_v_1_ii)
							op_dummy_v1.extend(op_dummyv3)
							op00=re.sub(r'(?:V)(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)','',op00)
							op00=strip(op00)
							p=[]
							p=op_dummy_v1
							dummy_group_name=dummy_1[ik]
							dummy_xml_propierty=dummy_2[ik]
						 else:
							 p=[]
			elif dummy_2[ik]=='V2' :
				   p=re.findall(dummy_3[ik],specie_new)
				   if p != []:
						 for i in range(len(p)):
							 pp2=pv2.match(strip(str(p[i])))
							 if pp2 !=None :
								op0.append(p[i])
						 if op0 !=[]:
							op00=join(op0)
							op00=fill(op00,width=len(op00))
							op00=strip(op00)
							op00=re.sub(r'\s+',' ',op00)
							op_dummy_v2=re.findall(r'(?<=V2\=)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',op00)
							op00=re.sub(r'(?:V2\=)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',' ',op00)
							op00=re.sub(r'(?:\sV)','   V',op00)
							op_dummy_v2_=re.findall(r'(?<=V2)(?:[A-Z0-9\=\(\)]*)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s\s|)',op00)
							op00=re.sub(r'(?:V2)(?:[A-Z0-9\=\(\)]*)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s\s|)',' ',op00)
							op_dummy_v_2_=re.findall(r'(?<=V\(2\)\=)(?:[A-Z0-9\.\-]*\s|[0-9\-\.\s\(\)]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',op00)
							op00=re.sub(r'(?:V\(2\)\=)(?:[A-Z0-9\.\-]*\s|[0-9\-\.\s\(\)]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',' ',op00)
							op_dummy_v_2_ii=re.findall(r'(?<=V\(2\))(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',op00)
							op00=re.sub(r'(?:V\(2\))(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',' ',op00)
							op00=strip(op00)
							op_dummyv2=re.findall(r'(?<=V)(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',op00)
							op_dummy_v2.extend(op_dummy_v2_)
							op_dummy_v2.extend(op_dummy_v_2_)
							op_dummy_v2.extend(op_dummy_v_2_ii)
							op_dummy_v2.extend(op_dummyv2)
							op00=re.sub(r'(?:V)(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)','',op00)
							op00=strip(op00)
							p=[]
							p=op_dummy_v2
							dummy_group_name=dummy_1[ik]
							dummy_xml_propierty=dummy_2[ik]
						 else:
							 p=[]
			elif dummy_2[ik]=='V3' :
				   p=re.findall(dummy_3[ik],specie_new)
				   if p != []:
						 for i in range(len(p)):
							 pp3=pv3.match(strip(str(p[i])))
							 if pp3 !=None :
								op0.append(p[i])
						 if op0 !=[]:
							op00=join(op0)
							op00=fill(op00,width=len(op00))
							op00=strip(op00)
							op00=re.sub(r'\s+',' ',op00)
							op_dummy_v3=re.findall(r'(?<=V3\=)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',op00)
							op00=re.sub(r'(?:V3\=)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',' ',op00)
							op00=re.sub(r'(?:\sV)','   V',op00)
							op_dummy_v3_=re.findall(r'(?<=V3)(?:[A-Z0-9\=\(\)]*)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s\s|)',op00)
							op00=re.sub(r'(?:V3)(?:[A-Z0-9\=\(\)]*)(?:[0-9\-\.\s]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s\s|)',' ',op00)
							op_dummy_v_3_=re.findall(r'(?<=V\(3\)\=)(?:[A-Z0-9\.\-]*\s|[0-9\-\.\s\(\)]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',op00)
							op00=re.sub(r'(?:V\(3\)\=)(?:[A-Z0-9\.\-]*\s|[0-9\-\.\s\(\)]*)(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-\.]*)(?=\s|)',' ',op00)
							op_dummy_v_3_ii=re.findall(r'(?<=V\(3\))(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',op00)
							op00=re.sub(r'(?:V\(3\))(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',' ',op00)
							op00=strip(op00)
							op_dummyv3=re.findall(r'(?<=V)(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)',op00)
							op_dummy_v3.extend(op_dummy_v3_)
							op_dummy_v3.extend(op_dummy_v_3_)
							op_dummy_v3.extend(op_dummy_v_3_ii)
							op_dummy_v3.extend(op_dummyv3)
							op00=re.sub(r'(?:V)(?:\=|\s+|)(?:[A-Z0-9\=]*|[\sA-Z0-9\=]*|[\-\+\(\)A-Z0-9\=]*)(?:[0-9\.])(?:[CM KCAL CAL \/ MOLE KJ\/MOLE \s 0-9\-]*)','',op00)
							op00=strip(op00)
							p=[]
							p=op_dummy_v3
							dummy_group_name=dummy_1[ik]
							dummy_xml_propierty=dummy_2[ik]
						 else:
							 p=[]
			elif dummy_2[ik]=='FORMULA_NAME_STRUCTURE':
			   if re.search(r'final',specie_new_fornastru) == None:
				  specie_new_fornastru = specie_new_fornastru + ' final'
			   p=re.findall(dummy_3[ik],specie_new_fornastru)
			   dummy_group_name=dummy_1[ik]
			   dummy_xml_propierty=dummy_2[ik]
			elif dummy_2[ik]!='FORMULA_NAME_STRUCTURE':	  
				p=re.findall(dummy_3[ik],specie_new)
				dummy_group_name=dummy_1[ik]
				dummy_xml_propierty=dummy_2[ik]
			length_string=len(p)
			if length_string != 0:
			   range_ik.append(ik)
			   if dummy_2[ik]=='V3':
				  dummy_3_d[ik]=dummy_v3_final
				  specie_new_fornastru=re.sub(dummy_3_d[ik],'final',specie_new_fornastru)
				  dummy_3_d[ik]=r'(?:)'
				  specie_new=re.sub(dummy_3_d[ik],'',specie_new)
			   elif dummy_2[ik]=='V2':
				  dummy_3_d[ik]=dummy_v2_final
				  specie_new_fornastru=re.sub(dummy_3_d[ik],'final',specie_new_fornastru)
				  dummy_3_d[ik]=r'(?:)'				  
				  specie_new=re.sub(dummy_3_d[ik],'',specie_new)
			   else:   
				   specie_new_fornastru=re.sub(dummy_3_d[ik],'final',specie_new_fornastru)
				   specie_new=re.sub(dummy_3_d[ik],'',specie_new)
			   result_properties+= '	</' +lower(dummy_xml_propierty) + '>\n'
			   p.reverse()
			   for jk in range(length_string):
					if dummy_2[ik]=='REFERENCE':
					   label_number_string_reference.append(str(length_string-jk))
					   length_string_reference=len(p)
					   p[jk]=re.sub('REF', '', p[jk])
					   p[jk]=re.sub(coef_4_re, '', p[jk])
					   p[jk]=re.sub('&', '&amp;',p[jk]) # Replacement of '&' symbol
					if dummy_2[ik]=='Max_Lst_Sq_Error':
					   p[jk]=re.sub('&', '&amp;', p[jk])
					if dummy_2[ik]=='ADDITIONAL_INFORMATION':
					   p[jk]=re.sub('&', '&amp;', p[jk])
					if dummy_2[ik]=='FORMULA_NAME_STRUCTURE':
					   p[jk]=re.sub('&', '&amp;', p[jk])
					result_properties += '		 <' + lower(dummy_xml_propierty)+'_'+str(length_string-jk) + '>'+ strip(p[jk]) + '</' + lower(dummy_xml_propierty) + '_'+str(length_string-jk)+'>' +'\n'	 
			   result_properties=result_properties + '	  <' + lower(dummy_xml_propierty) + '>\n'				 
	result_properties=split(result_properties,sep='\n')
	result_properties.reverse()
	ij_result_properties=[]
	lij_result_properties=0
	for x in result_properties[:]: # make a slice copy of the entire list
		resultados.append(x)
	for opq in range(len(resultados)):
		resultados[opq]=strip(str(resultados[opq])) 
	if resultados.count('<hf0>') !=0:
		 index_insert_reference=resultados.index('<hf0>')
	elif resultados.count('<hf298>') !=0:
		 index_insert_reference=resultados.index('<hf298>')
	elif resultados.count('<additional_information>') !=0:
		 index_insert_reference=resultados.index('<additional_information>')
	elif resultados.count('<max_lst_sq_error>') !=0:
		 index_insert_reference=resultados.index('<max_lst_sq_error>')
	elif resultados!=['']: 
		 index0=re.sub('</','<', str(resultados[-1:])) 
		 index0=re.sub('\[','',index0)
		 index0=re.sub('\]','',index0)
		 index0=re.sub('\'','',index0)
		 index_insert_reference=resultados.index(index0)
	for il in range(len(result_properties)):
		k_result_properties_string=str(result_properties[il])
		for lmn in range(len(dummy_reference_xml_tag)):
					 if lmn== 1:
						for nml in range(length_string_reference):
							v=label_number_string_reference[nml] + '>'	   
							dummy_reference_xml_tag_p=dummy_reference_xml_tag[lmn] + v
							h_result_properties_find=find(strip(k_result_properties_string),dummy_reference_xml_tag_p)
							dummy_reference_xml_tag_p=''
							if h_result_properties_find !=-1:
							   ij_result_properties.append(il)
							   lij_result_properties=lij_result_properties+1		
					 else:
						 dummy_reference_xml_tag_p=dummy_reference_xml_tag[lmn]
						 h_result_properties_find=find(strip(k_result_properties_string),dummy_reference_xml_tag_p)
						 if h_result_properties_find !=-1:
							ij_result_properties.append(il)
							lij_result_properties=lij_result_properties+1
	ij_result_properties.reverse()
	for ikl in range(len(ij_result_properties)):
		result_properties.insert(index_insert_reference,result_properties[ij_result_properties[ikl]])
	ij_result_properties.reverse()
	while  lij_result_properties > 0:
		result_properties.remove(result_properties[ij_result_properties[0]])
		lij_result_properties-=1
	result_properties=join(result_properties,sep='\n')
	for phase in phases:
		phde = phase_desc()
		phase = phase.expandtabs()
		phde.description = first_line.search(phase[0:80])
		phde.coefs_list = coef.findall(phase[81:-1])
		phde_list.append(phde)
	result_properties= result_properties + '\n'
	try:
		a = gen.add_specie(CASs, result_properties,phde_list)
	except:
		print "!!! Failed on "+specie
		# should raise exception: raise
		# for now, fail silently
		a= "<!-- COULD NOT CONVERT TO XML  -->\n"
		
	print a
	print >> file,'\n'
	print >> file, '<!-- \n'+specie+' -->\n'
	print >> file,a
	print >> file,'\n'
print '</database>'
# file.write('\n')
print >> file,'</database>'
file.close()
# Correction to the database that have to be made in order that this program will run:
# Replace 50888=73-8 with 50888-73-8C6H11  2M2en4yl
# BF3,B2O3(L),C6H4O2  O=C6H4=O should have O instead of 0
# 740-42-8	 added 0s to coef 1303-86-2 3889-76-7 75-69-4 2108-20-5 2108-20-5 33272-71-8
# 3474-12-2 75-43-4
# Contains Ds in exponent instead of Es in many places
# 1070-74-2 2781-85-3 - missing 0 in coef
# 106-51-4 Should contain OO instead of 00 in the elements part.
# 106-51-4 contains 9 instead of an E.
# 136202-28-3 119225-15-9 C6H9 3-Methenyl-Cyclopentene	 CY-C5H7-CH2* missing coef missing coef
# + in coef 287-12-7
#  should have 0.000000 as last coef
# 115383-22-7 or 135105-58-7 contains many errors with the 0s there.
# 24203-36-9 contains a G in one of the coefs
# 7440-01-9 contains unreadable 0s 7704-34-9 7704-34-9
