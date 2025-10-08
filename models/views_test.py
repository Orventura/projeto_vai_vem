from src.bd import BancoDeDados

with BancoDeDados() as bd:
    id2_embarque = bd.gerar_id2()

    itens_embarcados = [
        ("R123", "Alimentos", "2025-09-23", "TransManaus", "CNTR456", "ABC-1234", "LCR789",
         "Manaus", "Belém", "Manhã", "João", "Setor A", "12345", "Caixa de biscoitos",
         100, "NF98765", "Transferência", "Em trânsito", "Maria", "R124", "2025-09-24",
         "Loja Belém", "14:30", "PC01"),
        ("R123", "Alimentos", "2025-09-23", "TransManaus", "CNTR456", "ABC-1234", "LCR789",
         "Manaus", "Belém", "Manhã", "João", "Setor A", "67890", "Pacote de arroz",
         50, "NF98766", "Transferência", "Em trânsito", "Maria", "R124", "2025-09-24",
         "Loja Belém", "14:30", "PC01")
    ]

    for item in itens_embarcados:
        bd.inserir_dado((id2_embarque,) + item)