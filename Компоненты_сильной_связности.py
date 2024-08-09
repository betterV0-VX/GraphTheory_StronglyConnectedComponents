from Tkinter import *
from Tkinter import messagebox
from math import sin, cos, pi, sqrt
from numpy import *
import matplotlib.pyplot as plt

def mplt():

    text2.delete(1.0, END)
    text3.delete(1.0, END)
    text4.delete(1.0, END)

    h = 20
    color_list = [
    'crimson', 'royalblue', 'black',
    'darkorange', 'dimgrey', 'gold',
    'aqua', 'deeppink', 'green', 'lightgreen',
    'peru', 'tomato', 'teal', #13
    'darkcyan', 'maroon', 'lightcoral', 'magenta',
    'pink', 'blue', 'olivedrab'
    ]
    n = '{}'.format(text1.get(1.0, END))
    n = n.replace('\n', '')
    n = n.replace('\t', '')
    n = n.replace(' ','')
    n = n.replace('[', '')
    n = n.replace(']', '')
    s = n.count('0') + n.count('1')
    q = len(n)
    p = []

    #1, 4, 9.. 20^2
    for l in range(1, h+1):
        p.append(l*l)

    if (s != q) or (s not in p):
        clicked_info()
        return

    sq = int(sqrt(q))
    a = zeros(shape=(sq,sq), dtype=int)
    k = 0

    for i in range(sq):
      for j in range(sq):
            a[i, j] = int(n[k])
            k+=1

            #1
    R = 10
    angleZero = 0
    angle = 2*round(pi, 8)/sq
    x = 0
    y = 0
    ax = zeros(shape=(sq))
    ay = zeros(shape=(sq))

    for i in range(sq):
        x = R*cos(angleZero)
        y = R*sin(angleZero)
        ax[i] = x
        ay[i] = y
        angleZero+=angle

    T = T_matrix(a, sq)
    S = S_matrix(T, sq)
    S_components_graph(S, sq, a, color_list, h, ax, ay)
    text2.insert(1.0, T)
    text3.insert(1.0, S)

    plt.title('Исходный граф')
    plt.show()

def clicked_info():
    messagebox.showinfo('Правила заполнения', """1) Заполнить матрицу смежности значениями из {0,1}
     размера (N x N) (N>=1). По 1й строке считается кол-во\n     вершин. Можно вставлять матрицы из полей T, S
     (со скобками [ ])\n\n2) Нажать кнопку > \n\n3) Получить промежуточные этапы вычислений
    (T, S и график с отмеченными компонентами\n    сильной связности)\n\nПример (4x4):\n
       0111            (Максимальное число вершин Nmax = 20\n       1001                        по размеру поля)  \n       0101 \n       1100""")

def T_matrix(ar, t):

    T = copy(ar)
    E = identity(t, dtype=int)
    T = E + T
    T[T > 0] = 1
    for k in range(t):
      for i in range(t):
        for j in range(t):
                T[i, j] = int(T[i, j]) | (int(T[i, k]) & int(T[k, j]))

    return T

def S_matrix(T, t):
    S = copy(T)
    for i in range(t):
       for j in range(t):
           S[i, j] = int(S[i, j]) & int(S[j, i])

    return S

def S_components(S, t):
    Sc = copy(S)
    cmpts = ''
    l_c=[[]] #[[1, 2, 4], [3, 5]]

    for i in range(t):
       for j in range(t):
           if (Sc[i, j] == 1):
               for rm in range(i, t):
                   Sc[rm, j] = 0
               l_c[i].append(j)
               cmpts += ':::V' + str(j+1)

       l_c.append([])
       cmpts += '\n'

    #cleaning l_c from empty []
    l_c = [i for i in l_c if i]
    while '\n\n' in cmpts:
        cmpts = cmpts.replace('\n\n', '\n')
    text4.insert(1.0, cmpts)

    return l_c

