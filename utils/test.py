import customtkinter as ctk

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("300x200")
app.title("Seletor Infinito")

opcoes = ["Início", "Configurações", "Ajuda", "Sair"]
indice = [0]  # Usamos lista para tornar mutável dentro da função

label = ctk.CTkLabel(app, text=opcoes[indice[0]], font=("Arial", 20))
label.pack(pady=40)

def proximo():
    indice[0] = (indice[0] - 1) % len(opcoes)
    label.configure(text=opcoes[indice[0]])

btn = ctk.CTkButton(app, text="Próximo", command=proximo)
btn.pack()

app.mainloop()
