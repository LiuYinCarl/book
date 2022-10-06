# 本脚本用来简化 tex 脚本的编写

import time
import os
import sys
import shutil



tex_file_name = "main.tex"
backup_dir = "./backup/"


patterns = {
    "==begin_sh_code": r"\begin{lstlisting}[language=bash, numbers=left, numbersep=1em, numberstyle=\footnotesize , breaklines=true]",

    "==end_sh_code": r"\end{lstlisting}",

    "==begin_py_code": r"\begin{lstlisting}[language=Python, numbers=left, numbersep=1em, numberstyle=\footnotesize , breaklines=true]",

    "==end_py_code": r"\end{lstlisting}",

    "==begin_c_code": r"\begin{lstlisting}[language=C, numbers=left, numbersep=1em, numberstyle=\footnotesize , breaklines=true]",

    "==end_c_code": r"\end{lstlisting}",


    
}

def backup():
    timestr = time.strftime('%H:%M:%S', time.localtime())
    new_tex_file_name = "{}_{}".format(timestr, tex_file_name)

    src = tex_file_name
    dst = "{}{}".format(backup_dir, new_tex_file_name)

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.copy(src, dst)
    

def replace():
    new_lines = []
    with open(tex_file_name, "r") as f:
        lines = f.readlines()

        for line in lines:
            if line[0:2] == "==" and line.strip() in patterns:
                line = patterns[line.strip()] + '\n'
            new_lines.append(line)
            
    with open(tex_file_name, "w") as f:
        f.write("".join(new_lines))

def run():
    backup()
    replace()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        tex_file_name = sys.argv[1]
    if not os.path.exists(tex_file_name):
        print("[ERROR] file '{}' not exist.".format(tex_file_name))
        exit(1)
    if os.path.splitext(tex_file_name)[-1] != ".tex":
        print("[ERROR] only accept file with suffix '.tex'.")
        exit(1)

    run()
        
