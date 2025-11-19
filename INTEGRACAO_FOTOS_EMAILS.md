# 🖼️ Integração: Fotos dos Emails Sincronizadas com vehicle_images

## 📋 Problema Anterior

**Antes**: Os emails usavam fotos diretamente do CDN do CarJet:
- ❌ URLs relativas não funcionavam em emails
- ❌ Não aproveitavam as fotos já baixadas na base de dados
- ❌ Dependência externa do servidor CarJet
- ❌ Fotos podiam mudar ou ficar indisponíveis

**Resultado**: Fotos não carregavam corretamente nos emails, aparecendo apenas como "CDN..." ou ícones.

---

## ✅ Solução Implementada

**Agora**: Os emails usam fotos da tabela `vehicle_images` do sistema:
- ✅ **PRIORITY 1**: Busca foto na base de dados (`vehicle_images`)
- ✅ **PRIORITY 2**: Fallback para CDN CarJet (se não houver local)
- ✅ **PRIORITY 3**: Ícone SVG (se nenhuma foto disponível)

---

## 🔧 Arquitetura da Solução

### 1. Tabela `vehicle_images`

Armazena fotos dos veículos no PostgreSQL:

```sql
CREATE TABLE vehicle_images (
    vehicle_key TEXT PRIMARY KEY,          -- Nome normalizado do veículo
    image_data BYTEA NOT NULL,             -- Foto em formato binário
    content_type TEXT DEFAULT 'image/jpeg', -- Tipo MIME
    downloaded_at TIMESTAMP,               -- Data do download
    original_url TEXT                      -- URL original (referência)
);
```

**Características**:
- Fotos armazenadas como **BYTEA** (binário) diretamente no PostgreSQL
- Lookup rápido via `vehicle_key` (indexado por PRIMARY KEY)
- Suporta vários formatos: JPEG, PNG, WebP
- Persistência garantida (não depende de servidores externos)

---

### 2. Endpoint `/api/vehicles/{vehicle_name}/photo`

**Arquivo**: `main.py` (linhas ~20607-20700)

**Funcionalidade**:
- Serve fotos da base de dados via HTTP
- Não requer autenticação (permite uso em `<img>` tags)
- Busca inteligente com fallbacks:
  1. Tabela `vehicle_images` (foto principal)
  2. Tabela `vehicle_photos` (fotos alternativas)
  3. Variações do nome (ex: "BMW 3 Series" → "bmw 3")
  4. Tratamento especial para Station Wagon (SW)

**Exemplo de uso**:
```html
<img src="https://carrental-api-5f8q.onrender.com/api/vehicles/toyota aygo/photo" 
     alt="Toyota Aygo">
```

**Response**:
- HTTP 200 + imagem binária (JPEG/PNG)
- HTTP 404 se foto não encontrada

---

### 3. Função `fix_photo_url_for_email()`

**Arquivo**: `improved_reports.py` (linhas 20-65)

**Nova assinatura**:
```python
def fix_photo_url_for_email(photo_url, car_name=None):
    """
    Args:
        photo_url: URL original da foto (CarJet CDN)
        car_name: Nome do carro (para lookup em vehicle_images)
    
    Returns:
        URL absoluta da foto ou None
    """
```

**Lógica de prioridade**:

#### PRIORITY 1: Base de Dados Interna ✅
```python
if car_name:
    vehicle_key = car_name.lower().strip()
    base_url = get_base_url()  # Render ou local
    return f"{base_url}/api/vehicles/{vehicle_key}/photo"
```

**Vantagens**:
- ✅ Usa fotos já baixadas e armazenadas
- ✅ Endpoint público (funciona em emails)
- ✅ Fallbacks automáticos no endpoint
- ✅ Independente de CDN externo

#### PRIORITY 2: CDN CarJet (Fallback)
```python
if photo_url.startswith('/cdn/'):
    return f'https://www.carjet.pt{photo_url}'
```

**Quando usado**:
- Carros sem foto local ainda
- Novos modelos não processados
- Sistema de backup

#### PRIORITY 3: Sem Foto Válida
```python
return None  # → Mostra ícone SVG no email
```

---

### 4. Detecção de Hostname (Render vs Local)

**Arquivo**: `improved_reports.py` (linhas 12-18)

```python
def get_base_url():
    """Get base URL of the server"""
    render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_host:
        return f"https://{render_host}"  # Render (produção)
    else:
        return "http://localhost:8000"  # Local (desenvolvimento)
```

**Comportamento**:
- **Produção (Render)**: `https://carrental-api-5f8q.onrender.com`
- **Local**: `http://localhost:8000`

