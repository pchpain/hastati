import tkinter
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import pymongo


class LeftPane(tkinter.Frame):
    def __init__(self, master=None, relief=tkinter.constants.RAISED, borderwidth='2c'):
        tkinter.Frame.__init__(self, master)
        self.top_level = self.winfo_toplevel() 
        self.create_widgets()
        self.client = pymongo.MongoClient()

    def create_widgets(self):
        database_options = [
                "Eurostat",
                "INSEE",
                "INE"
        ]
        default = tkinter.StringVar(self)
        default.set(database_options[0])
        self.database_sel = tkinter.OptionMenu(self, default, *database_options)
        self.database_sel.pack(fill="both",side="top")
        def eurostat_tree(self)
            id_categories = self.client.eurostat.categories.find({'_id': 1})
            id_children = self.client.eurostat.categories.find({'children': 1})
            def flatten(li):
                if not isinstance(li, list):
                    return [li]
                result = []
                for ll in li:
                    result.extend(flatten(ll))
                return result
            id_children = flatten(id_children)
            return [id for id in id_categories if id not in children]

        self.tree = ttk.Treeview(self)
        self.node = self.tree.insert('', 'end', text='National accounts')
        self.tree.insert(self.node, 0, 'toto', text='PIB - quarterly')
        self.tree.insert(self.node, 1, 'gallery', text='PIB - annualy')
        self.node2 = self.tree.insert('', 'end', text='Industrial production')
        self.tree.insert(self.node2, 0, 'blub', text='By main industrial croupings')
        self.tree.pack(fill='both', side="top", expand=True)


class Graph(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.top_level = self.winfo_toplevel() 
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tkinter.Canvas(self,bg='red')
        self.graph_file = Image.open('ip.png')
        self.graph = ImageTk.PhotoImage(self.graph_file)
        self.image = self.canvas.create_image(0,0,anchor='nw', image=self.graph, tag='GRAPH')
        self.canvas.bind('<Configure>', self.resize )
        self.canvas.pack(side="top",expand=1,fill="both")
    def resize(self,event):
        self.cvw, self.cvh = self.winfo_width(), self.winfo_height()
        self.canvas.delete("GRAPH")
        self.graph_image = self.graph_file.resize((self.cvw, self.cvh), Image.ANTIALIAS)
        self.graph = ImageTk.PhotoImage(self.graph_image)
        self.image = self.canvas.create_image(0,0,anchor='nw', image=self.graph, tag='GRAPH')

class RightPane(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.top_level = self.winfo_toplevel() 
        self.create_widgets()

    def create_widgets(self):
        self.top_graph = Graph(master=self)
        self.top_graph.pack(fill="both",side="top", expand=True)
        self.buttons_graph = ButtonsGraph(master=self)
        self.buttons_graph.pack(fill="both",side="bottom", expand=False)


class ButtonsGraph(tkinter.Frame):
    def __init__(self, master=None):
        self.top_frame = tkinter.Frame.__init__(self, master)
        self.top_level = self.winfo_toplevel() 
        self.create_widgets()
        master.rowconfigure(1,weight=1)
        master.columnconfigure(2,weight=1)
    def create_widgets(self):
        self.variation_rate = tkinter.Button(self, text = "Variation rate")
        self.variation_rate.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.scale = tkinter.Button(self, text = "Scale")
        self.scale.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.frequency = tkinter.Button(self, text = "Frequency")
        self.frequency.grid(row=0, column=2, sticky=tkinter.NSEW)
        self.base_shift = tkinter.Button(self, text = "Rebase")
        self.base_shift.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.hp_filter = tkinter.Button(self, text = "HP filter")
        self.hp_filter.grid(row=1, column=1, sticky=tkinter.NSEW)
        self.plus = tkinter.Button(self, text = "+")
        self.plus.grid(row=1, column=2, sticky=tkinter.NSEW)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        
        
class About(tkinter.Frame):
    def __init__(self, master=None):
        self.top_frame = tkinter.Frame.__init__(self, master)
        self.top_level = self.winfo_toplevel() 
        self.top_level.title("Hastati - About")
        top = self.winfo_toplevel()
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.credits_title = tkinter.LabelFrame(self, text="Credits")
        self.credits_title.pack(side="top")
        self.credits = tkinter.Label(self.credits_title, text = 
                                     "Part of the Widukind suite \n"
                                     "Product licenced under the GPLv3 \n"
                                     "Michaël Malter, Pierre Chuong\n"
                                     "Cepremap")
        self.credits.pack(side="right")
        self.ok = tkinter.Button(self, text="OK",
                                command=self.master.destroy)
        self.ok.pack(side="bottom")


class Application(tkinter.Frame):
    def __init__(self, master=None):
        self.top_frame = tkinter.Frame.__init__(self, master)
        self.top_level = self.winfo_toplevel() 
        self.top_level.title("Hastati")
        top = self.winfo_toplevel()

        self.menu_bar = tkinter.Menu(top)
        top['menu'] = self.menu_bar

        self.sub_menu_file = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='File', menu=self.sub_menu_file)
        self.sub_menu_file.add_command(label='Quit',
                                       command=self.master.destroy)

        self.sub_menu_help = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Help', menu=self.sub_menu_help)
        self.sub_menu_help.add_command(label='About',
                                       command=self.__about_handler)

        self.left_pane = LeftPane(master=self)
        self.left_pane.pack(side="left", fill="both")
        self.right_pane = RightPane(master=self)
        self.right_pane.pack(side="right", fill="both", expand=True)
        
    def __about_handler(self, master=None):
        root_about = tkinter.Tk()
        about_window = About(master=root_about)
        about_window.mainloop()


root = tkinter.Tk()
application = Application(master=root)
application.pack(side='top',fill='both',expand=True)
application.mainloop()