def S_components_graph(S, t, a, c_l, h, ax, ay):
    l_cc = S_components(S, t)
    l_cc_len = len(l_cc)

    R = 20
    angleZero = 0
    angle = 2*round(pi, 8)/t
    x = 0
    y = 0

    plt.xlim(-13,13)
    plt.ylim(-13,13)

    for i in range(len(l_cc)):
        for j in range(len(l_cc[i])):
            x = ax[l_cc[i][j]]
            y = ay[l_cc[i][j]]
            plt.annotate("V" + str(l_cc[i][j]+1), xy=(x,y), xytext=(x-0.55, y-0.3), c=c_l[i], zorder=h+4)
            plt.scatter(x, y, linewidth=14, color='white', zorder=h+2, marker="p")
            plt.scatter(x, y, linewidth=20, color=c_l[i], zorder=h)

    for i in range(t):
        for j in range(t):
            for o in range(len(l_cc)):
                for p in range(len(l_cc[o])):
                    if(i in l_cc[o] and j in l_cc[o]):
                        if (a[i, j] == 1):
                            plt.arrow(round(ax[i], 5), round(ay[i], 5), round(ax[j]-ax[i], 5), round(ay[j]-ay[i], 5),
                                   color = c_l[o], width = 0.00025,
                                   zorder = o, head_length = 1.5,
                                   head_width = 0.5, length_includes_head = True)
                    else:
                        if(a[i, j] == 1):
                             plt.arrow(round(ax[i], 5), round(ay[i], 5), round(ax[j]-ax[i], 5), round(ay[j]-ay[i], 5),
                                color = 'lightgrey', width = 0.00025,
                                zorder = -1, head_length = 1.5,
                                head_width = 0.5, length_includes_head = True)

w = Tk()
w.title("Компоненты сильной связности")
w.resizable(width=False, height=False)
w.geometry('680x670')

x = (w.winfo_screenwidth() - w.winfo_reqwidth()) / 3
y = (w.winfo_screenheight() - w.winfo_reqheight()) / 4
w.wm_geometry("+%d+%d" % (x, y))

#create current c and r
h = 13
k = 2.5

c = 0
r = 0
lbl = Label(w, text="      ",  font=("Century Gothic", 11), fg="darkslategrey")
lbl.grid(column=c, row=r)

c = 1
r = 1
lbl = Label(w, text="  Введите матрицу смежности A: ",  font=("Century Gothic", 11), fg="white", bg='dimgrey')
lbl.grid(column=c, row=r)
text1 = Text(w, width=int(h*k), height=h, bg="white", fg='darkslategrey', font=("Century Gothic", 11))
text1.grid(column=c, row=r+1)
text1.focus()

c = 1
r += 2
lbl = Label(w, text="         ",  font=("Century Gothic", 11), fg="darkslategrey")
lbl.grid(column=c, row=r)
lbl = Label(w, text="  Матрица 1-cторон. связности T:  ",  font=("Century Gothic", 11), fg="white", bg='dimgrey')
lbl.grid(column=c, row=r+1)
text2 = Text(w, width=int(h*k), height=h, bg='white', fg='darkslategrey', font=("Century Gothic", 11))
text2.grid(column=c, row=r+2)

c += 1
r = 1
lbl = Label(w, text="      ",  font=("Century Gothic", 11), fg="darkslategrey")
lbl.grid(column=c, row=r)

c += 1
r = 1
lbl = Label(w, text="  Матрица сильной связности S:     ",  font=("Century Gothic", 11), fg="white", bg='dimgrey')
lbl.grid(column=c, row=r)
text3 = Text(w, width=int(h*k), height=h, bg='white', fg='darkslategrey', font=("Century Gothic", 11))
text3.grid(column=c, row=r+1)

r = 4
lbl = Label(w, text=" Компоненты сильной связности:  ",  font=("Century Gothic", 11), fg="white", bg='dimgrey')
lbl.grid(column=c, row=r)
text4 = Text(w, width=int(h*k), height=h, bg='white', fg='darkslategrey', font=("Century Gothic", 11))
text4.grid(column=c, row=r+1)

c = 5
r = 4
btn = Button(w, text="         >", command=mplt, bg='darkred', fg='white', font=("Furore", 12), highlightthickness = 0, bd = 0)
btn.grid(column=c, row=r)

c = 5
r = 0
lbl = Label(w, text="      ",  font=("Century Gothic", 11), fg="darkslategrey")
lbl.grid(column=c, row=r)

r = 1
btn = Button(w, text="        ? ", command=clicked_info, bg='grey', fg='white', font=("Magneto", 11), highlightthickness = 0, bd = 0)
btn.grid(column=c, row=r)

w.mainloop()
