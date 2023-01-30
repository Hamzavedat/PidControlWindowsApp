import serial
from tkinter import *
from tkinter import messagebox
import threading
import time
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
S = serial.Serial('COM3',9600)
    
P = None
I = None
D = None
hedef = None
Kp = None
Kı = None
Kd = None
H = None
anlık = None
Hiz = ''
Hizf = None
x = list()
y = list()
ciz = False
first = 0.0
x_ = 0.0

def cizim():
        global ciz,x,y,Hizf,canvas,x_,start,first
        
        if ciz:
                if(Hizf != None):
                        last = time.time()
                        if (first != 0.0): 
                                x_ += last - first
                        x.append(x_)
                        y.append(Hizf)
                        first = time.time()
                        Hizf = None
        lines.set_xdata(x)
        lines.set_ydata(y)
        canvas.draw()
        pencere.after(1,cizim)
                        
        



def command():
        msg = "SP" +P.get()+"I"+I.get()+"D"+D.get()+"H"+hedef.get()+"B"
        print(msg)
        S.write(msg.encode('utf-8'))




def speed():
        while True:
                global anlık, Hiz, Hizf
                Hiz = S.readline().decode()
                print(Hiz)
                anlık.config(text=str(Hiz))
                if(Hiz != ''):
                        Hiz2 = Hiz[0:len(Hiz)-2]
                        Hizf = float(Hiz2)



def dur():
        global P, I ,D , H, hedef, Kp, Kı, Kd,ciz
        ciz = False
        #P.delete(0, END)
        #D.delete(0, END)
        #I.delete(0, END)
        #hedef.delete(0, END)



def basla():
        global P, I ,D , H, hedef, Kp, Kı, Kd, ciz
        
        try :
                Kp = P.get()
                Kd = D.get()
                Kı = I.get()
                H  = hedef.get()
                
                print(Kp)
                if(isinstance(float(Kp),float) and isinstance(float(Kı),float) and isinstance(float(Kd),float) and isinstance(float(H),float)):
                        command()        
                        ciz = True
                        print("a")
        except (AttributeError, ValueError):
                messagebox.showwarning(title="Hata", message="YANLIŞ GİRDİNİZ")
                print("a")
        
    
pencere = Tk()
pencere.title("PID")
pencere.geometry("600x600+750+50")
pencere.resizable(FALSE,FALSE)
pencere.state("normal")


yazı = Label(text = "İstenilen Hız",
             fg = "black",
             font = ("Open Sans", "10", "normal"),
             )
yazı.pack()
yazı.place(x = 350, y = 40)

yazı2 = Label(text = "Anlık Hız",
             fg = "black",
             font = ("Open Sans", "10", "normal"),
             )
yazı2.pack()
yazı2.place(x = 470, y = 40)

yazı3 = Label(text = "Kp",
             fg = "black",
             font = ("Open Sans", "10", "normal"),
             )
yazı3.pack()
yazı3.place(x = 50, y = 40)

yazı4 = Label(text = "Kı",
             fg = "black",
             font = ("Open Sans", "10", "normal"),
             )
yazı4.pack()
yazı4.place(x = 150, y = 40)

yazı5 = Label(text = "Kd",
             fg = "black",
             font = ("Open Sans", "10", "normal"),
             )
yazı5.pack()
yazı5.place(x = 250, y = 40)

P = Entry(width = 4)
P.pack()
P.place(x = 48, y = 70)

I = Entry(width = 4)
I.pack()
I.place(x = 146, y = 70)

D = Entry(width = 4)
D.pack()
D.place(x = 247, y = 70)

hedef = Entry(width = 10)
hedef.pack()
hedef.place(x = 355 ,y = 70)

anlık = Label(text = "0.0",
             fg = "black",
             font = ("Open Sans", "10", "normal"),
             )
anlık.pack()
anlık.place(x = 485, y = 70)



start = Button(text = 'Start',
               command = basla,
               bg = "black",
               fg = 'white',
               )
start.pack()
start.place(x = 200, y = 120)

stop = Button(text = 'Stop',
               command = dur,
               bg = "black",
               fg = 'white',
               )
stop.pack()
stop.place(x = 350, y = 120)

thr_speed = threading.Thread(target=speed)
thr_speed.start()

fig = Figure();
ax = fig.add_subplot(111)

ax.set_title("Motor Speed");
ax.set_xlabel("Seconds")
ax.set_ylabel("Speed")
ax.set_xlim(0,60)
ax.set_ylim(0,350)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig,master=pencere)
canvas.get_tk_widget().place(x = 10,y = 150, width = 600, height = 400)
canvas.draw()


pencere.after(1,cizim)
pencere.mainloop()

