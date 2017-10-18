def output(var_name, var):
    print '---------------------------%s-----------------------------' % var_name
    print var
    print '------------------------------------------------------------'

def output_file(file):
    with open(file, 'r') as f:
        output('file content', f.read())
