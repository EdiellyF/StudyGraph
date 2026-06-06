# 🚀 Guia de Teste - StudyGraph

## 📊 Resumo da Implementação

Você solicitou **duas telas principais** + **ProfileView** para uma rede social acadêmica. Tudo foi implementado com sucesso! 

---

## ✅ Arquivos Criados/Modificados

### **Frontend - Vue 3**

#### **Criados:**
- ✨ `frontend/src/components/LoginForm.vue` — Layout 2 colunas minimalista com design vinho/creme
- ✨ `frontend/src/views/ProfileView.vue` — Perfil completo com stats, posts e follow

#### **Refatorados:**
- 🔄 `frontend/src/views/LoginView.vue` — Agora usa `LoginForm.vue` (era `AuthForm.vue`)
- 🔄 `frontend/src/views/FeedView.vue` — Completado com todos os handlers

#### **Validados/Existentes:**
- ✅ `frontend/src/components/RegisterForm.vue` — Layout 2 colunas (já estava pronto!)
- ✅ `frontend/src/components/AppShell.vue` — Sidebar + TopBar (funcionando)
- ✅ `frontend/src/stores/auth.js` — JWT authentication (completo)
- ✅ `frontend/src/stores/posts.js` — CRUD de posts (completo)

### **Backend - FastAPI**

#### **Endpoints Novos Adicionados:**
- ➕ `POST /users/{user_id}/follow` — Seguir usuário com validações
- ➕ `DELETE /users/{user_id}/follow` — Deseguir usuário
- ➕ `GET /posts?user_id={user_id}` — Filtrar posts por usuário

#### **Validados/Existentes:**
- ✅ `POST /register` + `POST /login` — Autenticação JWT
- ✅ `GET /profile/me` + `PUT /profile/me` — Perfil do usuário
- ✅ `GET /profile/{user_id}` — Perfil público
- ✅ `POST /posts` + `GET /posts` — CRUD de posts
- ✅ `GET /users/suggested` — Usuários para seguir

---

## 🎨 Design Implementado

### **Paleta de Cores (conforme solicitado)**
```
Bege/Creme:     #F5F0E8  → Fundos principais
Roxo/Vinho:     #4A2C39  → Painéis de destaque, headers
Malva/Rosa:     #C4A4A4  → Botões, detalhe
Rosa Claro:     #D4A5A5  → Texto secundário
```

### **Componentes Visuais**
- ✅ Bordas arredondadas suaves (`rounded-lg`, `rounded-xl`, `rounded-2xl`)
- ✅ Sombras sutis (`shadow-sm`, `shadow-md`)
- ✅ Layout minimalista com espaçamento generoso
- ✅ 2 colunas para Register/Login (responsive)
- ✅ AppShell para Feed/Profile (sidebar + main)

---

## 🧪 Como Testar (Passo a Passo)

### **Pré-requisitos**
- ✅ Node.js 18+ instalado
- ✅ Python 3.8+ instalado
- ✅ MongoDB rodando (ou MongoDB Atlas configurado)
- ✅ Variáveis de ambiente (.env) já existem no projeto

### **PASSO 1: Iniciar Backend**

**Terminal 1** (deixe rodando)
```bash
cd c:\Users\Edielly\Documents\IFTO\StudyGraph\StudyGraph\backend
python -m uvicorn main:app --reload
```

✅ Esperado:
```
INFO:     Started server process [...]
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### **PASSO 2: Iniciar Frontend**

**Terminal 2** (deixe rodando)
```bash
cd c:\Users\Edielly\Documents\IFTO\StudyGraph\StudyGraph\frontend
npm run dev
```

✅ Esperado:
```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

### **PASSO 3: Testar o Fluxo Completo**

Abra o navegador em **http://localhost:5173**

---

## 📱 TESTE 1: PÁGINA DE CADASTRO (RegisterView)

**URL:** http://localhost:5173/register

