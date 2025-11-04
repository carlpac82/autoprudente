# 📋 GRUPOS DA CARJET - LINKS PARA DOWNLOAD

## ✅ Grupos Recebidos

### Grupo N (Pequenos)
- **Status:** ⏳ Em processamento
- **URL:** https://www.carjet.com/do/list/pt?s=36b4f78e-2eb7-4ad3-b5ad-eefba5b8a662&b=b5feeaca-db6e-48d4-9fe3-c64d86ebe199
- **Descrição:** Carros pequenos

---

## ⏳ Aguardando Links

### Grupo C (Compactos/Médios)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

### Grupo F (Familiares/Grandes)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

### Grupo S (SUVs)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

### Grupo V (Vans/Monovolumes)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

### Grupo A (Automáticos)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

### Grupo L (Luxo/Premium)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

### Grupo E (Estate/SW)
- **Status:** ⏳ Aguardando link
- **URL:** _Pendente_

---

## 📝 Instruções

Quando receber os links, adicionar ao script `download_by_groups.py` na secção `GROUPS`:

```python
GROUPS = {
    'N': {
        'name': 'Pequenos',
        'url': 'https://www.carjet.com/do/list/pt?s=...',
        'description': 'Carros pequenos'
    },
    'C': {
        'name': 'Compactos',
        'url': 'https://www.carjet.com/do/list/pt?s=...',
        'description': 'Carros médios'
    },
    # ... adicionar outros grupos
}
```

---

## 📊 Estrutura de Saída

```
carjet_photos_by_group/
├── group_N/
│   ├── C45_Fiat_Panda.jpg
│   ├── C25_Fiat_500.jpg
│   └── ...
├── group_C/
│   ├── F12_VW_Golf.jpg
│   └── ...
└── group_F/
    └── ...
```

**Ficheiro JSON:** `carjet_cars_by_groups.json`
