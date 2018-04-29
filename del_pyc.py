# delete all *.pyc from project-path

import os
path = 'D:\python-project\mxonline'  # project-paht
for prefix, dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.pyc'):
            filename = os.path.join(prefix, name)
            print('del:' + filename)
            os.remove(filename)