**Validar:**
```
┌─────────────────────────────────────────────┐
│ ESQUERDA (1/3)     │  DIREITA (2/3)         │
│ ─────────────────  │  ──────────────────    │
│ Fundo VINHO        │  Fundo CREME           │
│                    │                        │
│ "Conecte-se ao     │  FORM:                 │
│  conhecimento"     │  ┌──────────────────┐  │
│                    │  │ Criar conta      │  │
│ 📚 10k+ estudantes │  ├──────────────────┤  │
│ 🎓 50+ instituições│  │ Nome             │  │
│ 💡 5k+ posts       │  │ Semestre         │  │
│                    │  │ E-mail           │  │
│                    │  │ Instituição      │  │
│                    │  │ Curso            │  │
│                    │  │ Senha (força)    │  │
│                    │  │ ▮▮▮ VERDE (forte)│  │
│                    │  │                  │  │
│                    │  │ [CADASTRAR]      │  │
│                    │  │                  │  │
│                    │  │ Já tem conta?    │  │
│                    │  │ → Faça login     │  │
│                    │  └──────────────────┘  │
└─────────────────────────────────────────────┘
```

**Teste:**
1. Preencher formulário:
   - Nome: `João Silva`
   - Semestre: `4º semestre`
   - E-mail: `joao.silva@ifto.edu.br`
   - Instituição: `IFTO`
   - Curso: `Sistemas de Informação`
   - Senha: `Senha@123` (vê a força mudar: vermelho → verde)

2. Clicar **"Cadastrar"**

✅ Esperado:
- Token JWT salvo em localStorage
- Redirecionado para `/feed`
- Sem erros no console

❌ Se erro "Email já cadastrado":
- Usar outro e-mail (email@test.com, etc.)

---

## 📰 TESTE 2: FEED/DASHBOARD (FeedView com AppShell)

**URL:** http://localhost:5173/feed (automático após login)

**Layout Esperado:**
```
┌────────────────────────────────────────────────────────────────┐
│ StudyGraph  [🔍 Buscar...]        [🔔 Notif]  [👤 Avatar]     │
├────────────────────────────────────────────────────────────────┤
│  SIDEBAR      │  MAIN CONTENT              │  SUGESTÕES        │
│  ─────────    │  ──────────────────────    │  ──────────       │
│ 📰 Feed       │  ┌─────────────────────┐   │ 💡 Sugeridos p/   │
│ 🔍 Explorar   │  │ Criar Post:         │   │ você             │
│ 🔔 Notif.     │  │ [👤] Compartilhe    │   │ ─────────────    │
│ 🔖 Salvos     │  │ conhecimento...      │   │ ┌──────────────┐ │
│ ⚙️ Ajustes    │  │ [Fotos] [Links]     │   │ │ 👤 User 1    │ │
│              │  │ ────────────────    │   │ │ 📍 Instituição│ │
│ ┌──────────┐ │  │ [PUBLICAR]         │   │ │ [SEGUIR]     │ │
│ │👤 João   │ │  │ └─────────────────┘ │   │ └──────────────┘ │
│ │ @joaosilva   │ │                       │   │               │
│ │[SAIR]    │ │  │ Posts:              │   │ ┌──────────────┐ │
│ └──────────┘ │  │ ┌─────────────────┐ │   │ │ 👤 User 2    │ │
│              │  │ │ João · 2h       │ │   │ │ 📍 Instituição│ │
│              │  │ │ Olá pessoal!    │ │   │ │ [SEGUIR]     │ │
│              │  │ │ ❤️ 5 💬 2 🔖    │ │   │ └──────────────┘ │
│              │  │ └─────────────────┘ │   │               │
│              │  │ ┌─────────────────┐ │   └──────────────────┘
│              │  │ │ outro post      │ │   
│              │  │ │ ❤️ 3 💬 1 🔖    │ │
│              │  │ └─────────────────┘ │
│              │  └───────────────────────┘
└────────────────────────────────────────────────────────────────┘
```

**Teste:**

### A. **Criar Post**
1. Digitar no textarea: `Olá pessoal! Este é meu primeiro post 👋`
2. Clicar **"Publicar"**

