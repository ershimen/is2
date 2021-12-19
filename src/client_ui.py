# Grupo 35
# Cliente de la aplicación de taxis
from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import socket, pickle, time
from hashlib import sha256
from datetime import datetime, date

# Window size
width = 900
height = 800

# Login canvas bg color
bg_color = "#dbdbdb"

# Default buffer size
BUFFER_SIZE = 1024

# Server address
SERVER_IP = "localhost"
SERVER_PORT = 1234

# Send msg to SERVER_IP:SERVER_PORT
def send_msg(msg, size=BUFFER_SIZE):
    result = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(pickle.dumps(msg))
        result = pickle.loads(s.recv(size))
        s.close()
    except ConnectionRefusedError:
        print("No se puede conectar con el servidor.")
        messagebox.showerror("Error", "Error conectando con el servidor.")
    finally:
        return result

# Format string to fixed length and append "..." if necessary
def just(s, l):
    if len(s) < l:
        return s
    return s[0:l-3]+"..."

def main():
    # root window
    root = Tk()
    root.title("AppTaxi")
    root.geometry("900x800")
    root.resizable(False, False)

    # App title label
    Label(root, text="App Taxi", font="Calibri 27 bold").place(x=380, y=60)

    # login canvas
    canvas_login = Canvas(root, width=400, height=300, bg=bg_color,
        highlightthickness=2, highlightbackground="black")
    canvas_login.place(x=240, y=150)

    # label login
    state_label = Label(canvas_login, text="Login", font="Calibri 20 bold",
                        bg=bg_color)
    state_label.place(x=15, y=10)

    #label username
    Label(canvas_login, text="Usuario:", font="Calibri 15 bold",
            bg="#dbdbdb").place(x=30, y=80)

    #label contraseña
    Label(canvas_login, text="Contraseña:", font="Calibri 15 bold",
            bg="#dbdbdb").place(x=30, y=150)

    usuario = None
    contrasena = None

    # entry Usuario
    entry_user = Entry(canvas_login, font="Calibri 15", exportselection=0)
    entry_user.place(x=145, y=80)

    # entry Contraseña
    entry_contrasena = Entry(canvas_login, font="Calibri 15", show="•",
                                exportselection=0)
    entry_contrasena.place(x=145, y=150)

    # boton parar servidor (solo para admin)
    def stop_server():
        msg = {"type": "stop"}
        response = send_msg(msg)
        if response is not None:
            messagebox.showinfo("Información", "Se ha cerrado el servidor.")
    boton_cerrar_server = Button(root, text="Cerrar servidor",
                                font="Calibri 15 bold", command=stop_server)
    boton_cerrar_server.place(x=670, y=755)
    boton_cerrar_server.place_forget()

    # boton registro
    def registro_ventana():
        reg_ventana = Toplevel(root)
        reg_ventana.title("Registro - AppTaxi")
        reg_ventana.geometry("325x250")
        reg_ventana.resizable(False, False)

        # Titulo ventana
        reg_ventana_label = Label(reg_ventana, text="Registro",
                                    font="Calibri 20 bold")
        reg_ventana_label.grid(column=0, row=0)

        # Nombre
        reg_ventana_label_nombre = Label(reg_ventana, text="Nombre:",
                                            font="Calibri 15 bold")
        reg_ventana_label_nombre.grid(column=0, row=1)
        reg_ventana_entry_nombre = Entry(reg_ventana, font="Calibri 15",
                                            exportselection=0)
        reg_ventana_entry_nombre.grid(column=1, row=1)

        # Correo
        reg_ventana_label_correo = Label(reg_ventana, text="Correo:",
                                            font="Calibri 15 bold")
        reg_ventana_label_correo.grid(column=0, row=2)
        reg_ventana_entry_correo = Entry(reg_ventana, font="Calibri 15",
                                            exportselection=0)
        reg_ventana_entry_correo.grid(column=1, row=2)

        # Telefono
        reg_ventana_label_telf = Label(reg_ventana, text="Telefono:",
                                        font="Calibri 15 bold")
        reg_ventana_label_telf.grid(column=0, row=3)
        reg_ventana_entry_telf = Entry(reg_ventana, font="Calibri 15",
                                        exportselection=0)
        reg_ventana_entry_telf.grid(column=1, row=3)

        # Medio de pago
        reg_ventana_label_pago = Label(reg_ventana, text="nº Tarjeta:",
                                        font="Calibri 15 bold")
        reg_ventana_label_pago.grid(column=0, row=4)
        reg_ventana_entry_pago = Entry(reg_ventana, font="Calibri 15",
                                        exportselection=0)
        reg_ventana_entry_pago.grid(column=1, row=4)

        # Contraseña
        reg_ventana_label_pwd = Label(reg_ventana, text="Contraseña:",
                                        font="Calibri 15 bold")
        reg_ventana_label_pwd.grid(column=0, row=5)
        reg_ventana_entry_pwd = Entry(reg_ventana, font="Calibri 15",
                                        exportselection=0, show="•")
        reg_ventana_entry_pwd.grid(column=1, row=5)

        # Cancelar registro
        reg_ventana_cerrar = Button(reg_ventana, text="Cancelar",
                                    font="Calibri 15 bold",
                                    command=reg_ventana.destroy)
        reg_ventana_cerrar.grid(column=1, row=6)

        # Registrar
        def registrar():
            msg = dict()
            msg["type"] = "registro"
            msg["nombre"] = reg_ventana_entry_nombre.get()
            msg["mail"] = reg_ventana_entry_correo.get()
            msg["tlf"] = reg_ventana_entry_telf.get()
            msg["pago"] = reg_ventana_entry_pago.get()
            msg["pwd"] = sha256(reg_ventana_entry_pwd.get().encode()).hexdigest()

            if "" in msg.values():
                messagebox.showerror("Error",
                                        "No se han rellenado todos los campos.")
            else:
                response = send_msg(msg)
                if response is not None:
                    if response["data"] == True:
                        messagebox.showinfo("Información",
                                                "Se ha registrado el usuario.")
                        entry_user.delete(0, END)
                        entry_user.insert(0, reg_ventana_entry_correo.get())
                        entry_contrasena.delete(0, END)
                        entry_contrasena.insert(0, reg_ventana_entry_pwd.get())
                    else:
                        messagebox.showinfo("Información", "El usuario ya existe.")
                reg_ventana.destroy()

        reg_ventana_registro = Button(reg_ventana, text="Registrar",
                                    font="Calibri 15 bold", command=registrar)
        reg_ventana_registro.grid(column=0, row=6)

        reg_ventana.grab_set()
        reg_ventana.mainloop()

    boton_registro = Button(canvas_login, text="Registro", font="Calibri 15 bold",
                            command=registro_ventana)
    boton_registro.place(x=290, y=230)

    # boton login
    def login():
        msg = dict()
        msg["type"] = "login"
        msg["mail"] = entry_user.get()
        msg["pwd"] = sha256(entry_contrasena.get().encode()).hexdigest()
        response = send_msg(msg)
        if response is not None:
            if response["data"] == True:
                if entry_user.get() == "admin":
                    messagebox.showinfo("Información",
                                        "Los credenciales se han validado. " \
                                        "Se ha iniciado sesión como administrador.")
                    boton_cerrar_server.place(x=670, y=755)

                    # Ventana app
                    canvas_login.destroy()

                    # Lista taxis
                    taxi_list_label = Label(root, text="Listado de taxis en funcionamiento:",
                                            font="Calibri 15 bold")
                    taxi_list_label.place(x=30, y=120)
                    admin_taxi_listbox_scrollbar = Scrollbar(root)
                    admin_taxi_listbox = Listbox(root, height=12, width=80, font="Consolas 14",
                                                yscrollcommand=admin_taxi_listbox_scrollbar.set)
                    admin_taxi_listbox_scrollbar.place(x=840, y=150)
                    admin_taxi_listbox_scrollbar.config(command=admin_taxi_listbox.yview)

                    # Lista peticiones
                    petition_list_label = Label(root, text="Listado de peticiones:",
                                                font="Calibri 15 bold")
                    petition_list_label.place(x=30, y=440)
                    admin_petition_listbox_scrollbar = Scrollbar(root)
                    admin_petition_listbox = Listbox(root, height=12, width=80,
                                                font="Consolas 14",
                                                yscrollcommand=admin_petition_listbox_scrollbar.set)
                    admin_petition_listbox_scrollbar.place(x=840, y=470)
                    admin_petition_listbox_scrollbar.config(command=admin_petition_listbox.yview)

                    # Datos lista taxis
                    msg = dict()
                    msg["type"] = "list_taxi"
                    response = send_msg(msg, size=8192)
                    if response is not None:
                        taxi_list = response["data"]
                        for t in taxi_list:
                            admin_taxi_listbox.insert(END, t.ljust(40) +
                                                            taxi_list[t]["status"].rjust(40))

                    # Datos lista peticiones
                    msg = dict()
                    msg["type"] = "get_status"
                    response = send_msg(msg, size=4096)
                    if response is not None:
                        petition_list = response["data"]
                        for p in petition_list:
                            pet = petition_list[p]
                            admin_petition_listbox.insert(END, "%s : %s -> %s | %.2f km | %.2f € | %s - %s" %
                                                                (just(p, 8),
                                                                 just(pet["origin"], 12).ljust(12),
                                                                 just(pet["destination"], 12).ljust(12),
                                                                 pet["distance"],
                                                                 pet["price"],
                                                                 pet["date"],
                                                                 pet["hour"]))

                    def update_taxi_info():
                        msg = dict()
                        msg["type"] = "list_taxi"
                        response = send_msg(msg, size=8192)
                        admin_taxi_listbox.delete(0, END)
                        if response is not None:
                            taxi_list.clear()
                            taxi_list.update(response["data"])
                            for t in taxi_list:
                                admin_taxi_listbox.insert(END, t.ljust(40) +
                                                                taxi_list[t]["status"].rjust(40))

                    def show_taxi_info(self):
                        if len(admin_taxi_listbox.curselection()) == 0:
                            return
                        listbox_info = admin_taxi_listbox.get(admin_taxi_listbox.curselection()[0])
                        taxi_name = listbox_info[0:listbox_info.index(" ")]
                        taxi_info = taxi_list[taxi_name]
                        selected_taxi_info = Toplevel(root)
                        selected_taxi_info.title("Información del taxi \"" + taxi_name + "\"")
                        selected_taxi_info.geometry("210x150")
                        selected_taxi_info.resizable(False, False)
                        Label(selected_taxi_info, text="Id_taxi:",
                            font="Calibri 15 bold").grid(column=0, row=0, sticky="w")
                        Label(selected_taxi_info, text=taxi_name,
                            font="Calibri 15").grid(column=1, row=0, sticky="e")
                        Label(selected_taxi_info, text="Ubicación:",
                            font="Calibri 15 bold").grid(column=0, row=1, sticky="w")
                        Label(selected_taxi_info, text="Latitud:",
                            font="Calibri 15 bold").grid(column=0, row=2, sticky="w")
                        Label(selected_taxi_info, text="%2.8f" % taxi_info["latitude"],
                            font="Calibri 15").grid(column=1, row=2, sticky="e")
                        Label(selected_taxi_info, text="Longitud:",
                            font="Calibri 15 bold").grid(column=0, row=3, sticky="w")
                        Label(selected_taxi_info, text="%2.8f" % taxi_info["longitude"],
                            font="Calibri 15").grid(column=1, row=3, sticky="e")
                        Label(selected_taxi_info, text="Estado:",
                            font="Calibri 15 bold").grid(column=0, row=4, sticky="w")
                        Label(selected_taxi_info, text=taxi_info["status"],
                            font="Calibri 15").grid(column=1, row=4, sticky="e")
                        selected_taxi_info.grab_set()
                        selected_taxi_info.mainloop()

                    def update_petition_info():
                        msg = dict()
                        msg["type"] = "get_status"
                        response = send_msg(msg, size=4096)
                        admin_petition_listbox.delete(0, END)
                        if response is not None:
                            petition_list.clear()
                            petition_list.update(response["data"])
                            for p in petition_list:
                                pet = petition_list[p]
                                admin_petition_listbox.insert(END, "%s : %s -> %s | %.2f km | %.2f € | %s - %s" %
                                                                    (just(p, 8),
                                                                     just(pet["origin"], 12).ljust(12),
                                                                     just(pet["destination"], 12).ljust(12),
                                                                     pet["distance"],
                                                                     pet["price"],
                                                                     pet["date"],
                                                                     pet["hour"]))

                    def show_petition_info(self):
                        if len(petition_list) == 0 or len(admin_petition_listbox.curselection()) == 0:
                            return
                        petition_info_listbox = admin_petition_listbox.get(admin_petition_listbox.curselection()[0])
                        taxi_name = petition_info_listbox[0:petition_info_listbox.index(" ")]
                        petition_info = petition_list[taxi_name]
                        selected_petition_info = Toplevel(root)
                        selected_petition_info.title("Información de la peticion")
                        selected_petition_info.geometry("320x255")
                        selected_petition_info.resizable(False, False)
                        Label(selected_petition_info, text="Id_taxi:",
                            font="Calibri 15 bold").grid(column=0, row=0, sticky="w")
                        Label(selected_petition_info, text=taxi_name,
                            font="Calibri 15").grid(column=1, row=0, sticky="e")
                        Label(selected_petition_info, text="Origen:",
                            font="Calibri 15 bold").grid(column=0, row=1, sticky="w")
                        Label(selected_petition_info, text=just(petition_info["origin"], 15),
                            font="Calibri 15").grid(column=1, row=1, sticky="e")
                        Label(selected_petition_info, text="Destino:",
                            font="Calibri 15 bold").grid(column=0, row=2, sticky="w")
                        Label(selected_petition_info, text=just(petition_info["destination"], 15),
                            font="Calibri 15").grid(column=1, row=2, sticky="e")
                        Label(selected_petition_info, text="Distancia:",
                            font="Calibri 15 bold").grid(column=0, row=3, sticky="w")
                        Label(selected_petition_info, text="%.2f km" % petition_info["distance"],
                            font="Calibri 15").grid(column=1, row=3, sticky="e")
                        Label(selected_petition_info, text="Precio:",
                            font="Calibri 15 bold").grid(column=0, row=4, sticky="w")
                        Label(selected_petition_info, text="%.2f €" % petition_info["price"],
                            font="Calibri 15").grid(column=1, row=4, sticky="e")
                        Label(selected_petition_info, text="Fecha:",
                            font="Calibri 15 bold").grid(column=0, row=5, sticky="w")
                        Label(selected_petition_info, text=petition_info["date"],
                            font="Calibri 15").grid(column=1, row=5, sticky="e")
                        Label(selected_petition_info, text="Hora:",
                            font="Calibri 15 bold").grid(column=0, row=6, sticky="w")
                        Label(selected_petition_info, text=petition_info["hour"],
                            font="Calibri 15").grid(column=1, row=6, sticky="e")

                        def update_petition(st, taxi):
                            msg = dict()
                            msg["type"] = "status_update"
                            msg["status"] = st
                            msg["taxi"] = taxi
                            response = send_msg(msg)

                        def accept_petition():
                            update_petition("accept", taxi_name)
                            selected_petition_info.destroy()
                            update_petition_info()

                        def reject_petition():
                            update_petition("reject", taxi_name)
                            update_petition_info()
                            selected_petition_info.destroy()

                        Button(selected_petition_info, text="Aceptar peticion",
                                font="Calibri 15 bold", bg="#c0f9bb",
                                command=accept_petition).grid(column=0, row=7)
                        Button(selected_petition_info, text="Rechazar peticion",
                                font="Calibri 15 bold", bg="#f78f8f",
                                command=reject_petition).grid(column=1, row=7)
                        selected_petition_info.grab_set()
                        selected_petition_info.mainloop()
                    admin_taxi_listbox.bind("<<ListboxSelect>>", show_taxi_info)
                    admin_taxi_listbox.place(x=30, y=150)
                    taxi_list_update = Button(root, text="Recargar",
                                                font="Calibri 14 bold",
                                                command=update_taxi_info)
                    taxi_list_update.place(x=745, y=110)
                    admin_petition_listbox.bind("<<ListboxSelect>>", show_petition_info)
                    admin_petition_listbox.place(x=30, y=470)
                    petition_list_update = Button(root, text="Recargar",
                                                    font="Calibri 14 bold",
                                                    command=update_petition_info)
                    petition_list_update.place(x=745, y=430)
                else:
                    messagebox.showinfo("Información", "Los credenciales se han validado.")
                    print("Se ha iniciado sesion")
                    canvas_login.destroy()

                    user_ui_label = Label(root, text="Pedir un viaje", font="Calibri 15 bold")
                    user_ui_label.place(x=388, y=120)

                    # Origen
                    user_ui_origin_label = Label(root, text="Origen:", font="Calibri 15 bold")
                    user_ui_origin_label.place(x=250, y=160)
                    user_ui_origin_entry = Entry(root, font="Calibri 15", exportselection=0)
                    user_ui_origin_entry.place(x=370, y=160)

                    # Destino
                    user_ui_detination_label = Label(root, text="Destino:", font="Calibri 15 bold")
                    user_ui_detination_label.place(x=250, y=200)
                    user_ui_destination_entry = Entry(root, font="Calibri 15", exportselection=0)
                    user_ui_destination_entry.place(x=370, y=200)

                    # Fecha
                    user_ui_detination_date_label = Label(root, text="Fecha:", font="Calibri 15 bold")
                    user_ui_detination_date_label.place(x=250, y=240)
                    user_ui_destination_date_calendar = Calendar(root, selectmode="day",
                                                                year=int(date.today().strftime("%Y")),
                                                                month=int(date.today().strftime("%m")),
                                                                day=int(date.today().strftime("%d")))
                    user_ui_destination_date_calendar.place(x=370, y=240)

                    # Hora
                    user_ui_detination_time_label = Label(root, text="Hora:", font="Calibri 15 bold")
                    user_ui_detination_time_colon_label = Label(root, text=":", font="Calibri 15 bold")
                    hours_string_var = StringVar(root)
                    hours_string_var.set(datetime.now().strftime("%H"))
                    user_ui_destination_time_hours_spinbox = Spinbox(root, wrap=True,
                                                                    textvariable=hours_string_var,
                                                                    from_=0, to=23, width=2,
                                                                    font="Calibri 15")
                    minutes_string_var = StringVar(root)
                    minutes_string_var.set(datetime.now().strftime("%M"))
                    user_ui_destination_time_minutes_spinbox = Spinbox(root, wrap=True,
                                                                    textvariable=minutes_string_var,
                                                                    from_=0, to=59, width=2,
                                                                    font="Calibri 15")
                    user_ui_detination_time_label.place(x=250, y=440)
                    user_ui_destination_time_hours_spinbox.place(x=370, y=440)
                    user_ui_detination_time_colon_label.place(x=410, y=440)
                    user_ui_destination_time_minutes_spinbox.place(x=425, y=440)

                    # Boton pedir viaje
                    def send_travel():
                        msg = dict()
                        msg["type"] = "viaje"
                        msg["location"] = user_ui_origin_entry.get()
                        msg["destination"] = user_ui_destination_entry.get()
                        msg["date"] = user_ui_destination_date_calendar.get_date()
                        msg["hour"] = "%02d" % int(user_ui_destination_time_hours_spinbox.get()) + \
                                    ":" + "%02d" % int(user_ui_destination_time_minutes_spinbox.get())
                        if msg["location"] == "" or msg["destination"] == "":
                            messagebox.showwarning("Advertencia",
                                                    "Se debe indicar un origen y un destino.")
                            return
                        response = send_msg(msg)
                        if response is not None:
                            travel_data = response["data"]
                            taxi_name = travel_data["id_taxi"]
                            if travel_data is None:
                                messagebox.showwaring("Advertencia", "No hay taxis disponibles.")
                            else:
                                ui_travel_window = Toplevel(root)
                                ui_travel_window.geometry("420x200")
                                ui_travel_window.resizable(False, False)
                                Label(ui_travel_window, text="Datos viaje",
                                        font="Calibri 17 bold").grid(column=0, row=0, sticky="w")
                                Label(ui_travel_window, text="Taxi asignado:",
                                        font="Calibri 15 bold").grid(column=0, row=1, sticky="w")
                                Label(ui_travel_window, text=travel_data["id_taxi"],
                                        font="Calibri 15").grid(column=1, row=1, sticky="w")
                                Label(ui_travel_window, text="Origen:",
                                        font="Calibri 15 bold").grid(column=0, row=2, sticky="w")
                                Label(ui_travel_window, text=just(msg["location"], 12),
                                        font="Calibri 15").grid(column=1, row=2, sticky="w")
                                Label(ui_travel_window, text="Destino:",
                                        font="Calibri 15 bold").grid(column=2, row=2, sticky="w")
                                Label(ui_travel_window, text=just(msg["destination"], 12),
                                        font="Calibri 15").grid(column=3, row=2, sticky="w")
                                Label(ui_travel_window, text="Fecha:",
                                        font="Calibri 15 bold").grid(column=0, row=3, sticky="w")
                                Label(ui_travel_window, text=msg["date"],
                                        font="Calibri 15").grid(column=1, row=3, sticky="w")
                                Label(ui_travel_window, text="Hora:",
                                        font="Calibri 15 bold").grid(column=2, row=3, sticky="w")
                                Label(ui_travel_window, text=msg["hour"],
                                        font="Calibri 15").grid(column=3, row=3, sticky="w")
                                Label(ui_travel_window, text="Distancia:",
                                        font="Calibri 15 bold").grid(column=0, row=4, sticky="w")
                                Label(ui_travel_window, text="%.2f km" % travel_data["distancia"],
                                        font="Calibri 15").grid(column=1, row=4, sticky="w")
                                Label(ui_travel_window, text="Precio:",
                                        font="Calibri 15 bold").grid(column=2, row=4, sticky="w")
                                Label(ui_travel_window, text="%.2f €" % travel_data["precio"],
                                        font="Calibri 15").grid(column=3, row=4, sticky="w")
                                ui_travel_status_label = Label(ui_travel_window,
                                                                text="Se ha enviado la peticion.",
                                                                fg="#f2b648", font="Calibri 15 bold")
                                ui_travel_status_label.grid(column=0, columnspan=2, row=5, sticky="w")
                                ui_travel_refresh_button = None
                                ui_travel_close_button = None

                                def refresh():
                                    msg = dict()
                                    msg["type"] = "status"
                                    msg["taxi"] = taxi_name
                                    response = send_msg(msg)
                                    if response is not None:
                                        if response["data"] == "pending":
                                            ui_travel_status_label.config(text="Pendiente.")
                                        if response["data"] == "accept":
                                            ui_travel_status_label.config(text="Aceptada.",
                                                                            fg="#258c2c")
                                            ui_travel_refresh_button.grid_forget()
                                            ui_travel_close_button.grid(column=2, row=5, sticky="e")
                                        elif response["data"] == "reject":
                                            ui_travel_status_label.config(text="Rechazada.",
                                                                            fg="#c6311d")
                                            ui_travel_refresh_button.grid_forget()
                                            ui_travel_close_button.grid(column=2, row=5, sticky="e")

                                ui_travel_refresh_button = Button(ui_travel_window,
                                                                    text="Refrescar",
                                                                    font="Calibri 15 bold",
                                                                    command=refresh)
                                ui_travel_refresh_button.grid(column=3, row=5, sticky="e")
                                ui_travel_close_button = Button(ui_travel_window, text="Cerrar",
                                                                font="Calibri 15 bold",
                                                                command=ui_travel_window.destroy)
                                ui_travel_window.grab_set()
                                ui_travel_window.mainloop()

                    user_ui_confirm_travel_button = Button(root, text="Pedir viaje",
                                                            font="Calibri 15 bold",
                                                            command=send_travel)
                    user_ui_confirm_travel_button.place(x=370, y=480)

                    def user_data():
                        user_data_ventana = Toplevel(root)
                        user_data_ventana.title("Cambio de datos de usuario - AppTaxi")
                        user_data_ventana.geometry("405x250")
                        user_data_ventana.resizable(False, False)

                        # Titulo ventana
                        user_data_ventana_label = Label(user_data_ventana, text="Cambio de datos",
                                                    font="Calibri 20 bold")
                        user_data_ventana_label.grid(column=0, row=0)

                        # Nombre
                        user_data_ventana_label_nombre = Label(user_data_ventana, text="Nombre:",
                                                            font="Calibri 15 bold")
                        user_data_ventana_label_nombre.grid(column=0, row=1)
                        user_data_ventana_entry_nombre = Entry(user_data_ventana, font="Calibri 15",
                                                            exportselection=0)
                        user_data_ventana_entry_nombre.grid(column=1, row=1)

                        # Correo
                        user_data_ventana_label_correo = Label(user_data_ventana, text="Correo:",
                                                            font="Calibri 15 bold")
                        user_data_ventana_label_correo.grid(column=0, row=2)
                        user_data_ventana_entry_correo = Entry(user_data_ventana, font="Calibri 15",
                                                            exportselection=0)
                        user_data_ventana_entry_correo.grid(column=1, row=2)

                        # Telefono
                        user_data_ventana_label_telf = Label(user_data_ventana, text="Telefono:",
                                                        font="Calibri 15 bold")
                        user_data_ventana_label_telf.grid(column=0, row=3)
                        user_data_ventana_entry_telf = Entry(user_data_ventana, font="Calibri 15",
                                                        exportselection=0)
                        user_data_ventana_entry_telf.grid(column=1, row=3)

                        # Medio de pago
                        user_data_ventana_label_pago = Label(user_data_ventana, text="nº Tarjeta:",
                                                        font="Calibri 15 bold")
                        user_data_ventana_label_pago.grid(column=0, row=4)
                        user_data_ventana_entry_pago = Entry(user_data_ventana, font="Calibri 15",
                                                        exportselection=0)
                        user_data_ventana_entry_pago.grid(column=1, row=4)

                        # Contraseña
                        user_data_ventana_label_pwd = Label(user_data_ventana, text="Contraseña:",
                                                        font="Calibri 15 bold")
                        user_data_ventana_label_pwd.grid(column=0, row=5)
                        user_data_ventana_entry_pwd = Entry(user_data_ventana, font="Calibri 15",
                                                        exportselection=0, show="•")
                        user_data_ventana_entry_pwd.grid(column=1, row=5)

                        # Cancelar cambio de datos
                        user_data_ventana_cerrar = Button(user_data_ventana, text="Cancelar",
                                                    font="Calibri 15 bold",
                                                    command=user_data_ventana.destroy)
                        user_data_ventana_cerrar.grid(column=1, row=6)

                        # Cambiar datos
                        def cambiar():
                            msg = dict()
                            msg["type"] = "cambio"
                            msg["nombre"] = user_data_ventana_entry_nombre.get()
                            msg["mail"] = user_data_ventana_entry_correo.get()
                            msg["tlf"] = user_data_ventana_entry_telf.get()
                            msg["pago"] = user_data_ventana_entry_pago.get()
                            msg["pwd"] = sha256(user_data_ventana_entry_pwd.get().encode()).hexdigest()

                            if "" in msg.values():
                                messagebox.showerror("Error", "No se han rellenado todos los campos.")
                            else:
                                response = send_msg(msg)
                                if response is not None:
                                    if response["data"] == True:
                                        messagebox.showinfo("Información", "Se han cambiado los datos.")
                                    else:
                                        messagebox.showinfo("Información", "No se han podido cambiar los datos.")
                                user_data_ventana.destroy()

                        user_data_ventana_registro = Button(user_data_ventana, text="Cambiar",
                                                    font="Calibri 15 bold", command=cambiar)
                        user_data_ventana_registro.grid(column=0, row=6)

                        user_data_ventana.grab_set()
                        user_data_ventana.mainloop()

                    user_ui_data_button = Button(root, text="Cambiar datos de usuario",
                                                        font="Calibri 15 bold",
                                                        command=user_data)
                    user_ui_data_button.place(x=5, y=755)
            else:
                messagebox.showinfo("Información", "Los credenciales no son válidos.")

    # Boton login
    boton_login = Button(canvas_login, text="Login", font="Calibri 15 bold", command=login)
    boton_login.place(x=180, y=230)

    # Boton para salir
    boton_salir = Button(root, text="Salir", font="Calibri 15 bold", command=root.destroy)
    boton_salir.place(x=840, y=755)

    root.mainloop()

if __name__ == '__main__':
    main()
