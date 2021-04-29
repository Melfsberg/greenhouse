from tkinter import *
import serial, time
import serial.tools.list_ports
import pickle

tidpunkt=['18:00','18:05','18:10','18:15']
accvol=[0,0,0,0]
vol=[2,2,2,2]
maxtid=[10,10,10,10]
extravol=2
extratid=10
flagga=[1,1,1,1]

buttons = ['0','1','2','3','4','5','6','7','8','9',':','<']
time1 = ''

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
print("Connected COM ports: " + str(connected))

if len(connected)>0:
    ser=serial.Serial(str(connected[0]))

gui= Tk()

def keyboard():
    
    varRow = 410
    varColumn = 0

    for button in buttons:
        command = lambda x=button: select(x)
        Button(gui,text= button,width=3,height=2,command=command,font=("",18)).place(x=varColumn,y=varRow)
        varColumn +=58

def select(value):

    focus=gui.focus_get()
    
    if (str(focus)=='.!entry6' or str(focus)=='.!entry10' or str(focus)=='.!entry14' or str(focus)=='.!entry18'):
        return

    if value == "<" :
        focus.delete(0,END)
    else :
        focus.insert(END,value)        

def save_settings(file_name):
    global accvol,vol,maxtid,tidpunkt,extravol,extratid
    
    with open(file_name, 'wb') as file:
        pickle.dump([accvol,vol,maxtid,tidpunkt,extravol,extratid], file)    


def load_settings(file_name):
    global accvol,vol,maxtid,tidpunkt,extravol,extratid
    
    try:
        with open(file_name, 'rb') as file:
            [accvol,vol,maxtid,tidpunkt,extravol,extratid]=pickle.load(file)
    except:
        print('no file')
        
def apply():
    global accvol,vol,maxtid,tidpunkt,extravol,extratid
    
    save_settings('temp.dat')    
    
    for ent in [ent_tid1, ent_tid2, ent_tid3, ent_tid4]:    
        if len(ent.get())!=5:
            reset()        
            return        
        elif (int(ent.get()[0:2])>23 or int(ent.get()[0:2])<00 or
                int(ent.get()[3:5])>59 or int(ent.get()[3:5])<00) :
            reset()        
            return
    
    
    for i,a,v,m,t in zip(range(0,5), [ent_avl1,ent_avl2,ent_avl3,ent_avl4],[ent_vol1,ent_vol2,ent_vol3,ent_vol4],
                         [ent_mtd1,ent_mtd2,ent_mtd3,ent_mtd4],[ent_tid1,ent_tid2,ent_tid3,ent_tid4]):
                
        accvol[i]=int(a.get())
        vol[i]=(v.get())
        maxtid[i]=(m.get())
        tidpunkt[i]=(t.get())
        
    extravol=ent_extravol.get()
    extratid=ent_extramtd.get()
    
    save_settings('settings.dat')
    updategui()
    
def cancel():    
    load_settings('temp.dat')
    save_settings('settings.dat')
    updategui()

def reset():
    global accvol
    
    accvol=[0,0,0,0]    
    save_settings('settings.dat')
    updategui()

def updategui():
    global accvol,vol,maxtid,tidpunkt,extravol,extratid
   
    for i,a,v,m,t in zip(range(0,5), [ent_avl1,ent_avl2,ent_avl3,ent_avl4],[ent_vol1,ent_vol2,ent_vol3,ent_vol4],
                         [ent_mtd1,ent_mtd2,ent_mtd3,ent_mtd4],[ent_tid1,ent_tid2,ent_tid3,ent_tid4]):
                
        a.delete(0,END)
        a.insert(0,accvol[i])   
        v.delete(0,END)
        v.insert(0,vol[i])        
        m.delete(0,END)
        m.insert(0,maxtid[i])
        t.delete(0,END)
        t.insert(0,tidpunkt[i])

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
    
    if 'ser' in globals():
        ser.write(cmd.encode('ascii'))
    
        while True:
            tmp=ser.readline()
            tmp=tmp.decode('ascii')
            tmp=tmp.split(',')
            channel=int(tmp[0])
            volume=int(tmp[1])
            #tid=int(tmp[2])
                
            if channel==-1:         
                break
      
        accvol[slinga-1]=accvol[slinga-1]+(volume)
        updategui()

    else:
        time.sleep(2)
        accvol[slinga-1]=accvol[slinga-1]+2
        updategui()
        
    save_settings('settings.dat')
    
def on_closing():    
    gui.destroy()
    exit()

# GUI Design

