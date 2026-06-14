# StudyGraph API - Documentação Completa

## 📚 Introdução

A API StudyGraph é uma API RESTful construída com FastAPI que fornece todos os endpoints necessários para gerenciar uma rede social educacional.

**URL Base:** `http://localhost:8000`

## 🔐 Autenticação

Todos os endpoints (exceto `/register` e `/login`) requerem autenticação via Bearer Token.

**Header de Autenticação:**
```
Authorization: Bearer <seu_token_jwt>
```

## 📋 Endpoints

### 1. Autenticação

#### Registrar Novo Usuário
```http
POST /register
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123",
  "semester": "6º",
  "institution": "Universidade Federal",
  "course": "Engenharia de Software"
}
```

**Resposta (201):**
```json
{
  "message": "Usuário criado com sucesso!"
}
```

**Erros:**
- `400`: Email já cadastrado

---

#### Fazer Login
```http
POST /login
Content-Type: application/json

{
  "email": "joao@example.com",
  "password": "senha123"
}
```

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erros:**
- `400`: Credenciais inválidas

---

### 2. Perfil

#### Obter Perfil do Usuário Logado
```http
GET /profile/me
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "João Silva",
  "email": "joao@example.com",
  "institution": "Universidade Federal",
  "course": "Engenharia de Software",
  "semester": "6º",
  "bio": "Apaixonado por tecnologia",
  "followersCount": 42,
  "followingCount": 15,
  "createdAt": "2024-01-15T10:30:00"
}
```

---

#### Obter Perfil de Outro Usuário
```http
GET /profile/{user_id}
Authorization: Bearer <token>
```

**Parâmetros:**
- `user_id` (string): ID do usuário

**Resposta (200):** Mesmo formato do perfil do usuário logado

**Erros:**
- `400`: ID de usuário inválido
- `404`: Usuário não encontrado

---

#### Atualizar Perfil
```http
PUT /profile/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "João Silva",
  "institution": "Universidade Federal",
  "course": "Engenharia de Software",
  "semester": "7º",
  "bio": "Desenvolvedor Full Stack"
}
```

**Resposta (200):** Perfil atualizado

**Erros:**
- `400`: Nenhum campo para atualizar

---

#### Deletar Conta
```http
DELETE /profile/me
Authorization: Bearer <token>
```

**Resposta (204):** Sem conteúdo

---

### 3. Posts

#### Criar Post
```http
POST /posts
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Acabei de aprender sobre React Hooks! Muito útil para gerenciar estado."
}
```

**Resposta (201):**
```json
{
  "id": "507f1f77bcf86cd799439012",
  "content": "Acabei de aprender sobre React Hooks!",
  "authorId": "507f1f77bcf86cd799439011",
  "authorName": "João Silva",
  "authorAvatar": null,
  "likesCount": 0,
  "commentsCount": 0,
  "createdAt": "2024-01-15T11:30:00"
}
```

**Validações:**
- `content`: Mínimo 1, máximo 2000 caracteres

---

#### Listar Posts
```http
GET /posts?user_id=507f1f77bcf86cd799439011&limit=20&skip=0
Authorization: Bearer <token>
```

**Parâmetros Query:**
- `user_id` (opcional): Filtrar por autor
- `limit` (opcional): Número de posts (padrão: 20)
- `skip` (opcional): Paginação (padrão: 0)

**Resposta (200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "content": "Meu primeiro post!",
    "authorId": "507f1f77bcf86cd799439011",
    "authorName": "João Silva",
    "authorAvatar": null,
    "likesCount": 5,
    "commentsCount": 2,
    "createdAt": "2024-01-15T11:30:00"
  }
]
```

---

#### Deletar Post
```http
DELETE /posts/{post_id}
Authorization: Bearer <token>
```

**Resposta (204):** Sem conteúdo

**Erros:**
- `400`: ID de post inválido
- `403`: Você não tem permissão para deletar este post
- `404`: Post não encontrado

---

### 4. Likes

#### Curtir Post
```http
POST /posts/{post_id}/like
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Post curtido com sucesso"
}
```

**Erros:**
- `400`: ID inválido ou já curtiu
- `404`: Post não encontrado

---

#### Descurtir Post
```http
DELETE /posts/{post_id}/like
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Like removido com sucesso"
}
```

**Erros:**
- `400`: Você não curtiu este post
- `404`: Post não encontrado

---

### 5. Comentários

#### Criar Comentário
```http
POST /posts/{post_id}/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Ótimo post! Muito útil."
}
```

**Resposta (201):**
```json
{
  "id": "507f1f77bcf86cd799439013",
  "content": "Ótimo post! Muito útil.",
  "authorId": "507f1f77bcf86cd799439011",
  "authorName": "João Silva",
  "authorAvatar": null,
  "createdAt": "2024-01-15T12:00:00"
}
```

**Validações:**
- `content`: Mínimo 1, máximo 500 caracteres

---

#### Listar Comentários
```http
GET /posts/{post_id}/comments?limit=20&skip=0
Authorization: Bearer <token>
```

**Parâmetros Query:**
- `limit` (opcional): Número de comentários (padrão: 20)
- `skip` (opcional): Paginação (padrão: 0)

**Resposta (200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439013",
    "content": "Ótimo post!",
    "authorId": "507f1f77bcf86cd799439011",
    "authorName": "João Silva",
    "authorAvatar": null,
    "createdAt": "2024-01-15T12:00:00"
  }
]
```

