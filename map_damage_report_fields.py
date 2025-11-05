#!/usr/bin/env python3
"""
Sistema interativo para mapear campos do Damage Report PDF
Clica nas posições onde queres preencher cada campo
"""

import fitz  # PyMuPDF
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
import json

# Lista de campos a mapear
FIELDS_TO_MAP = [
    # Topo
    ('dr_number', 'DR Nº (topo direita)'),
    ('date', 'Data (topo direita)'),
    
    # Cliente
    ('client_name', 'Nome Completo do Cliente'),
    ('client_email', 'Email do Cliente'),
    ('client_phone', 'Telefone do Cliente'),
    ('client_address', 'Morada do Cliente'),
    ('client_postal_code', 'Código Postal'),
    ('client_city', 'Cidade'),
    ('client_country', 'País'),
    
    # Veículo
    ('vehicle_plate', 'Matrícula'),
    ('vehicle_brand', 'Marca'),
    ('vehicle_model', 'Modelo'),
    
    # Levantamento
    ('pickup_date', 'Data de Levantamento'),
    ('pickup_time', 'Hora de Levantamento'),
    ('pickup_location', 'Local de Levantamento'),
    
    # Devolução
    ('return_date', 'Data de Devolução'),
    ('return_time', 'Hora de Devolução'),
    ('return_location', 'Local de Devolução'),
    
    # Outros
    ('issued_by', 'Feito por / Issued by'),
]

