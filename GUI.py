from tkinter import *
import serial, time, threading, pickle
import serial.tools.list_ports

tidpunkt=['18:00','18:05','18:10','18:15']
accvol=[0,0,0,0]
vol=[2,2,2,2]
maxtid=[10,10,10,10]
extravol=2
extratid=10
flagga=[1,1,1,1]
tid_=0
time1 = ''

debug=0

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
print("Connected COM ports: " + str(connected))

if len(connected)>0:
    ser=serial.Serial(str(connected[0]))      
        
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

def check():    
    global vol, maxtid, tidpunkt,flagga,gui
    
    for n in range(0,4):
        if tidpunkt[n]==time.strftime('%H:%M') and flagga[n]:
            threading.Thread(vattna(n+1,vol[n],maxtid[n])).start()
            gui.updategui()
            flagga[n]=0
    
        elif flagga[n]==0:
            tid=tidpunkt[n]
            if (int(tid[3:5]))+5 % 60 < int(time.strftime('%M')):
                flagga[n]=1
                    
    threading.Timer(1, check).start()               
                

def vattna(slinga,volym,tid):
    
    global accvol,tid_,debug
    cmd=str(slinga) + ',' + str(volym) + ',' + str(tid) + '\r'
    volume=0
    vol_cur=int(accvol[slinga-1])
  
    gui.b_clr('#BB0000',slinga)



    if not(debug):
    
        ser.write(cmd.encode('ascii'))    
        while True:
            tmp=ser.readline()
            tmp=tmp.decode('ascii')
            tmp=tmp.split(',')
            channel=int(tmp[0])
            volume=int(tmp[1])
            tid_=int(tmp[2])
            accvol[slinga-1]=vol_cur+volume
            gui.updategui()
            time.sleep(.2)
                            
            if channel==-1:         
                break     
    
    else:
        while True:
            tid_+=1
            volume+=1
            accvol[slinga-1]=vol_cur+volume
            gui.updategui()
            if int(tid_)>=int(tid):
                break
            time.sleep(1)
        
    
    save_settings('settinpgs.dat')
    tid_=0
    gui.b_clr('#D9D9D9',slinga)
    gui.updategui()    
    