---

#### Deletar Comentário
```http
DELETE /comments/{comment_id}
Authorization: Bearer <token>
```

**Resposta (204):** Sem conteúdo

**Erros:**
- `403`: Você não tem permissão para deletar
- `404`: Comentário não encontrado

---

### 6. Posts Salvos

#### Salvar Post
```http
POST /posts/{post_id}/save
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Post salvo com sucesso"
}
```

---

#### Remover Post Salvo
```http
DELETE /posts/{post_id}/save
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Post removido dos salvos"
}
```

---

#### Listar Posts Salvos
```http
GET /saved-posts?limit=20&skip=0
Authorization: Bearer <token>
```

**Resposta (200):** Array de posts (mesmo formato de `/posts`)

---

### 7. Usuários

#### Buscar Usuários
```http
GET /users/search?q=engenharia&limit=10
Authorization: Bearer <token>
```

**Parâmetros Query:**
- `q` (obrigatório): Termo de busca (mínimo 2 caracteres)
- `limit` (opcional): Número de resultados (padrão: 10)

**Resposta (200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "João Silva",
    "institution": "Universidade Federal",
    "course": "Engenharia de Software",
    "followersCount": 42
  }
]
```

---

#### Obter Sugestões de Usuários
```http
GET /users/suggested?limit=5
Authorization: Bearer <token>
```

**Parâmetros Query:**
- `limit` (opcional): Número de sugestões (padrão: 5)

**Resposta (200):** Array de usuários

---

### 8. Follow

#### Seguir Usuário
```http
POST /users/{user_id}/follow
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Usuário seguido com sucesso"
}
```

**Erros:**
- `400`: Você não pode seguir a si mesmo ou já segue
- `404`: Usuário não encontrado

---

#### Deixar de Seguir
```http
DELETE /users/{user_id}/follow
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Usuário deixado de seguir com sucesso"
}
```

---

### 9. Notificações

#### Listar Notificações
```http
GET /notifications?limit=20&skip=0
Authorization: Bearer <token>
```

**Resposta (200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439014",
    "type": "like",
    "message": "curtiu seu post",
    "fromUserId": "507f1f77bcf86cd799439011",
    "fromUserName": "João Silva",
    "postId": "507f1f77bcf86cd799439012",
    "read": false,
    "createdAt": "2024-01-15T13:00:00"
  }
]
```

---

#### Marcar Notificação como Lida
```http
PUT /notifications/{notification_id}/read
Authorization: Bearer <token>
```

**Resposta (200):**
```json
{
  "message": "Notificação marcada como lida"
}
```

---

## 🔄 Fluxos de Uso

### Fluxo de Autenticação
1. Usuário se registra em `/register`
2. Usuário faz login em `/login` e recebe token
3. Token é armazenado no localStorage
4. Token é enviado em cada requisição no header `Authorization`

### Fluxo de Criação de Post
1. Usuário cria post em `/posts`
2. Post é adicionado ao feed
3. Outros usuários podem curtir, comentar e salvar
4. Autor pode deletar seu próprio post

### Fluxo de Busca e Follow
1. Usuário busca por usuários em `/users/search`
2. Usuário segue alguém em `/users/{user_id}/follow`
3. Posts do usuário seguido aparecem no feed
4. Usuário pode deixar de seguir em `/users/{user_id}/follow` (DELETE)

---

## 📊 Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 204 | No Content - Sucesso sem conteúdo na resposta |
| 400 | Bad Request - Requisição inválida |
| 401 | Unauthorized - Token inválido ou expirado |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro do servidor |

---

## 🧪 Testando a API

### Com cURL

**Registrar:**
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João",
    "email": "joao@example.com",
    "password": "senha123",
    "institution": "USP",
    "course": "Engenharia"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

**Criar Post:**
```bash
curl -X POST http://localhost:8000/posts \
  -H "Authorization: Bearer <seu_token>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Meu primeiro post!"}'
```

### Com Postman

1. Importe a coleção de endpoints
2. Configure a variável `{{token}}` após login
3. Teste cada endpoint

### Com Swagger UI

Acesse `http://localhost:8000/docs` para documentação interativa

---

## 🔒 Boas Práticas de Segurança

1. **Nunca compartilhe seu token**
2. **Use HTTPS em produção**
3. **Implemente rate limiting**
4. **Valide todas as entradas**
5. **Use variáveis de ambiente para secrets**
6. **Implemente CORS corretamente**

---

## 📝 Notas

- Todos os timestamps estão em ISO 8601
- IDs são ObjectIds do MongoDB (24 caracteres hexadecimais)
- Paginação usa `limit` e `skip`
- Buscas são case-insensitive

---

**Última atualização:** Janeiro 2024
