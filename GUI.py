from tkinter import *
import serial, time
import serial.tools.list_ports

time1 = ''
accvol=[0,0,0,0]
vol=[2,2,2,2]
maxtid=[10,10,10,10]
flagga=[1,1,1,1]

extravol=5
extratid=5

tidpunkt=['18:00','18:05','18:10','18:15']

buttons = ['0','1','2','3','4','5','6','7','8','9',':','<']

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
#print("Connected COM ports: " + str(connected))

ser=serial.Serial(str(connected[0]))
gui= Tk()

def HosoPop():
    
    varRow = 410
    varColumn = 0

    for button in buttons:
        command = lambda x=button: select(x)
        Button(gui,text= button,width=3,height=2,command=command,font=("",18)).place(x=varColumn,y=varRow)
        varColumn +=58

def select(value):


    if value == "<" :
        gui.focus_displayof().delete(0,END)

    else :
        gui.focus_displayof().insert(END,value)
        
def apply():
    global accvol,vol,maxtid,tidpunkt,extravol,extratid
    
    accvol[0]=int(ent_avl1.get())
    accvol[1]=int(ent_avl2.get())
    accvol[2]=int(ent_avl3.get())
    accvol[3]=int(ent_avl4.get())
 
    vol[0]=ent_vol1.get()
    vol[1]=ent_vol2.get()
    vol[2]=ent_vol3.get()
    vol[3]=ent_vol4.get()
    
    maxtid[0]=ent_mtd1.get()
    maxtid[1]=ent_mtd2.get()
    maxtid[2]=ent_mtd3.get()
    maxtid[3]=ent_mtd4.get()
    
    tidpunkt[0]=ent_tid1.get()
    tidpunkt[1]=ent_tid2.get()
    tidpunkt[2]=ent_tid3.get()
    tidpunkt[3]=ent_tid4.get()
   
    extravol=ent_extravol.get()
    extratid=ent_extramtd.get()
     

    updategui()

    
def cancel():
    updategui()

def reset():
    global accvol,vol,maxtid,extravol,extratid,tidpunkt
    
    extravol=5
    extratid=5
    accvol=[0,0,0,0]
    vol=[2,2,2,2]
    maxtid=[10,10,10,10]
    tidpunkt=['18:00','18:05','18:10','18:15']
        
    updategui()

def updategui():
    global accvol,vol,maxtid,tidpunkt,extravol,extratid

    ent_avl1.delete(0,END)
    ent_avl1.insert(0,accvol[0])
    ent_avl2.delete(0,END)
    ent_avl2.insert(0,accvol[1])
    ent_avl3.delete(0,END)
    ent_avl3.insert(0,accvol[2])
    ent_avl4.delete(0,END)
    ent_avl4.insert(0,accvol[3])

    ent_vol1.delete(0,END)
    ent_vol1.insert(0,vol[0])
    ent_vol2.delete(0,END)
    ent_vol2.insert(0,vol[1])
    ent_vol3.delete(0,END)
    ent_vol3.insert(0,vol[2])
    ent_vol4.delete(0,END)
    ent_vol4.insert(0,vol[3])
    
    ent_mtd1.delete(0,END)
    ent_mtd1.insert(0,maxtid[0])
    ent_mtd2.delete(0,END)
    ent_mtd2.insert(0,maxtid[1])
    ent_mtd3.delete(0,END)
    ent_mtd3.insert(0,maxtid[2])
    ent_mtd4.delete(0,END)
    ent_mtd4.insert(0,maxtid[3])
    
    ent_tid1.delete(0,END)
    ent_tid1.insert(0,tidpunkt[0])
    ent_tid2.delete(0,END)
    ent_tid2.insert(0,tidpunkt[1])
    ent_tid3.delete(0,END)
    ent_tid3.insert(0,tidpunkt[2])
    ent_tid4.delete(0,END)
    ent_tid4.insert(0,tidpunkt[3])
    
    ent_extravol.delete(0,END)
    ent_extravol.insert(0,extravol)
    ent_extramtd.delete(0,END)
    ent_extramtd.insert(0,extratid)


def tick():
    global time1

    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    clock.after(200, tick)

def check():
    global vol, maxtid, tidpunkt,flagga
    
    for n in range(0,4):

        if tidpunkt[n]==time.strftime('%H:%M') and flagga[n]:
            vattna(n+1,vol[n],maxtid[n])
            flagga[n]=0
    
        elif flagga[n]==0:
            tid=tidpunkt[n]
            if (int(tid[3:5]))+5 % 60 < int(time.strftime('%M')):
                flagga[n]=1
                
    clock.after(1000, check)


def vattna(slinga,volym,tid):
    
    global accvol
    cmd=str(slinga) + ',' + str(volym) + ',' + str(tid) + '\r'
    ser.write(cmd.encode('ascii'))
    
    while True:
        tmp=ser.readline()
        tmp=tmp.decode('ascii')
        tmp=tmp.split(',')
        channel=int(tmp[0])
        volume=int(tmp[1])
        tid=int(tmp[2])
                
        if channel==-1:         
            break
      
    accvol[slinga-1]=accvol[slinga-1]+(volume)
    updategui()


