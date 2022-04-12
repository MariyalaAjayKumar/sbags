import requests
import json
from tkinter import *
from tkinter import messagebox,Menu
import sqlite3

pycrypto=Tk()
pycrypto.title("my crypto portfolio")
pycrypto.iconbitmap("favicon.ico")
con=sqlite3.connect("coin.db")
cursorobj=con.cursor()
cursorobj.execute("CREATE TABLE IF NOT EXISTS coiN(id INTEGER PRIMARY KEY,symbol TEXT,amount INTEGER,price REAL)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():  #destroy our window ,it will clear the all the window when will call a function for to add coin or delete coin it will clear window and print freshly
        cell.destroy()   
    app_header()
    my_portfolio()
    app_nav()

def app_nav():
    def clear_all():
        cursorobj.execute("DELETE FROM coin")
        con.commit()
    
    def close_app():
        pycrypto.destroy()
        
    menu=Menu(pycrypto)
    file_item=Menu(menu)
    file_item.add_command(label="clear portfolio",command=clear_all)
    file_item.add_command(label="Close App",command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)



def my_portfolio():
    api_request=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=82180813-12f0-4f70-810c-31af4e0762a7")
    api=json.loads(api_request.content)
    
    cursorobj.execute("SELECT * FROM coin")
    coins=cursorobj.fetchall()
    
    def font_color(amount):
        if amount>=0:
            return "green"
        else:
            return "red"
    
    def insert_coin():
        cursorobj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()
        messagebox.showinfo("portfolio notification","coin add to portfolio successfully")
        reset()
    
    def update_coin():
        cursorobj.execute("UPDATE coin SET symbol=?,price=?,amount=? WHERE id=?",(symbol_update.get(),price_update.get(),amount_update.get(),portid_update.get()))
        con.commit()
        messagebox.showinfo("portfolio notification","coin updated to portfolio successfully")
        reset()

    def delete_coin():
        cursorobj.execute("DELETE FROM coin WHERE id=?",(portid_delete.get()))
        con.commit()
        messagebox.showinfo("portfolio notification","coin deleted from portfolio successfully")
        reset()



    total_pl=0
    coin_row=1
    total_current_value=0
    total_paid_value=0

    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"]==coin[1]:
                total_paid=coin[2]*coin[3]
                current_value=coin[2]*api["data"][i]["quote"]["USD"]["price"]
                pl_percoin=api["data"][i]["quote"]["USD"]["price"]-coin[3]
                total_pl_coin=pl_percoin*coin[2]
                total_pl+=total_pl_coin
                total_current_value+=current_value
                total_paid_value+=total_paid

        

                portfolio_id=Label(pycrypto,text=coin[0],bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                portfolio_id.grid(row=coin_row,column=0,sticky=N+S+E+W)
                name=Label(pycrypto,text=api["data"][i]["symbol"],bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                name.grid(row=coin_row,column=1,sticky=N+S+E+W)
                price=Label(pycrypto,text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                price.grid(row=coin_row,column=2,sticky=N+S+E+W)
                no_coins=Label(pycrypto,text=coin[2],bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                no_coins.grid(row=coin_row,column=3,sticky=N+S+E+W)
                amount_paid=Label(pycrypto,text="${0:.2f}".format(total_paid),bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                amount_paid.grid(row=coin_row,column=4,sticky=N+S+E+W)
                current_value=Label(pycrypto,text="${0:.2f}".format(current_value),bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                current_value.grid(row=coin_row,column=5,sticky=N+S+E+W)
                PL_coin=Label(pycrypto,text="${0:.2f}".format(pl_percoin),bg="#F3F4F5",fg=font_color(float("{0:.2f}".format(pl_percoin))),font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                PL_coin.grid(row=coin_row,column=6,sticky=N+S+E+W)
                totalPL=Label(pycrypto,text="${0:.2f}".format(total_pl_coin),bg="#F3F4F5",fg=font_color(float("{0:.2f}".format(total_pl_coin))),font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
                totalPL.grid(row=coin_row,column=7,sticky=N+S+E+W)
                coin_row+=1 

    #insert add coin
    symbol_txt=Entry(pycrypto,borderwidth=2,relief="groove")
    symbol_txt.grid(row=coin_row+1,column=1)
    price_txt=Entry(pycrypto,borderwidth=2,relief="groove")
    price_txt.grid(row=coin_row+1,column=2)
    amount_txt=Entry(pycrypto,borderwidth=2,relief="groove")
    amount_txt.grid(row=coin_row+1,column=3)
    add_coin=Button(pycrypto,text="ADD COIN",bg="#142E54",fg="white",command=insert_coin,font="Lato 12 bold",borderwidth=2,relief="groove",padx="5",pady="5")
    add_coin.grid(row=coin_row+1,column=4,sticky=N+S+E+W)

    #update coin
    portid_update=Entry(pycrypto,borderwidth=2,relief="groove")
    portid_update.grid(row=coin_row+2,column=0)
    symbol_update=Entry(pycrypto,borderwidth=2,relief="groove")
    symbol_update.grid(row=coin_row+2,column=1)
    price_update=Entry(pycrypto,borderwidth=2,relief="groove")
    price_update.grid(row=coin_row+2,column=2)
    amount_update=Entry(pycrypto,borderwidth=2,relief="groove")
    amount_update.grid(row=coin_row+2,column=3)
    update_coin_txt=Button(pycrypto,text="UPDATE",bg="#142E54",fg="white",command=update_coin,font="Lato 12 bold",borderwidth=2,relief="groove",padx="5",pady="5")
    update_coin_txt.grid(row=coin_row+2,column=4,sticky=N+S+E+W)

    #DELETE COIN
    portid_delete=Entry(pycrypto,borderwidth=2,relief="groove")
    portid_delete.grid(row=coin_row+3,column=0)
    delete_coin_txt=Button(pycrypto,text="DELETE",bg="#142E54",fg="white",command=delete_coin,font="Lato 12 bold",borderwidth=2,relief="groove",padx="5",pady="5")
    delete_coin_txt.grid(row=coin_row+3,column=4,sticky=N+S+E+W)





    total_pl_buy=Label(pycrypto,text="${0:.2f}".format(total_pl),bg="#F3F4F5",fg=font_color(float("{0:.2f}".format(total_pl))),font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
    total_pl_buy.grid(row=coin_row,column=7,sticky=N+S+E+W)
    total_pv=Label(pycrypto,text="${0:.2f}".format(total_paid_value),bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
    total_pv.grid(row=coin_row,column=4,sticky=N+S+E+W)
    total_cv=Label(pycrypto,text="${0:.2f}".format(total_current_value),bg="#F3F4F5",fg="black",font="Lato 12",borderwidth=2,relief="groove",padx="5",pady="5")
    total_cv.grid(row=coin_row,column=5,sticky=N+S+E+W)
    api=" "
    Refresh=Button(pycrypto,text="REFRESH",bg="#142E54",fg="white",command=reset,font="Lato 12 bold",borderwidth=2,relief="groove",padx="5",pady="5")
    Refresh.grid(row=coin_row+1,column=7,sticky=N+S+E+W)
    
    

def app_header():
    portfolio_id=Label(pycrypto,text="portfolio ID",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    portfolio_id.grid(row=0,column=0,sticky=N+S+E+W)
    name=Label(pycrypto,text="Bitcoin",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    name.grid(row=0,column=1,sticky=N+S+E+W)
    price=Label(pycrypto,text="price",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    price.grid(row=0,column=2,sticky=N+S+E+W)
    no_coins=Label(pycrypto,text="coins owned",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    no_coins.grid(row=0,column=3,sticky=N+S+E+W)
    amount_paid=Label(pycrypto,text="total amount paid",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    amount_paid.grid(row=0,column=4,sticky=N+S+E+W)
    current_value=Label(pycrypto,text="current value",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    current_value.grid(row=0,column=5,sticky=N+S+E+W)
    PL_coin=Label(pycrypto,text="P/L per coin",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    PL_coin.grid(row=0,column=6,sticky=N+S+E+W)
    totalPL=Label(pycrypto,text="total P/L our coin ",bg="#142E54",fg="white",font="Lato 12 bold",padx="5",pady="5",borderwidth=2,relief="groove")
    totalPL.grid(row=0,column=7,sticky=N+S+E+W)

app_nav()#this app_nav function
app_header() #this is app_header function
my_portfolio()#this is our main function
pycrypto.mainloop()
print("completed program")
cursorobj.close()
con.close()