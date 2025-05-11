import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'db_agenda',
    'user': 'postgres',
    'password': 'root',
    'port': 5432
}

# Função para conectar ao banco
def conectar():
    return psycopg2.connect(**DB_CONFIG)

# Função para inserir um novo contato
def inserir_contato():
    nome = nome_entry.get()
    telefone = telefone_entry.get()
    email = email_entry.get()
    data_nasc = nascimento_entry.get()
    
    if nome == "" or telefone == "":
        messagebox.showwarning("Atenção", "Nome e telefone são obrigatórios.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO contatos (nome, telefone, email, data_nascimento)
            VALUES (%s, %s, %s, %s)
        """, (nome, telefone, email, data_nasc))
        conn.commit()
        cur.close()
        conn.close()
        listar_contatos()
        limpar_campos()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para listar contatos
def listar_contatos():
    for row in tree.get_children():
        tree.delete(row)

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM contatos ORDER BY id")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para deletar um contato
def deletar_contato():
    id_contato = id_entry.get()
    if not id_contato:
        messagebox.showwarning("Atenção", "Selecione um contato para deletar.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM contatos WHERE id = %s", (id_contato,))
        conn.commit()
        cur.close()
        conn.close()
        listar_contatos()
        limpar_campos()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para atualizar um contato
def atualizar_contato():
    id_contato = id_entry.get()
    nome = nome_entry.get()
    telefone = telefone_entry.get()
    email = email_entry.get()
    data_nasc = nascimento_entry.get()

    if not id_contato:
        messagebox.showwarning("Atenção", "Selecione um contato para atualizar.")
        return

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE contatos 
            SET nome=%s, telefone=%s, email=%s, data_nascimento=%s
            WHERE id=%s
        """, (nome, telefone, email, data_nasc, id_contato))
        conn.commit()
        cur.close()
        conn.close()
        listar_contatos()
        limpar_campos()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para limpar os campos
def limpar_campos():
    id_entry.config(state="normal")
    id_entry.delete(0, tk.END)
    id_entry.config(state="readonly")
    nome_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    nascimento_entry.delete(0, tk.END)

# Evento para selecionar um contato na Treeview e preencher os campos
def selecionar_contato(event):
    item = tree.selection()
    if item:
        dados = tree.item(item)["values"]
        # Atualiza o campo ID (read-only)
        id_entry.config(state="normal")
        id_entry.delete(0, tk.END)
        id_entry.insert(0, dados[0])
        id_entry.config(state="readonly")
        # Atualiza os demais campos
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, dados[1])
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, dados[2])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, dados[3])
        nascimento_entry.delete(0, tk.END)
        nascimento_entry.insert(0, dados[4])

# Criando a interface gráfica
root = tk.Tk()
root.title("Agenda Telefônica")
root.geometry("750x500")

# Linha para o campo ID (incluso para atualização e deleção)
tk.Label(root, text="ID").grid(row=0, column=0, padx=5, pady=5)
id_entry = tk.Entry(root, state="readonly")  # Campo somente para leitura
id_entry.grid(row=0, column=1, padx=5, pady=5)

# Linha para o Nome
tk.Label(root, text="Nome").grid(row=1, column=0, padx=5, pady=5)
nome_entry = tk.Entry(root)
nome_entry.grid(row=1, column=1, padx=5, pady=5)

# Linha para o Telefone
tk.Label(root, text="Telefone").grid(row=2, column=0, padx=5, pady=5)
telefone_entry = tk.Entry(root)
telefone_entry.grid(row=2, column=1, padx=5, pady=5)

# Linha para o Email
tk.Label(root, text="Email").grid(row=3, column=0, padx=5, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=3, column=1, padx=5, pady=5)

# Linha para a Data de Nascimento
tk.Label(root, text="Data Nasc (YYYY-MM-DD)").grid(row=4, column=0, padx=5, pady=5)
nascimento_entry = tk.Entry(root)
nascimento_entry.grid(row=4, column=1, padx=5, pady=5)

# Botões de ação
tk.Button(root, text="Inserir", command=inserir_contato).grid(row=5, column=0, padx=5, pady=10)
tk.Button(root, text="Atualizar", command=atualizar_contato).grid(row=5, column=1, padx=5, pady=10)
tk.Button(root, text="Deletar", command=deletar_contato).grid(row=5, column=2, padx=5, pady=10)
tk.Button(root, text="Limpar", command=limpar_campos).grid(row=5, column=3, padx=5, pady=10)

# Treeview para exibir os contatos
colunas = ("id", "nome", "telefone", "email", "data_nascimento")
tree = ttk.Treeview(root, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col.capitalize())
tree.grid(row=6, column=0, columnspan=4, padx=5, pady=10)

# Vincula o evento de seleção para preencher os campos
tree.bind("<<TreeviewSelect>>", selecionar_contato)

listar_contatos()
root.mainloop()
