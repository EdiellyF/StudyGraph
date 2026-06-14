# StudyGraph - Guia de Configuração Completo

## 📋 Visão Geral

StudyGraph é uma rede social educacional que permite que estudantes compartilhem conhecimento, conectem-se com colegas e explorem conteúdo educacional. A aplicação foi completamente finalizada com todas as funcionalidades essenciais.

## 🚀 Funcionalidades Implementadas

### Autenticação e Perfil
- ✅ Registro e login de usuários
- ✅ Gerenciamento de perfil pessoal
- ✅ Visualização de perfis de outros usuários
- ✅ Edição de bio e informações acadêmicas
- ✅ Deleção de conta

### Rede Social
- ✅ Criar, editar e deletar posts
- ✅ Curtir e descurtir posts
- ✅ Comentar em posts
- ✅ Deletar comentários
- ✅ Seguir e deixar de seguir usuários
- ✅ Contadores de seguidores e seguindo

### Descoberta
- ✅ Feed de posts de usuários seguidos
- ✅ Explorar e buscar usuários
- ✅ Sugestões de usuários para seguir
- ✅ Busca por nome, instituição e curso

### Salvos e Notificações
- ✅ Salvar posts favoritos
- ✅ Visualizar posts salvos
- ✅ Sistema de notificações
- ✅ Marcar notificações como lidas

### Configurações
- ✅ Gerenciar preferências de conta
- ✅ Atualizar informações de perfil
- ✅ Logout seguro

## 🛠️ Requisitos

### Backend
- Python 3.8+
- MongoDB (local ou Atlas)
- pip (gerenciador de pacotes Python)

### Frontend
- Node.js 20.19.0+ ou 22.12.0+
- npm ou pnpm

## 📦 Instalação

### 1. Clonar o Repositório

```bash
git clone <seu-repositorio>
cd StudyGraph
```

### 2. Configurar o Backend

#### 2.1 Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 Configurar Variáveis de Ambiente

Criar arquivo `.env` baseado em `.env.example`:

```bash
cp .env.example .env
```

Editar `.env` com suas credenciais:

```env
SECRET_KEY=sua_chave_secreta_aqui
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/studygraph?retryWrites=true&w=majority
MONGO_DB=studygraph
```