class MainGUI:
    def __init__(self):
        
        self.gui = Tk()
                    
        fnts=18;bfts=12;lfnts=12;ewdt=5;bhgt=2;bwdt=10;timx=110;timlx=10;timy=5
        row0=15;row1=40;row2=80;row3=150;row4=220;row5=290;row7=350
        col0=10;col1=90;col2=190;col3=290;col4=390;col6=530;ecl1=500;ecl2=600;colb1=10;colb2=140;colb3=270
            
        Label(self.gui, text="Aktuell tid: ",font=("", lfnts)).place(x=timlx,y=timy)
        self.clock=Label(self.gui,font=("", lfnts))
        self.clock.place(x=timx,y=timy)
        
        self.ent_vattnar=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts+7),bg='#BDBDBD')
        self.ent_vattnar.place(x=col6,y=row7)
        
        Button(self.gui, text="Applicera", command = self.apply,  height = bhgt, width = bwdt,font=("", bfts)).place(x=colb1, y=row7)
        Button(self.gui, text="Ångra", command = self.cancel,  height = bhgt, width = bwdt,font=("", bfts)).place(x=colb3, y=row7)
        Button(self.gui, text="Reset", command = self.reset,  height = bhgt, width = bwdt,font=("", bfts)).place(x=colb2, y=row7)

        self.Bv1=Button(self.gui, text="Vattna 1",
                command= lambda: [threading.Thread(target=vattna,args=[1,self.ent_extravol.get(),self.ent_extramtd.get()]).start()],
                   height = bhgt, width = bwdt,font=("", bfts))
        self.Bv1.place(x=col6, y=row2)

        self.Bv2=Button(self.gui, text="Vattna 2",
                command= lambda:[threading.Thread(target=vattna,args=[2,self.ent_extravol.get(),self.ent_extramtd.get()]).start()],
                  height = bhgt, width = bwdt,font=("", bfts))
        self.Bv2.place(x=col6, y=row3)
       
        self.Bv3=Button(self.gui, text="Vattna 3",
                command= lambda:[threading.Thread(target=vattna,args=[3,self.ent_extravol.get(),self.ent_extramtd.get()]).start()],
                  height = bhgt, width = bwdt,font=("", bfts))
        self.Bv3.place(x=col6, y=row4)
        
        self.Bv4=Button(self.gui, text="Vattna 4",
                command= lambda:[threading.Thread(target=vattna,args=[4,self.ent_extravol.get(),self.ent_extramtd.get()]).start()],
                  height = bhgt, width = bwdt,font=("", bfts))
        self.Bv4.place(x=col6, y=row5)

        Label(self.gui,text="Volym dl",font=("", lfnts)).place(x=col1,y=row1)
        Label(self.gui,text="Maxtid s",font=("", lfnts)).place(x=col2,y=row1)
        Label(self.gui,text="Tid hh:mm",font=("", lfnts)).place(x=col3,y=row1)
        Label(self.gui,text="Tol vol dl",font=("", lfnts)).place(x=col4,y=row1)
        Label(self.gui,text="Volym dl",font=("", lfnts)).place(x=ecl1,y=row0)
        Label(self.gui,text="Maxtid s",font=("", lfnts)).place(x=ecl2,y=row0)

        self.ent_extravol=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_extravol.place(x=ecl1,y=row1)
        self.ent_extramtd=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_extramtd.place(x=ecl2,y=row1)

        Label(self.gui, text="Slinga 1",font=("", lfnts)).place(x=col0,y=row2)
        self.ent_vol1=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_vol1.place(x=col1,y=row2)
        self.ent_mtd1=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_mtd1.place(x=col2,y=row2)
        self.ent_tid1=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_tid1.place(x=col3,y=row2)
        self.ent_avl1=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
        self.ent_avl1.place(x=col4,y=row2)

        Label(self.gui, text="Slinga 2",font=("", lfnts)).place(x=col0,y=row3)
        self.ent_vol2=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_vol2.place(x=col1,y=row3)
        self.ent_mtd2=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_mtd2.place(x=col2,y=row3)
        self.ent_tid2=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_tid2.place(x=col3,y=row3)
        self.ent_avl2=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
        self.ent_avl2.place(x=col4,y=row3)

        Label(self.gui, text="Slinga 3",font=("", lfnts)).place(x=col0,y=row4)
        self.ent_vol3=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_vol3.place(x=col1,y=row4)
        self.ent_mtd3=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_mtd3.place(x=col2,y=row4)
        self.ent_tid3=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_tid3.place(x=col3,y=row4)
        self.ent_avl3=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
        self.ent_avl3.place(x=col4,y=row4)

        Label(self.gui, text="Slinga 4",font=("", lfnts)).place(x=col0,y=row5)
        self.ent_vol4=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_vol4.place(x=col1,y=row5)
        self.ent_mtd4=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_mtd4.place(x=col2,y=row5)
        self.ent_tid4=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts))
        self.ent_tid4.place(x=col3,y=row5)
        self.ent_avl4=Entry(self.gui,width=ewdt,justify=RIGHT,font=("", fnts),bg='#EDEDED')
        self.ent_avl4.place(x=col4,y=row5)

        for b in [self.ent_extravol, self.ent_extramtd, self.ent_tid1, self.ent_vol1, self.ent_mtd1, self.ent_tid2, self.ent_vol2, self.ent_mtd2,
            self.ent_tid3, self.ent_vol3, self.ent_mtd3, self.ent_tid4, self.ent_vol4, self.ent_mtd4]:
            b.bind("<Button-1>", lambda e: self.keyboard())
        
        self.gui.geometry("720x480+0+0")
        #self.gui.attributes("-fullscreen", True)
        
        self.keyboard()

    def tick(self):
        global time1

        time2 = time.strftime('%H:%M:%S')
        if time2 != time1:
            time1 = time2
            self.clock.config(text=time2)
        self.clock.after(200, self.tick)
    
    def updategui(self):
        global accvol,vol,maxtid,tidpunkt,extravol,extratid,tid_

        for i,a,v,m,t in zip(range(0,5), [self.ent_avl1,self.ent_avl2,self.ent_avl3,self.ent_avl4],
                             [self.ent_vol1,self.ent_vol2,self.ent_vol3,self.ent_vol4],
                         [self.ent_mtd1,self.ent_mtd2,self.ent_mtd3,self.ent_mtd4],
                             [self.ent_tid1,self.ent_tid2,self.ent_tid3,self.ent_tid4]):

            a.delete(0,END)
            a.insert(0,accvol[i])   
            v.delete(0,END)
            v.insert(0,vol[i])        
            m.delete(0,END)
            m.insert(0,maxtid[i])
            t.delete(0,END)
            t.insert(0,tidpunkt[i])
            
        self.ent_extravol.delete(0,END)
        self.ent_extravol.insert(0,extravol)
        self.ent_extramtd.delete(0,END)
        self.ent_extramtd.insert(0,extratid)
        
        self.ent_vattnar.delete(0,END)
        self.ent_vattnar.insert(0,tid_)
        
    def keyboard(self):
        buttons = ['0','1','2','3','4','5','6','7','8','9',':','<']
        varRow = 410
        varColumn = 5

        for button in buttons:
            command = lambda x=button: self.select(x)
            Button(self.gui,text= button,width=2,height=2,command=command,font=("",18)).place(x=varColumn,y=varRow)
            varColumn +=59

    def select(self,value):

        focus=self.gui.focus_get()
        print(focus)
        
        
        if (str(focus)=='.!entry7' or str(focus)=='.!entry11' or str(focus)=='.!entry15' or str(focus)=='.!entry19'):
            return
        
        if value == "<" :
            focus.delete(0,END)
        else :
            focus.insert(END,value)
        
    def apply(self):
        global accvol,vol,maxtid,tidpunkt,extravol,extratid
    
        save_settings('temp.dat')    
    
        for ent in [self.ent_tid1, self.ent_tid2, self.ent_tid3, self.ent_tid4]:    
            if len(ent.get())!=5:
                self.reset()        
                return       
            
            elif (int(ent.get()[0:2])>23 or int(ent.get()[0:2])<00 or
                int(ent.get()[3:5])>59 or int(ent.get()[3:5])<00) :
                self.reset()        
                return    
    
        for i,a,v,m,t in zip(range(0,5), [self.ent_avl1,self.ent_avl2,self.ent_avl3,self.ent_avl4],
                             [self.ent_vol1,self.ent_vol2,self.ent_vol3,self.ent_vol4],
                         [self.ent_mtd1,self.ent_mtd2,self.ent_mtd3,self.ent_mtd4],
                             [self.ent_tid1,self.ent_tid2,self.ent_tid3,self.ent_tid4]):                
            accvol[i]=int(a.get())
            vol[i]=(v.get())
            maxtid[i]=(m.get())
            tidpunkt[i]=(t.get())
        
        extravol=self.ent_extravol.get()
        extratid=self.ent_extramtd.get()
    
        save_settings('settings.dat')
        self.updategui()
    
    def b_clr(self,colr,slinga):
        
        if slinga==1:
            self.Bv1.configure(bg=colr)
        elif slinga==2:
            self.Bv2.configure(bg=colr)
        elif slinga==3:
            self.Bv3.configure(bg=colr)
        elif slinga==4:
            self.Bv4.configure(bg=colr)

        
    def cancel(self):    
        load_settings('temp.dat')
        save_settings('settings.dat')
        self.updategui()
          
    def reset(self):
        global accvol
    
        accvol=[0,0,0,0]    
        save_settings('settings.dat')
        self.updategui()
        
    def run(self):
        self.gui.mainloop()

load_settings('settings.dat')

gui=MainGUI()
gui.tick()
gui.updategui()
check()
gui.run()