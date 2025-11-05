#!/usr/bin/env python3
"""
Script interativo para mapear coordenadas de campos no PDF
Clica nas posições onde queres preencher texto
"""

import fitz  # PyMuPDF
import sys

def map_coordinates(pdf_path):
    """Abre PDF e permite clicar para mapear coordenadas"""
    try:
        import tkinter as tk
        from tkinter import simpledialog
        from PIL import Image, ImageTk
        import io
        
        doc = fitz.open(pdf_path)
        page = doc[0]  # Primeira página
        
        # Converter página para imagem
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Criar janela
        root = tk.Tk()
        root.title("Mapear Coordenadas do PDF - Clica nas posições dos campos")
        
        # Variáveis
        coordinates = []
        
        # Canvas para mostrar PDF
        canvas = tk.Canvas(root, width=img.width, height=img.height)
        canvas.pack()
        
        # Mostrar imagem
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        
        # Frame para instruções
        frame = tk.Frame(root)
        frame.pack(pady=10)
        
        label = tk.Label(frame, text="Clica na posição do campo e dá um nome", 
                        font=("Arial", 12, "bold"))
        label.pack()
        
        # Lista de campos
        fields_frame = tk.Frame(root)
        fields_frame.pack(pady=10)
        
        fields_label = tk.Label(fields_frame, text="Campos mapeados:", 
                               font=("Arial", 10, "bold"))
        fields_label.pack()
        
        fields_text = tk.Text(fields_frame, width=80, height=15)
        fields_text.pack()
        
        def on_click(event):
            """Quando clica no PDF"""
            # Converter coordenadas de canvas para PDF
            # Canvas está em 2x zoom
            x_pdf = event.x / 2
            # Inverter Y (PDF tem origem no canto inferior esquerdo)
            y_pdf = page.rect.height - (event.y / 2)
            
            # Perguntar nome do campo
            field_name = simpledialog.askstring("Nome do Campo", 
                                               f"Nome do campo na posição ({x_pdf:.1f}, {y_pdf:.1f})?")
            
            if field_name:
                coordinates.append({
                    'name': field_name,
                    'x': x_pdf,
                    'y': y_pdf
                })
                
                # Desenhar marcador
                canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, 
                                  fill='red', outline='white', width=2)
                canvas.create_text(event.x, event.y-15, text=field_name, 
                                  fill='red', font=("Arial", 10, "bold"))
                
                # Atualizar lista
                fields_text.delete(1.0, tk.END)
                fields_text.insert(tk.END, "COORDENADAS MAPEADAS:\n")
                fields_text.insert(tk.END, "="*70 + "\n\n")
                
                for coord in coordinates:
                    fields_text.insert(tk.END, 
                        f"'{coord['name']}': ({coord['x']:.1f}, {coord['y']:.1f}),\n")
                
                fields_text.insert(tk.END, "\n" + "="*70 + "\n")
                fields_text.insert(tk.END, "\n📝 CÓDIGO PYTHON:\n\n")
                fields_text.insert(tk.END, "FIELD_POSITIONS = {\n")
                for coord in coordinates:
                    fields_text.insert(tk.END, 
                        f"    '{coord['name']}': ({coord['x']:.1f}, {coord['y']:.1f}),\n")
                fields_text.insert(tk.END, "}\n")
        
        canvas.bind("<Button-1>", on_click)
        
        # Botão para guardar
        def save_coordinates():
            with open('pdf_field_coordinates.txt', 'w') as f:
                f.write("COORDENADAS DOS CAMPOS DO PDF\n")
                f.write("="*70 + "\n\n")
                for coord in coordinates:
                    f.write(f"{coord['name']}: ({coord['x']:.1f}, {coord['y']:.1f})\n")
                f.write("\n" + "="*70 + "\n")
                f.write("\nCÓDIGO PYTHON:\n\n")
                f.write("FIELD_POSITIONS = {\n")
                for coord in coordinates:
                    f.write(f"    '{coord['name']}': ({coord['x']:.1f}, {coord['y']:.1f}),\n")
                f.write("}\n")
            
            label.config(text=f"✅ {len(coordinates)} campos guardados em pdf_field_coordinates.txt")
        
        save_btn = tk.Button(root, text="💾 Guardar Coordenadas", 
                            command=save_coordinates, 
                            font=("Arial", 12, "bold"),
                            bg="#009cb6", fg="white", padx=20, pady=10)
        save_btn.pack(pady=10)
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro: Falta instalar dependências")
        print(f"\nInstala com:")
        print(f"  pip3 install PyMuPDF pillow")
        print(f"\nErro: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 map_pdf_coordinates.py <caminho_do_pdf>")
        print("\nExemplo:")
        print("  python3 map_pdf_coordinates.py 'DR 39:2025.pdf'")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    map_coordinates(pdf_path)