✅ Esperado:
- Loading state: botão muda para "Publicando..."
- Post aparece no topo da lista em tempo real
- Textarea limpa

### B. **Seguir Usuário**
1. Na seção "Sugeridos para você" (direita), clicar **"[SEGUIR]"**

✅ Esperado:
- POST `/users/{userId}/follow` executado
- Usuário removido da lista de sugestões
- Botão muda visualmente (confirmação)

### C. **Observar Loading**
1. Ao carregar a página, você vê "Carregando posts..." brevemente
2. Posts aparecem dinamicamente

---

## 👤 TESTE 3: PERFIL DE USUÁRIO (ProfileView)

**URL:** http://localhost:5173/profile

**Layout Esperado:**
```
┌──────────────────────────────────────────────────┐
│  SIDEBAR  │  PROFILE VIEW                        │
├──────────────────────────────────────────────────┤
│           │ ┌────────────────────────────────┐   │
│           │ │ 👤  JOÃO SILVA                 │   │
│           │ │ @joaosilva                     │   │
│           │ │ Sem descrição adicionada.      │   │
│           │ │ IFTO • Sistemas de Informação │   │
│           │ │                [EDITAR PERFIL] │   │
│           │ └────────────────────────────────┘   │
│           │                                       │
│           │ ┌──────────┬──────────┬──────────┐   │
│           │ │    5    │    12   │     3    │   │
│           │ │  Posts  │Seguidores│Seguindo │   │
│           │ └──────────┴──────────┴──────────┘   │
│           │                                       │
│           │ POSTS:                                │
│           │ ┌────────────────────────────────┐   │
│           │ │ João · 2h                      │   │
│           │ │ Olá pessoal! Este é meu       │   │
│           │ │ primeiro post 👋              │   │
│           │ │ ❤️ 5  💬 2  🔖                │   │
│           │ └────────────────────────────────┘   │
│           │                                       │
│           │ ┌────────────────────────────────┐   │
│           │ │ João · 1h                      │   │
│           │ │ Estudando React!               │   │
│           │ │ ❤️ 3  💬 1  🔖                │   │
│           │ └────────────────────────────────┘   │
│           │                                       │
└──────────────────────────────────────────────────┘
```

**Teste:**

### A. **Editar Bio**
1. Clicar **"[EDITAR PERFIL]"**
2. Textarea aparece: `Adicione uma bio...`
3. Digitar: `Estudante de SI apaixonado por tecnologia 💻`
4. Clicar **"[SALVAR]"**

✅ Esperado:
- Bio é enviada (PUT `/profile/me`)
- Bio aparece salva no header
- Botão volta a "Editar Perfil"

### B. **Ver Posts**
- Verificar que posts do usuário estão listados
- Cada post mostra: autor, conteúdo, data, interações (❤️ 💬 🔖)

### C. **Stats**
- Verificar contadores: Posts, Seguidores, Seguindo
- Devem estar corretos baseado nas ações realizadas

---

## 🔑 TESTE 4: LOGIN

**URL:** http://localhost:5173/login

**Layout Esperado:** (Mesma estrutura 2 colunas do Register, mas com título "Bem-vindo de volta")

**Teste:**
1. Clicar link "Faça login" em qualquer place (ou clicar "Sair" no sidebar)
2. Preencher:
   - E-mail: `joao.silva@ifto.edu.br`
   - Senha: `Senha@123`
3. Clicar **"[ENTRAR]"**

✅ Esperado:
- Token JWT salvo em localStorage
- Redirecionado para `/feed`
- Usuário está autenticado

---

## 🎨 TESTE 5: Design & Responsividade

### **Cores (Verificar Paleta)**
```
✅ Bege/Creme (#F5F0E8)     → Fundos principais
✅ Roxo/Vinho (#4A2C39)    → Sidebar, headers, painéis
✅ Malva (#C4A4A4)         → Botões "Seguir", "Publicar"
✅ Rosa (#D4A5A5)          → Texto secundário
```

### **Bordas & Sombras**
- ✅ Bordas suaves: `rounded-lg`, `rounded-xl`, `rounded-2xl`
- ✅ Sombras sutis: `shadow-sm`, `shadow-md`
- ✅ Espaçamento arejado

