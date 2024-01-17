import os
import sys
import json
import winreg

STARTS = 'GENERAL_DATA_V2_ActionBindingLocalDataDic'
STARTG = 'GENERAL_DATA_V2_ActionGroupBindingLocalDataDic'
JSONS = 's.json'
JSONG = 'g.json'

VERSION_FILE = '.version'
ver = 0
if os.path.exists('.version'):
    ver = int(open(VERSION_FILE, 'r').read().split()[0]) + 1
else:
    open(VERSION_FILE, 'w').write('0')

a = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    'Software\\miHoYo\\崩坏3',
    0,
    winreg.KEY_ALL_ACCESS
)

b = winreg.QueryInfoKey(a)

regs = None
regg = None
for i in range(b[1]):
    c = winreg.EnumValue(a, i)
    if c[0].startswith(STARTS):
        regs = c
    elif c[0].startswith(STARTG):
        regg = c
    if regs and regg:
        break

assert regs is not None
assert regg is not None


def rencode(j: dict) -> bytes:
    return json.dumps(j).replace(' ', '').encode()+b'\x00'


js = json.loads(regs[1][:-1])
assert rencode(js) == regs[1]

jg = json.loads(regg[1][:-1])
assert rencode(jg) == regg[1]

open('s%d.json' % ver, 'w').write(json.dumps(js, skipkeys=True, indent=4))
open('g%d.json' % ver, 'w').write(json.dumps(jg, skipkeys=True, indent=4))
open(VERSION_FILE, 'w').write(str(ver))

b = None
print('Modify the keys and save as `%s` and `%s`.' % (JSONS, JSONG))
print('Type "OK".')
while b != 'OK':
    b = input('>>> ')

if os.path.exists(JSONS):
    newjs = json.loads(open(JSONS, 'rb').read())
    winreg.SetValueEx(a, regs[0], 0, regs[2], rencode(newjs))
    print(regs[0], 'edited.')

if os.path.exists(JSONG):
    newjg = json.loads(open(JSONG, 'rb').read())
    winreg.SetValueEx(a, regg[0], 0, regg[2], rencode(newjg))
    print(regg[0], 'edited.')

# winreg.FlushKey(a)
winreg.CloseKey(a)