class PDFFieldMapper:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.page = self.doc[0]
        self.coordinates = {}
        self.current_field_index = 0
        
        # Criar janela
        self.root = tk.Tk()
        self.root.title("Mapear Campos do Damage Report - Clica na posição de cada campo")
        self.root.geometry("1400x900")
        
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame esquerdo (PDF)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame direito (instruções e lista)
        right_frame = tk.Frame(main_frame, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Instruções
        self.create_instructions(right_frame)
        
        # Canvas para PDF
        self.create_pdf_canvas(left_frame)
        
        # Lista de campos
        self.create_fields_list(right_frame)
        
        # Botões
        self.create_buttons(right_frame)
        
        # Mostrar primeiro campo
        self.update_current_field()
        
    def create_instructions(self, parent):
        """Criar painel de instruções"""
        frame = tk.LabelFrame(parent, text="📋 Instruções", font=("Arial", 12, "bold"))
        frame.pack(fill=tk.X, pady=(0, 10))
        
        instructions = [
            "1. Vê o campo atual destacado abaixo",
            "2. Clica no PDF onde esse campo deve ser preenchido",
            "3. O próximo campo aparece automaticamente",
            "4. Podes pular campos com 'Pular'",
            "5. No fim, clica 'Guardar Coordenadas'"
        ]
        
        for inst in instructions:
            label = tk.Label(frame, text=inst, font=("Arial", 10), anchor="w")
            label.pack(fill=tk.X, padx=10, pady=2)
        
        # Campo atual
        self.current_field_label = tk.Label(frame, text="", 
                                           font=("Arial", 14, "bold"),
                                           fg="white", bg="#009cb6", 
                                           pady=10)
        self.current_field_label.pack(fill=tk.X, padx=10, pady=10)
        
    def create_pdf_canvas(self, parent):
        """Criar canvas com PDF"""
        # Converter página para imagem
        zoom = 1.5
        mat = fitz.Matrix(zoom, zoom)
        pix = self.page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Criar canvas com scrollbar
        canvas_frame = tk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas = tk.Canvas(canvas_frame, 
                               yscrollcommand=scrollbar_y.set,
                               xscrollcommand=scrollbar_x.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar_y.config(command=self.canvas.yview)
        scrollbar_x.config(command=self.canvas.xview)
        
        # Mostrar imagem
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        # Guardar zoom para conversão de coordenadas
        self.zoom = zoom
        
        # Bind click
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def create_fields_list(self, parent):
        """Criar lista de campos mapeados"""
        frame = tk.LabelFrame(parent, text="✅ Campos Mapeados", 
                             font=("Arial", 12, "bold"))
        frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Criar Treeview
        self.tree = ttk.Treeview(frame, columns=('Status', 'X', 'Y'), 
                                 show='tree headings', height=15)
        self.tree.heading('#0', text='Campo')
        self.tree.heading('Status', text='Status')
        self.tree.heading('X', text='X')
        self.tree.heading('Y', text='Y')
        
        self.tree.column('#0', width=200)
        self.tree.column('Status', width=60)
        self.tree.column('X', width=50)
        self.tree.column('Y', width=50)
        
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Adicionar todos os campos
        for field_id, field_name in FIELDS_TO_MAP:
            self.tree.insert('', tk.END, iid=field_id, 
                           text=field_name, 
                           values=('⏳', '', ''))
        
    def create_buttons(self, parent):
        """Criar botões de controle"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão Pular
        skip_btn = tk.Button(frame, text="⏭️ Pular Campo", 
                            command=self.skip_field,
                            font=("Arial", 11),
                            bg="#ffa500", fg="white",
                            padx=10, pady=5)
        skip_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Botão Voltar
        back_btn = tk.Button(frame, text="⬅️ Campo Anterior", 
                            command=self.previous_field,
                            font=("Arial", 11),
                            bg="#666", fg="white",
                            padx=10, pady=5)
        back_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Botão Guardar
        save_btn = tk.Button(frame, text="💾 Guardar Coordenadas", 
                            command=self.save_coordinates,
                            font=("Arial", 12, "bold"),
                            bg="#009cb6", fg="white",
                            padx=10, pady=10)
        save_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Label de progresso
        self.progress_label = tk.Label(frame, text="", 
                                      font=("Arial", 10))
        self.progress_label.pack(pady=(10, 0))
        
    def update_current_field(self):
        """Atualizar campo atual"""
        if self.current_field_index < len(FIELDS_TO_MAP):
            field_id, field_name = FIELDS_TO_MAP[self.current_field_index]
            self.current_field_label.config(
                text=f"📍 Clica para: {field_name}"
            )
            
            # Atualizar progresso
            total = len(FIELDS_TO_MAP)
            mapped = len(self.coordinates)
            self.progress_label.config(
                text=f"Progresso: {mapped}/{total} campos mapeados"
            )
        else:
            self.current_field_label.config(
                text="✅ Todos os campos mapeados!"
            )
            messagebox.showinfo("Concluído", 
                              "Todos os campos foram mapeados!\n\n"
                              "Clica em 'Guardar Coordenadas' para finalizar.")
    
    def on_canvas_click(self, event):
        """Quando clica no canvas"""
        if self.current_field_index >= len(FIELDS_TO_MAP):
            return
        
        field_id, field_name = FIELDS_TO_MAP[self.current_field_index]
        
        # Converter coordenadas de canvas para PDF
        x_pdf = event.x / self.zoom
        y_pdf = self.page.rect.height - (event.y / self.zoom)
        
        # Guardar coordenadas
        self.coordinates[field_id] = (x_pdf, y_pdf)
        
        # Desenhar marcador
        self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5,
                               fill='red', outline='white', width=2)
        self.canvas.create_text(event.x, event.y-15, 
                               text=field_id,
                               fill='red', font=("Arial", 8, "bold"))
        
        # Atualizar lista
        self.tree.item(field_id, values=('✅', f'{x_pdf:.1f}', f'{y_pdf:.1f}'))
        
        # Próximo campo
        self.current_field_index += 1
        self.update_current_field()
    
    def skip_field(self):
        """Pular campo atual"""
        if self.current_field_index < len(FIELDS_TO_MAP):
            field_id, _ = FIELDS_TO_MAP[self.current_field_index]
            self.tree.item(field_id, values=('⏭️', '-', '-'))
            self.current_field_index += 1
            self.update_current_field()
    
    def previous_field(self):
        """Voltar ao campo anterior"""
        if self.current_field_index > 0:
            self.current_field_index -= 1
            field_id, _ = FIELDS_TO_MAP[self.current_field_index]
            
            # Remover coordenadas se existirem
            if field_id in self.coordinates:
                del self.coordinates[field_id]
            
            self.tree.item(field_id, values=('⏳', '', ''))
            self.update_current_field()
    
    def save_coordinates(self):
        """Guardar coordenadas em ficheiro"""
        if not self.coordinates:
            messagebox.showwarning("Aviso", "Nenhum campo foi mapeado!")
            return
        
        # Guardar em JSON
        with open('damage_report_coordinates.json', 'w') as f:
            json.dump(self.coordinates, f, indent=2)
        
        # Guardar código Python
        with open('damage_report_coordinates.py', 'w') as f:
            f.write("# Coordenadas dos campos do Damage Report PDF\n")
            f.write("# Gerado automaticamente pelo map_damage_report_fields.py\n\n")
            f.write("DAMAGE_REPORT_FIELDS = {\n")
            for field_id, (x, y) in self.coordinates.items():
                f.write(f"    '{field_id}': ({x:.1f}, {y:.1f}),\n")
            f.write("}\n")
        
        messagebox.showinfo("Sucesso", 
                          f"✅ {len(self.coordinates)} campos guardados!\n\n"
                          f"Ficheiros criados:\n"
                          f"• damage_report_coordinates.json\n"
                          f"• damage_report_coordinates.py")
        
        self.root.quit()
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    mapper = PDFFieldMapper("Damage Report.pdf")
    mapper.run()