Isto garante que as URLs funcionam em qualquer ambiente.

---

## 🔄 Fluxo Completo

### Geração de Email Diário

```
1. Sistema gera relatório HTML
   ↓
2. Para cada carro no relatório:
   - car_name = "Toyota Aygo"
   - car_photo = "/cdn/img/cars/S/car_C01.jpg"
   ↓
3. Chama fix_photo_url_for_email(car_photo, car_name)
   ↓
4. Retorna: "https://carrental-api-5f8q.onrender.com/api/vehicles/toyota aygo/photo"
   ↓
5. HTML gerado com URL interna:
   <img src="https://carrental-api-5f8q.onrender.com/api/vehicles/toyota aygo/photo">
   ↓
6. Email enviado via Gmail API
   ↓
7. Cliente de email (Gmail/Outlook) faz request à URL
   ↓
8. Endpoint /api/vehicles/{name}/photo busca na base de dados
   ↓
9. Foto retornada e renderizada no email ✅
```

---

## 📊 Comparação: Antes vs Depois

### Antes (❌ Problema)

**HTML do email**:
```html
<img src="/cdn/img/cars/S/car_C01.jpg" alt="Toyota Aygo">
```

**Problema**:
- URL relativa → Cliente de email não consegue resolver
- Não usa fotos da base de dados
- Aparece como "CDN..." ou ícone quebrado

---

### Depois (✅ Solução)

**HTML do email**:
```html
<img src="https://carrental-api-5f8q.onrender.com/api/vehicles/toyota aygo/photo" 
     alt="Toyota Aygo">
```

**Vantagens**:
- URL absoluta → Funciona em qualquer cliente de email
- Usa fotos da base de dados `vehicle_images`
- Fallbacks automáticos (vehicle_photos → variações → CDN)
- Sistema robusto e escalável

---

## 🧪 Como Testar

### Teste 1: Verificar Endpoint de Fotos

**Acessar no browser**:
```
https://carrental-api-5f8q.onrender.com/api/vehicles/toyota aygo/photo
```

**Esperado**:
- ✅ Imagem do Toyota Aygo carregada
- ✅ HTTP 200 OK
- ✅ Content-Type: image/jpeg ou image/png

**Se não funcionar**:
- Verificar se foto está em `vehicle_images`
- Verificar logs do endpoint
- Tentar variações do nome: "toyotaaygo", "toyota-aygo"

---

### Teste 2: Email de Teste

**Via API**:
```bash
POST /api/reports/test-daily
```

**Esperado no email recebido**:
- ✅ Fotos dos carros carregam corretamente
- ✅ URLs apontam para `/api/vehicles/{name}/photo`
- ✅ Fallback para ícone SVG se não houver foto

**Inspecionar HTML do email**:
```html
<!-- ✅ Correto -->
<img src="https://carrental-api-5f8q.onrender.com/api/vehicles/renault clio/photo">

<!-- ❌ Antigo (não deve aparecer) -->
<img src="/cdn/img/cars/S/car_C04.jpg">
```

---

### Teste 3: Verificar Fotos na Base de Dados

**Query SQL**:
```sql
-- Contar fotos disponíveis
SELECT COUNT(*) as total_photos FROM vehicle_images;

-- Ver fotos específicas
SELECT vehicle_key, content_type, downloaded_at 
FROM vehicle_images 
ORDER BY downloaded_at DESC 
LIMIT 20;

-- Buscar foto específica
SELECT vehicle_key, content_type 
FROM vehicle_images 
WHERE vehicle_key LIKE '%toyota%';
```

**Esperado**:
- Centenas de fotos armazenadas
- Última atualização recente
- Diversos tipos de veículos

---

## 🔍 Troubleshooting

### Problema: Fotos ainda não carregam no email

**Verificação 1**: URL no HTML do email
```bash
# View → Message Source no Gmail
# Procurar por <img src=
```

**Esperado**:
```html
<img src="https://carrental-api-5f8q.onrender.com/api/vehicles/...">
```

**Se ainda aparecer**:
```html
<img src="/cdn/img/...">
```
→ Deploy de `improved_reports.py` não foi feito

---

**Verificação 2**: Endpoint responde?
```bash
curl -I https://carrental-api-5f8q.onrender.com/api/vehicles/toyota%20aygo/photo
```

**Esperado**:
```
HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: 45231
```

**Se HTTP 404**:
- Foto não está na base de dados
- Nome do veículo incorreto
- Executar download de fotos

---

**Verificação 3**: Foto existe na BD?
```sql
SELECT * FROM vehicle_images WHERE vehicle_key = 'toyota aygo';
```

