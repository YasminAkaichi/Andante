from aloe.utils import multiple_replace
import os

END_PATH = []

def replace_names_everywhere(replacement):
    def change_text(text):
        return multiple_replace(replacement, text)

    l = os.listdir()
    for name in l:
        if name in END_PATH or '__pycache__'==name[-11:]:
            continue

        if os.path.isfile(name):
            print(name)
            if '.ipynb' in name or '.py' in name or '.pl' in name:
                iname, oname = name, multiple_replace(replacement, name)
                with open(iname, 'r') as f_in:
                    t_in  = f_in.read()
                    t_out = change_text(t_in)
                with open(oname, 'w') as f_out:
                    f_out.write(t_out)
                if iname!=oname:
                    os.remove(iname)

        else:
            l_ = ['%s/%s' % (name, e) for e in os.listdir(name)]
            l.extend(l_)
        

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    
    def fun(arg):
        t = arg.split(':')
        if len(t)>2:
            raise ValueError("%s is not a valid input" % s)

        output = []
        for el in t:
            if el[0]=='"' and el[-1]=='"':
                el = el[1:-1]
            output.append(el)
        return tuple(output)

    replacement = dict()
    for arg in args:
        key, value = fun(arg)
        replacement[key] = value
     
    replace_names_everywhere(replacement)