**Nota sobre MongoDB:**
- Para desenvolvimento local: `mongodb://localhost:27017/studygraph`
- Para produção: Use MongoDB Atlas (https://www.mongodb.com/cloud/atlas)

#### 2.3 Executar o Backend

```bash
python main.py
# ou
uvicorn main:app --reload
```

O backend estará disponível em `http://localhost:8000`

### 3. Configurar o Frontend

#### 3.1 Instalar Dependências

```bash
cd ../frontend
npm install
# ou
pnpm install
```

#### 3.2 Configurar Variáveis de Ambiente

Criar arquivo `.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

#### 3.3 Executar o Frontend

```bash
npm run dev
# ou
pnpm dev
```

O frontend estará disponível em `http://localhost:5173`

## 🧪 Testando a Aplicação

### 1. Criar Conta
- Acesse `http://localhost:5173/register`
- Preencha os dados (nome, email, senha, instituição, curso, semestre)
- Clique em "Registrar"

### 2. Fazer Login
- Acesse `http://localhost:5173/login`
- Use as credenciais criadas
- Será redirecionado para o feed

### 3. Testar Funcionalidades

**Feed:**
- Criar um novo post
- Curtir/descurtir posts
- Adicionar comentários
- Salvar posts

**Explorar:**
- Buscar por usuários
- Seguir usuários sugeridos
- Ver perfis de outros usuários

**Perfil:**
- Editar bio e informações
- Ver posts pessoais
- Gerenciar seguidores

**Configurações:**
- Atualizar informações de perfil
- Gerenciar preferências
- Fazer logout

## 📁 Estrutura do Projeto

```
StudyGraph/
├── backend/
│   ├── main.py              # API FastAPI principal
│   ├── requirements.txt      # Dependências Python
│   └── .env.example         # Exemplo de variáveis de ambiente
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes Vue reutilizáveis
│   │   ├── views/           # Páginas da aplicação
│   │   ├── stores/          # Stores Pinia (estado global)
│   │   ├── router/          # Configuração do Vue Router
│   │   ├── assets/          # Estilos e assets
│   │   └── App.vue          # Componente raiz
│   ├── package.json         # Dependências Node.js
│   ├── vite.config.js       # Configuração Vite
│   └── tailwind.config.js   # Configuração Tailwind CSS
└── README.md                # Este arquivo
```

## 🔌 Endpoints da API

### Autenticação
- `POST /register` - Registrar novo usuário
- `POST /login` - Fazer login

### Perfil
- `GET /profile/me` - Obter perfil do usuário logado
- `GET /profile/{user_id}` - Obter perfil de outro usuário
- `PUT /profile/me` - Atualizar perfil
- `DELETE /profile/me` - Deletar conta

### Posts
- `POST /posts` - Criar post
- `GET /posts` - Listar posts
- `DELETE /posts/{post_id}` - Deletar post
- `POST /posts/{post_id}/like` - Curtir post
- `DELETE /posts/{post_id}/like` - Descurtir post
- `POST /posts/{post_id}/save` - Salvar post
- `DELETE /posts/{post_id}/save` - Remover salvos
- `GET /saved-posts` - Listar posts salvos

### Comentários
- `POST /posts/{post_id}/comments` - Criar comentário
- `GET /posts/{post_id}/comments` - Listar comentários
- `DELETE /comments/{comment_id}` - Deletar comentário

### Usuários
- `GET /users/search` - Buscar usuários
- `GET /users/suggested` - Obter sugestões de usuários
- `POST /users/{user_id}/follow` - Seguir usuário
- `DELETE /users/{user_id}/follow` - Deixar de seguir

### Notificações
- `GET /notifications` - Listar notificações
- `PUT /notifications/{notification_id}/read` - Marcar como lida

## 🎨 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Motor** - Driver assíncrono para MongoDB
- **PyJWT** - Autenticação com JWT
- **Passlib + Bcrypt** - Hash seguro de senhas
- **Pydantic** - Validação de dados

### Frontend
- **Vue 3** - Framework JavaScript progressivo
- **Vue Router** - Roteamento de aplicação
- **Pinia** - Gerenciamento de estado
- **Tailwind CSS** - Utilitários CSS
- **Vite** - Build tool rápido

## 🔐 Segurança

- Senhas são hasheadas com bcrypt
- Autenticação via JWT
- CORS configurado para aceitar localhost
- Validação de entrada com Pydantic
- Proteção de rotas no frontend

## 🚨 Troubleshooting

### Erro: "MONGO_URI não encontrada"
- Verifique se o arquivo `.env` existe no diretório backend
- Confirme que `MONGO_URI` está definida corretamente

### Erro: "Connection refused" ao conectar ao MongoDB
- Verifique se MongoDB está rodando
- Para MongoDB local: `mongod` deve estar em execução
- Para MongoDB Atlas: Verifique a string de conexão

### Erro: "Port already in use"
- Backend: Mude a porta com `uvicorn main:app --port 8001`
- Frontend: Mude a porta em `vite.config.js`

### Frontend não conecta ao backend
- Verifique se `VITE_API_URL` está correto em `.env.local`
- Confirme que o backend está rodando
- Verifique CORS no backend

## 📝 Próximos Passos para Produção

1. **Variáveis de Ambiente:**
   - Use variáveis de ambiente seguras
   - Nunca commite `.env` no Git

2. **Banco de Dados:**
   - Use MongoDB Atlas para produção
   - Configure backups automáticos

3. **Deploy:**
   - Backend: Heroku, Railway, Render
   - Frontend: Vercel, Netlify, GitHub Pages

4. **SSL/HTTPS:**
   - Configure certificados SSL
   - Use HTTPS em produção

5. **Monitoramento:**
   - Configure logging
   - Use ferramentas de monitoramento

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação FastAPI: https://fastapi.tiangolo.com
2. Verifique a documentação Vue: https://vuejs.org
3. Consulte a documentação MongoDB: https://docs.mongodb.com

## 📄 Licença

Este projeto está sob licença MIT.

---

**Desenvolvido com ❤️ para a comunidade educacional**
