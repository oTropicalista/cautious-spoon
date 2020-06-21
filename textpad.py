# Nome: textpad.py
# Autor: oTropicalista
# Data: 14/05
# Descrição: Simple notepad in python with GUI GTK create using Glade.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Main:

    def __init__(self):
        #get the window file
        gladeFile = "textpad.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladeFile)

        #Gtk.Application.add_accelerator()

        window = self.builder.get_object("janela")
        window.connect("delete-event", Gtk.main_quit)
        window.show()

        self.create_textview()
        self.create_powerbar()

    
    #metodo para criação da textview    
    def create_textview(self):
        #pega o txtpad e crio o self.textview
        self.textview = self.builder.get_object("txt_pad")
        self.textbuffer = self.textview.get_buffer()
        
        self.tag_found = self.textbuffer.create_tag("found", background="yellow", foreground="black")
        self.tag_def = self.textbuffer.create_tag("tagdef", foreground="red")
        tag = self.textbuffer.create_tag("orange_bg", background="orange")
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.apply_tag(tag, start_iter, end_iter)

        
        cursor_mark = self.textbuffer.get_insert()
        start = self.textbuffer.get_iter_at_mark(cursor_mark)
        text = "def"
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_def, match_start, match_end)

    #metodo para criação da barra inferior
    def create_powerbar(self):
        self.power_bar = self.builder.get_object("txt_bar")
        self.button_run = self.builder.get_object("btn_run")
        self.button_run.connect("clicked", self.RunCommand)

    #metodo para rodar os comandos da powerbar
    def RunCommand(self, widget):
        #pega o comando inserido na barra
        cmd = self.power_bar.get_text()
        print("Comando cru:", cmd)
        #limpa o conteudo da barra
        self.power_bar.set_text("")
        #escolha do método referente ao comando dado
        if "new" in cmd:
            self.new_document()
        elif "open" in cmd:
            var = cmd.split()#separa termos
            open_name = str(var[1])#pega só o nome do arquivo
            self.open_document(open_name)

        elif "save" in cmd:
            var = cmd.split()#separa termos
            save_name = str(var[1])#pega só o nome do arquivo
            self.save_document(save_name)
        elif "search" in cmd:
            #pegar o qeu tem que ser buscado
            var1 = cmd.split()#separa em lista pelos espaços
            var1.pop(0)#aqui apaga o primeiro item da lista, o "search"
            text = " ".join(var1)# aqui já temos o termo de pesquisa separado por espaços
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()
            
            self.search_and_mark(text, start)
    
    def search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)

    def new_document(self):
        self.textbuffer.set_text("")

    def open_document(self, selected_file):
        #abre o arquivo
        with open(selected_file, 'r') as f:
            data = f.read()
            self.textbuffer.set_text(data)

    def save_document(self, save_file):
        #pega certinho o conteúdo do buffer
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(start_iter, end_iter, True)   

        #grava no arquivo
        with open(save_file, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    main = Main()
    Gtk.main()