### **Responsividade**
1. Abrir DevTools (F12)
2. Ativar "Device Toolbar" (mobile)
3. Testar no tamanho `iphone 12` (390px)

✅ Esperado:
- Sidebar collapsa ou desaparece
- Content se adapta
- 2 colunas stackam verticalmente

---

## 🔍 Validação Técnica (DevTools)

### **LocalStorage**
1. Abrir DevTools → Application → LocalStorage
2. Procurar por chave: `studygraph_token`

✅ Esperado: Token JWT presente após login

### **Network**
1. Abrir DevTools → Network
2. Criar post
3. Procurar por requisição POST `/posts`

✅ Esperado:
- Header: `Authorization: Bearer {token}`
- Status: 201 (sucesso)
- Response: Post criado com ID, timestamp, etc.

### **Console**
✅ Esperado: Sem erros (exceto avisos do Vite)

---

## 📊 Checklist de Validação

```
REGISTRO:
  [ ] Formulário com 2 colunas
  [ ] Validação de e-mail
  [ ] Indicador de força de senha
  [ ] Cadastro bem-sucedido
  [ ] Redirecionamento para /feed

LOGIN:
  [ ] Formulário com 2 colunas
  [ ] Login bem-sucedido
  [ ] Token salvo em localStorage
  [ ] Redirecionamento para /feed

FEED:
  [ ] AppShell carregado (sidebar + topbar)
  [ ] Posts listados com loading state
  [ ] Criar post funciona
  [ ] Seguir usuário funciona
  [ ] Sugestões aparecem

PERFIL:
  [ ] Header com foto, nome, bio
  [ ] Stats exibidos corretamente
  [ ] Posts do usuário listados
  [ ] Editar bio funciona
  [ ] Seguir/Deseguir funciona

DESIGN:
  [ ] Cores corretas (vinho, creme, malva)
  [ ] Bordas suaves
  [ ] Sombras sutis
  [ ] Layout responsivo

API:
  [ ] Requisições com Bearer token
  [ ] Loading states funcionando
  [ ] Erros tratados corretamente
  [ ] localStorage persistindo token
```

---

## 🆘 Troubleshooting

### **Backend não inicia?**
```bash
# Verificar MongoDB
# Se usar MongoDB Atlas, verificar .env

# Reinstalar dependências:
pip install -r requirements.txt
```

### **Frontend não carrega posts?**
```bash
# Verificar .env VITE_API_URL
# Deve ser: http://localhost:8000

# Limpar localStorage e tentar novamente
# F12 → Application → LocalStorage → Apagar tudo
```

### **Erro "Email já cadastrado"?**
- Use outro e-mail (teste@ifto.edu.br, etc.)

### **Cors error?**
- Verificar que backend está rodando em http://127.0.0.1:8000
- Verificar .env do backend tem: `MONGO_URI` e `SECRET_KEY`

---

## 📞 Arquivos Principais

```
frontend/
  src/
    views/
      LoginView.vue           ← Refatorado ✅
      RegisterView.vue        ← Existente ✅
      FeedView.vue            ← Completado ✅
      ProfileView.vue         ← Novo ✅
    components/
      LoginForm.vue           ← Novo ✅
      RegisterForm.vue        ← Existente ✅
      AppShell.vue            ← Validado ✅
    stores/
      auth.js                 ← Validado ✅
      posts.js                ← Validado ✅
  .env                        ← Configurado ✅

backend/
  main.py                     ← Estendido ✅
  .env                        ← Verificado ✅
```

---

## 🎉 Conclusão

Tudo está pronto para teste! Os componentes seguem o design solicitado (2 colunas minimalista, paleta de cores terrosas), usam Vue 3 + Tailwind CSS, integram com FastAPI/MongoDB, e gerenciam autenticação JWT via Pinia.

**Próximas melhorias:** Like/Unlike, comentários, busca, notificações real-time, uploads de avatar.

Aproveite! 🚀
