"""
Host system is missing dependencies to run browsers. ║
║ Missing libraries:                                   ║
║     libgstcodecparsers-1.0.so.0                      ║
║     libflite.so.1                                    ║
║     libflite_usenglish.so.1                          ║
║     libflite_cmu_grapheme_lang.so.1                  ║
║     libflite_cmu_grapheme_lex.so.1                   ║
║     libflite_cmu_indic_lang.so.1                     ║
║     libflite_cmu_indic_lex.so.1                      ║
║     libflite_cmulex.so.1                             ║
║     libflite_cmu_time_awb.so.1                       ║
║     libflite_cmu_us_awb.so.1                         ║
║     libflite_cmu_us_kal16.so.1                       ║
║     libflite_cmu_us_kal.so.1                         ║
║     libflite_cmu_us_rms.so.1                         ║
║     libflite_cmu_us_slt.so.1                         ║
║     libavif.so.13                                    ║
║     libx264.so
"""

import re

a = "欢迎您：meiduo001 退出"
# welcome_text = re.compile(r"欢迎您：.+ 退出")
#
# r = re.search(r"欢迎您：(.+?) 退出", welcome_text).group(1)
# print(r)
result = re.findall(r'[a-zA-Z0-9]', a)
username = re.search(r'欢迎您：([a-zA-Z0-9]+) 退出', a).group(1)
print(username)