fnts=13;bfts=9;ewdt=6;bhgt=2;bwdt=10;timx=100;timlx=10;timy=5
row0=15;row1=40;row2=80;row3=150;row4=220;row5=290;row6=360;row7=350;row8=420
col0=10;col1=90;col2=190;col3=290;col4=390;col5=490;col6=530;ecl1=500;ecl2=600;colb1=10;colb2=140;colb3=270
    
Label(gui, text="Aktuell tid: ",font=("", fnts)).place(x=timlx,y=timy)
clock=Label(gui,font=("", fnts))
clock.place(x=timx,y=timy)

Button(gui, text="Applicera", command = apply,  height = bhgt, width = bwdt,font=("", bfts)).place(x=colb1, y=row7)
Button(gui, text="Ångra", command = cancel,  height = bhgt, width = bwdt,font=("", bfts)).place(x=colb3, y=row7)
Button(gui, text="Reset", command = reset,  height = bhgt, width = bwdt,font=("", bfts)).place(x=colb2, y=row7)

Button(gui, text="Vattna 1",command= lambda: vattna(1,ent_extravol.get(),ent_extramtd.get()),  height = bhgt, width = bwdt,font=("", bfts)).place(x=col6, y=row2)
Button(gui, text="Vattna 2", command= lambda: vattna(2,ent_extravol.get(),ent_extramtd.get()),  height = bhgt, width = bwdt,font=("", bfts)).place(x=col6, y=row3)
Button(gui, text="Vattna 3", command= lambda: vattna(3,ent_extravol.get(),ent_extramtd.get()),  height = bhgt, width = bwdt,font=("", bfts)).place(x=col6, y=row4)
Button(gui, text="Vattna 4", command= lambda: vattna(4,ent_extravol.get(),ent_extramtd.get()),  height = bhgt, width = bwdt,font=("", bfts)).place(x=col6, y=row5)

Label(gui,text="Volym dl",font=("", fnts)).place(x=col1,y=row1)
Label(gui,text="Maxtid s",font=("", fnts)).place(x=col2,y=row1)
Label(gui,text="Tid hh:mm",font=("", fnts)).place(x=col3,y=row1)
Label(gui,text="Acc vol dl",font=("", fnts)).place(x=col4,y=row1)
Label(gui,text="Volym dl",font=("", fnts)).place(x=ecl1,y=row0)
Label(gui,text="Maxtid s",font=("", fnts)).place(x=ecl2,y=row0)

ent_extravol=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_extravol.place(x=ecl1,y=row1)
ent_extramtd=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_extramtd.place(x=ecl2,y=row1)

Label(gui, text="Slinga 1",font=("", fnts)).place(x=col0,y=row2)
ent_vol1=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_vol1.place(x=col1,y=row2)
ent_mtd1=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_mtd1.place(x=col2,y=row2)
ent_tid1=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_tid1.place(x=col3,y=row2)
ent_avl1=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
ent_avl1.place(x=col4,y=row2)

Label(gui, text="Slinga 2",font=("", fnts)).place(x=col0,y=row3)
ent_vol2=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_vol2.place(x=col1,y=row3)
ent_mtd2=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_mtd2.place(x=col2,y=row3)
ent_tid2=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_tid2.place(x=col3,y=row3)
ent_avl2=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
ent_avl2.place(x=col4,y=row3)

Label(gui, text="Slinga 3",font=("", fnts)).place(x=col0,y=row4)
ent_vol3=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_vol3.place(x=col1,y=row4)
ent_mtd3=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_mtd3.place(x=col2,y=row4)
ent_tid3=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_tid3.place(x=col3,y=row4)
ent_avl3=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
ent_avl3.place(x=col4,y=row4)

Label(gui, text="Slinga 4",font=("", fnts)).place(x=col0,y=row5)
ent_vol4=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_vol4.place(x=col1,y=row5)
ent_mtd4=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_mtd4.place(x=col2,y=row5)
ent_tid4=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts))
ent_tid4.place(x=col3,y=row5)
ent_avl4=Entry(gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
ent_avl4.place(x=col4,y=row5)

for b in [ent_extravol, ent_extramtd, ent_tid1, ent_vol1, ent_mtd1, ent_tid2, ent_vol2, ent_mtd2,
    ent_tid3, ent_vol3, ent_mtd3, ent_tid4, ent_vol4, ent_mtd4]:
    b.bind("<Button-1>", lambda e: keyboard())

gui.geometry("680x480+0+0")
gui.protocol("WM_DELETE_WINDOW", on_closing)
#gui.attributes("-fullscreen", True)

tick()
load_settings('settings.dat')
updategui()
keyboard()

check()
gui.mainloop()
