import tkinter as tk
from tkinter import font # sirve para manejar los tipos de fuentes de letras
from tkinter import ttk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from formularios.conexion import DataBase

class FormularioMaestroDesign (tk.Tk): 
     
    def __init__(self):
        super().__init__()
        #self.logo = util_img.leer_imagen("./imagenes/anc_logo.png", (553,561))
        self.db = DataBase()
        self.modificar=False
        self.dni=tk.StringVar()
        self.sexo=tk.StringVar()
        self.nombres=tk.StringVar()
        self.apellidos=tk.StringVar()
        self.perfil = util_img.leer_imagen("./imagenes/foto_perfil.png", (120, 110))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo_principal()
        self.llenar_tabla()
    
    def config_window(self):
        self.title("CONTROL Y REGISTRO DE PACIENTES")
        self.iconbitmap("./imagenes/anc_logo.ico")
        w, h = 600, 400
        self.geometry("%dx%d+0+0" % (w, h))
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
        self.barra_superior = tk.Frame (self, bg = COLOR_BARRA_SUPERIOR, height= 50) # Un Frame es un widget que sirve como contenedor para otros widgets, se puede entender como un subconjunto de wigdgets
        self.barra_superior.pack(side = tk.TOP, fill= "both") # sirve para ubicar el Frame barra_superior en la ventana 

        self.menu_lateral = tk.Frame(self, bg = COLOR_MENU_LATERAL, width = 150)
        self.menu_lateral.pack (side = tk.LEFT, fill= "both", expand = False)
        
        
        self.cuerpo_principal = tk.Frame (self, bg = COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack( side = tk.RIGHT, fill ="both", expand =True)

    def controles_barra_superior(self):
        font_awesome =font.Font( family = "FontAwesome", size = 12)

        self.labeltitulo = tk.Label (self.barra_superior, text = "Método ANC")
        self.labeltitulo.config(fg = "#fff", font = ("Roboto", 15), bg= COLOR_BARRA_SUPERIOR, pady =10, width =16)
        self.labeltitulo.pack (side =tk.LEFT)

        self.buttonMenuLateral = tk.Button(self.barra_superior,text="\uf0c9",command = self.toggle_panel, font = font_awesome,bd=0,bg=COLOR_BARRA_SUPERIOR,fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        self.labeltitulo=tk.Label(self.barra_superior, text="felipe.gomez@anc.com.mx")
        self.labeltitulo.config(fg="#fff", font=("Roboto",12), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labeltitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        ancho_menu= 20
        alto_menu = 2
        font_awesome = font.Font(family = "FontAwesome", size =12)
        self.labelperfil = tk.Label(self.menu_lateral, image = self.perfil, bg = COLOR_MENU_LATERAL)
        self.labelperfil.pack(side =tk.TOP, pady = 30)
        # A continuación se van a instanciar todos los botones del menú lateral

        self.boton_eliminar = tk.Button(self.menu_lateral, command =self.eliminar)
        self.boton_nuevo = tk.Button(self.menu_lateral, command = self.nuevo)
        self.boton_modificar = tk.Button(self.menu_lateral, command = self.actualizar )

      

        

        #Configuración y empaquetamiento de los botones

        buttons_info = [
            ("Eliminar", "\uf2ed", self.boton_eliminar),
            ("Guardar", "\uf0c7", self.boton_nuevo),
            ("Seleccionar","\uf14a", self.boton_modificar),
            ]
        
        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

    def configurar_boton_menu(self,button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text = f"  {icon}  {text}", anchor="w", font = font_awesome,
                     bd=0, bg=COLOR_MENU_LATERAL, fg = "white", width =ancho_menu, height = alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self,button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))
   
    def on_enter(self,event,button):
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg="white")
   
    def on_leave (self,event,button):
        button.config(bg=COLOR_MENU_LATERAL, fg="white")
    
    
    
    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill="y")
    
    #funciones del treeview
    def modificarFalse(self):
        self.modificar=False
        self.tvEstudiantes.config(selectmode= "none")
        self.boton_nuevo.config(text=" \uf0c7 Guardar")
        self.boton_modificar.config(text=" \uf14a Seleccionar")
        self.boton_eliminar.config(state="disabled")

    def modificarTrue(self):
       
        self.modificar=True
        self.tvEstudiantes.config(selectmode= "browse")
        self.boton_nuevo.config(text=" \uf03a Nuevo")
        self.boton_modificar.config(text=" \uf304 Modificar")
        self.boton_eliminar.config(state="normal")



    def limpiar(self):
        self.dni.set("")
        self.nombres.set("")
        self.apellidos.set("")

    def validar(self):
        return len(self.dni.get()) and len(self.nombres.get()) and len(self.apellidos.get()) 

    def vaciar_tabla(self):
        filas = self.tvEstudiantes.get_children()
        for fila in filas:
            self.tvEstudiantes.delete(fila)

    def llenar_tabla(self):
        self.vaciar_tabla()
        sql ="SELECT* FROM estudiantes"
        self.db.cursor.execute(sql)
        filas = self.db.cursor.fetchall()
    
        for fila in filas:
            id = fila[0]
            self.tvEstudiantes.insert("", "end", id, text = id, values=fila)

    def eliminar(self):
        id= self.tvEstudiantes.selection()[0]
        if int(id)>0:
            sql="delete from estudiantes where id="+id
            self.db.cursor.execute(sql)
            self.db.connection.commit()
            self.tvEstudiantes.delete(id)
            self.lblMensaje.config(text="El registro ha sido eliminado correctamente")
        else:
            self.lblMensaje.config(text="Seleccione un registro para eliminar")


    def nuevo(self):
        if self.modificar==False:
            if self.validar():
                val = (self.dni.get(),self.sexo.get(),self.nombres.get(),self.apellidos.get())
                sql = "INSERT INTO estudiantes (dni, sexo, nombres, apellidos) values(%s,%s,%s,%s)"
                self.db.cursor.execute(sql,val)
                self.db.connection.commit()
                self.lblMensaje.config(text="Se guardó un registro correctamente", fg="green")
                self.llenar_tabla()
                self.limpiar()
            else:
                self.lblMensaje.config(text="Los campos no deben estar vacios", fg="red")
        else:
            self.modificarFalse()

    def actualizar(self):
        if self.modificar==True:
            if self.validar():
                id= self.tvEstudiantes.selection()[0]
                val = (self.dni.get(),self.sexo.get(),self.nombres.get(),self.apellidos.get())
                sql = "UPDATE estudiantes SET dni=%s, sexo=%s, nombres=%s, apellidos=%s WHERE id="+id
                self.db.cursor.execute(sql,val)
                self.db.connection.commit()
                self.lblMensaje.config(text="Se ha actualizado un registro correctamente", fg="green")
                self.llenar_tabla()
                self.limpiar()
            else:
                self.lblMensaje.config(text="Los campos no deben estar vacios", fg="red")
        else:
            self.modificarTrue()
          
       

    def controles_cuerpo_principal(self):

        #Etuquetas y cajas de texto
        lblDni= tk.Label (self.cuerpo_principal, text="DNI",bg =COLOR_CUERPO_PRINCIPAL).grid(column=0,row=0,padx=5,pady=5)
        textDni = tk.Entry(self.cuerpo_principal, textvariable=self.dni)
        textDni.grid(column = 1, row=0)

        lblSexo= tk.Label (self.cuerpo_principal, text="Sexo",bg =COLOR_CUERPO_PRINCIPAL).grid(column=0,row=1,padx=5,pady=5)
        textSexo = ttk.Combobox(self.cuerpo_principal,values=["M","F"], textvariable=self.sexo)
        textSexo.grid(column = 1, row=1)
        textSexo.current(0)

        lblNombres= tk.Label (self.cuerpo_principal, text="Nombres",bg =COLOR_CUERPO_PRINCIPAL).grid(column=2,row=0,padx=5,pady=5)
        textNombres = tk.Entry(self.cuerpo_principal, textvariable=self.nombres)
        textNombres.grid(column = 3, row=0)

        lblApellidos= tk.Label (self.cuerpo_principal, text="Apellidos",bg =COLOR_CUERPO_PRINCIPAL).grid(column=2,row=1,padx=5,pady=5)
        textApellidos = tk.Entry(self.cuerpo_principal, textvariable=self.apellidos)
        textApellidos.grid(column = 3, row=1)

        self.lblMensaje=tk.Label(self.cuerpo_principal, text="Mensajes",bg=COLOR_CUERPO_PRINCIPAL)
        self.lblMensaje.grid(column=0, row=2, columnspan=4)

        #Treeview

        self.tvEstudiantes=ttk.Treeview(self.cuerpo_principal, selectmode= "none")
        self.tvEstudiantes.grid(column=0, row=3, columnspan=4, padx=5,pady=10)

        self.tvEstudiantes["columns"]=("ID","SEXO","DNI","NOMBRES","APELLIDOS")
        self.tvEstudiantes.column("#0",width=0,stretch="no")
        self.tvEstudiantes.column("ID", width=50, anchor="center")
        self.tvEstudiantes.column("SEXO", width=50, anchor="center")
        self.tvEstudiantes.column("DNI", width=50, anchor="center")
        self.tvEstudiantes.column("NOMBRES", width=100, anchor="center")
        self.tvEstudiantes.column("APELLIDOS", width=100, anchor="center")

        self.tvEstudiantes.heading("#0",text="")
        self.tvEstudiantes.heading("ID", text="ID", anchor="center")
        self.tvEstudiantes.heading("SEXO", text="SEXO", anchor="center")
        self.tvEstudiantes.heading("DNI", text="DNI", anchor="center")
        self.tvEstudiantes.heading("NOMBRES", text="NOMBRES", anchor="center")
        self.tvEstudiantes.heading("APELLIDOS", text="APELLIDOS", anchor="center")

     

       