# GUI Design

fnts=13
row0=15
row1=40
row2=80
row3=150
row4=220
row5=290
row6=360
row7=350
row8=420
col0=10
col1=90
col2=190
col3=290
col4=390
col5=490
col6=530
    
cl_lbl=Label(gui, text="Aktuell tid: ",font=("", fnts))
cl_lbl.place(x=10,y=5)
clock=Label(gui,font=("", fnts))
clock.place(x=100,y=5)

btn_apply=Button(gui, text="Applicera", command = apply,  height = 2, width = 10,font=("", fnts-4))
btn_apply.place(x=col0, y=row7)
btn_apply=Button(gui, text="Ångra", command = cancel,  height = 2, width = 10,font=("", fnts-4))
btn_apply.place(x=col2, y=row7)
btn_apply=Button(gui, text="Reset", command = reset,  height = 2, width = 10,font=("", fnts-4))
btn_apply.place(x=col4, y=row7)

btn_v1=Button(gui, text="Vattna 1",command= lambda: vattna(1,ent_extravol.get(),ent_extramtd.get()),  height = 2, width = 9,font=("", fnts-4))
btn_v1.place(x=col6, y=row2+20)
btn_v1=Button(gui, text="Vattna 2", command= lambda: vattna(2,ent_extravol.get(),ent_extramtd.get()),  height = 2, width = 9,font=("", fnts-4))
btn_v1.place(x=col6, y=row3+20)
btn_v1=Button(gui, text="Vattna 3", command= lambda: vattna(3,ent_extravol.get(),ent_extramtd.get()),  height = 2, width = 9,font=("", fnts-4))
btn_v1.place(x=col6, y=row4+20)
btn_v1=Button(gui, text="Vattna 4", command= lambda: vattna(4,ent_extravol.get(),ent_extramtd.get()),  height = 2, width = 9,font=("", fnts-4))
btn_v1.place(x=col6, y=row5+20)

lbl_vol=Label(gui,text="Volym l",font=("", fnts))
lbl_vol.place(x=col1,y=row1)
lbl_vol=Label(gui,text="Maxtid s",font=("", fnts))
lbl_vol.place(x=col2,y=row1)
lbl_vol=Label(gui,text="Tid hh:mm",font=("", fnts))
lbl_vol.place(x=col3,y=row1)
lbl_avl=Label(gui,text="Acc vol dl",font=("", fnts))
lbl_avl.place(x=col4,y=row1)

lbl_vol=Label(gui,text="Volym dl",font=("", fnts))
lbl_vol.place(x=500,y=row0)
lbl_vol=Label(gui,text="Maxtid s",font=("", fnts))
lbl_vol.place(x=600,y=row0)
ent_extravol=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_extravol.place(x=500,y=row1)
ent_extramtd=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_extramtd.place(x=600,y=row1)

lbl_s1=Label(gui, text="Slinga 1",font=("", fnts))
lbl_s1.place(x=col0,y=row2)
ent_vol1=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_vol1.place(x=col1,y=row2)
ent_mtd1=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_mtd1.place(x=col2,y=row2)
ent_tid1=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_tid1.place(x=col3,y=row2)
ent_avl1=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_avl1.place(x=col4,y=row2)

lbl_s2=Label(gui, text="Slinga 2",font=("", fnts))
lbl_s2.place(x=col0,y=row3)
ent_vol2=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_vol2.place(x=col1,y=row3)
ent_mtd2=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_mtd2.place(x=col2,y=row3)
ent_tid2=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_tid2.place(x=col3,y=row3)
ent_avl2=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_avl2.place(x=col4,y=row3)

lbl_s3=Label(gui, text="Slinga 3",font=("", fnts))
lbl_s3.place(x=col0,y=row4)
ent_vol3=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_vol3.place(x=col1,y=row4)
ent_mtd3=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_mtd3.place(x=col2,y=row4)
ent_tid3=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_tid3.place(x=col3,y=row4)
ent_avl3=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_avl3.place(x=col4,y=row4)

lbl_s4=Label(gui, text="Slinga 4",font=("", fnts))
lbl_s4.place(x=col0,y=row5)
ent_vol4=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_vol4.place(x=col1,y=row5)
ent_mtd4=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_mtd4.place(x=col2,y=row5)
ent_tid4=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_tid4.place(x=col3,y=row5)
ent_avl4=Entry(gui,width=6,justify=RIGHT,font=("", fnts))
ent_avl4.place(x=col4,y=row5)

for b in [ent_extravol, ent_extramtd, ent_tid1, ent_vol1, ent_mtd1, ent_tid2, ent_vol2, ent_mtd2,
           ent_tid3, ent_vol3, ent_mtd3, ent_tid4, ent_vol4, ent_mtd4]:
    b.bind("<Button-1>", lambda e: HosoPop())

gui.geometry("680x480+0+0")

#

updategui()

#gui.attributes("-fullscreen", True)

tick()
check()
gui.mainloop()