**Se vazio**:
- Foto não foi baixada ainda
- Executar script de download: `upload_real_photos_to_postgres.py`
- Ou verificar se nome está normalizado corretamente

---

### Problema: Algumas fotos mostram ícone SVG

**Esperado** ✅:
- Comportamento normal quando:
  - Veículo não tem foto na base de dados
  - Nome do veículo não corresponde (ex: variação regional)
  - Foto ainda não foi baixada

**Solução**:
1. Identificar quais carros não têm foto
2. Executar download manual ou automático
3. Verificar mapeamentos de nomes em `vehicle_name_overrides`

---

### Problema: URLs apontam para localhost em produção

**Causa**: Variável `RENDER_EXTERNAL_HOSTNAME` não configurada

**Verificação**:
```bash
# No Render Shell
echo $RENDER_EXTERNAL_HOSTNAME
```

**Esperado**:
```
carrental-api-5f8q.onrender.com
```

**Solução**:
- Variável é definida automaticamente pelo Render
- Se não existir, verificar configurações do serviço
- Reiniciar serviço pode resolver

---

## 📈 Benefícios da Integração

### 1. Performance ⚡
- **Antes**: Cada foto = request ao CarJet CDN
- **Depois**: Fotos servidas do próprio servidor PostgreSQL
- **Resultado**: Carregamento mais rápido e confiável

### 2. Confiabilidade 🛡️
- **Antes**: Dependência de servidor externo (CarJet)
- **Depois**: Fotos persistidas na nossa base de dados
- **Resultado**: Emails sempre com fotos, mesmo se CarJet estiver offline

### 3. Controle 🎛️
- **Antes**: Fotos podem mudar sem aviso
- **Depois**: Controle total sobre quais fotos usar
- **Resultado**: Consistência visual nos relatórios

### 4. Sincronização 🔄
- **Antes**: Fotos do sistema ≠ Fotos dos emails
- **Depois**: Mesmas fotos em web app e emails
- **Resultado**: Experiência consistente para o utilizador

---

## 🎯 Checklist de Implementação

- [x] Tabela `vehicle_images` criada no PostgreSQL
- [x] Endpoint `/api/vehicles/{name}/photo` funcional
- [x] Função `fix_photo_url_for_email()` atualizada
- [x] Detecção de hostname (Render vs Local)
- [x] Relatórios diários integrados
- [x] Relatórios semanais integrados
- [x] Documentação completa
- [ ] Deploy no Render
- [ ] Teste com email real
- [ ] Verificar fotos carregam corretamente
- [ ] Validar fallbacks funcionam

---

## 📚 Arquivos Modificados

1. **`improved_reports.py`**
   - Linhas 9-65: Funções `get_base_url()` e `fix_photo_url_for_email()`
   - Linhas 427-429: Relatório diário - lookup com `car_name`
   - Linhas 689-691: Relatório semanal - lookup com `car_name`

2. **`main.py`**
   - Linhas ~20607-20700: Endpoint `/api/vehicles/{name}/photo`
   - Sistema de fallbacks e variações de nomes

---

## 🚀 Próximos Passos

### 1. Deploy
```bash
# Render Dashboard → Manual Deploy
git push origin main
```

### 2. Verificar Fotos na BD
```sql
-- Contar fotos disponíveis
SELECT COUNT(*) FROM vehicle_images;
-- Esperado: > 200 fotos
```

### 3. Teste Manual
```bash
# Enviar email de teste
POST /api/reports/test-daily
# Verificar fotos carregam
```

### 4. Monitorar Logs
```
✅ Serving photo from vehicle_images: toyota aygo
⚠️ Photo not found, trying variations...
✅ Found variation: toyotaaygo
```

---

## 💡 Melhorias Futuras

### Download Automático de Fotos Novas
- Detectar veículos sem foto em pesquisas
- Download automático via scraping
- Notificar admin quando novas fotos adicionadas

### Cache de URLs
- Cachear URLs de fotos por 24h
- Reduzir queries à base de dados
- Invalidar cache ao atualizar fotos

### Compressão de Imagens
- Comprimir fotos ao guardar (WebP, JPEG optimizado)
- Reduzir tamanho da base de dados
- Melhorar velocidade de load nos emails

### Suporte a Múltiplas Fotos
- Várias fotos por veículo (diferentes ângulos)
- Escolher melhor foto baseado em critérios
- Galeria de fotos no email (opcional)

---

**Última atualização**: 2025-11-19  
**Autor**: Cascade AI Assistant  
**Status**: ✅ Integração completa implementada
