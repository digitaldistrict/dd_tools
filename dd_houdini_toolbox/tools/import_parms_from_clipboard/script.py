import hou


try:
    from PyQt5 import QtWidgets, QtCore, QtGui
except ImportError:
    from Qt import QtWidgets, QtCore, QtGui

error_count = 0

m = None
if len( hou.selectedNodes() ) > 0:
    m = hou.selectedNodes()[0]

clipboard = QtWidgets.QApplication.clipboard()
text = clipboard.text()
lines = text.splitlines()

if lines.count > 1:
    if lines[0].startswith('#'):
        type = lines[0][1:]

        if m == None:
            try:
                parent = cur_obj = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd()
                if parent != None:
                    m = parent.createNode(type)
                    m.moveToGoodPosition()
                    m.setSelected(True, True)
            except:
                pass

        if m != None:
            if m.type().name() == type:
                for line in lines[1:]:
                    ls = line.split(',', 1)
                    if len(ls) == 2:
                        try:
                            m.parm(ls[0]).set(eval(ls[1]))
                        except:
                            print('cannot setting parameter: ' + ls[0])
                            error_count += 1

                if error_count > 0:
                    print('material parameters imported with: ' + str(error_count) + ' errors')
                else:
                    print('material parameters successfully imported')
            else:
                print('cannot apply clipboad values, wrong type!')
        else:
            print('cannot apply clipboad values, wrong type!')
    else:
        print('cannot apply clipboad values, wrong type!')
else:
    print('nothing to import')