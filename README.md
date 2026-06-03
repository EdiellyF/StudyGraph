# 🎓 Mini Rede Social Acadêmica

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Uma rede social acadêmica de alto desempenho, projetada para entrega ágil (MVP em 13 dias) com foco rigoroso em performance (latência de leitura < 200ms). A arquitetura é 100% assíncrona, orientada a componentes e utiliza estratégias avançadas de banco de dados (Fan-out on Write e paginação por cursor).

---

## 📑 Índice

1. [Visão Geral](#-visão-geral)
2. [Stack Tecnológica](#-stack-tecnológica)
3. [Principais Funcionalidades](#-principais-funcionalidades)
4. [Arquitetura e Banco de Dados](#-arquitetura-e-banco-de-dados)
5. [Requisitos Não-Funcionais](#-requisitos-não-funcionais)
6. [Roadmap do MVP (13 Dias)](#-roadmap-do-mvp-13-dias)
7. [Como Rodar Localmente](#-como-rodar-localmente)
8. [Estrutura de Componentes UI](#-estrutura-de-componentes-ui)

---

## 👁️ Visão Geral

Este projeto visa entregar uma experiência de usuário fluida e em tempo real para o ambiente acadêmico. O diferencial técnico reside na modelagem desnormalizada do MongoDB e no uso de **Fan-out on Write** para garantir que a leitura do feed seja uma operação simples e extremamente rápida, sem a necessidade de JOINs complexos ou degradação de performance em coleções grandes.

---

## 🛠️ Stack Tecnológica

### Frontend (Interface e UX)
* **Framework Core:** Vue 3 (Composition API)
* **Estado Global:** Pinia
* **Data Fetching & Cache:** Vue Query (com mutações otimistas)
* **Roteamento:** Vue Router
* **Estilização:** Tailwind CSS
* **Real-time:** Composable customizado `useWebSocket()`

### Backend (Lógica e API)
* **Linguagem & Framework:** Python com FastAPI (Stateless)
* **Real-time:** WebSockets nativos (via Starlette)
* **Processamento Assíncrono:** Background Tasks (envio de e-mails, Fan-out do feed)
* **Segurança:** PyJWT (Access 1h / Refresh 7d) + SlowAPI (Rate limiting)

### Banco de Dados
* **Engine:** MongoDB (Modelagem desnormalizada)
* **Driver:** Motor (Driver assíncrono para Python, evitando bloqueio de I/O)
* **Hospedagem:** MongoDB Atlas (com whitelist de IPs)

### Infraestrutura e Deploy
* **Containerização:** Docker (Gunicorn/Uvicorn)
* **Frontend:** Vercel ou Netlify
* **Backend:** Railway ou Render

---

## ✨ Principais Funcionalidades

* **📝 Postagens:** Criação, edição (até 30min) e exclusão. Limite de 2.000 caracteres, upload de 1-4 imagens e preview automático de URLs.
* **❤️ Curtidas e Comentários:** Feedback visual imediato (< 100ms) via Mutação Otimista. Comentários aninhados (1 nível) com suporte a menções `@usuario`.
* **👥 Grafo Social:** Seguir/Deixar de seguir com atualização atômica de contadores (`followersCount` / `followingCount`).
* **⚡ Feed em Tempo Real:** Atualização via WebSocket com banner "Ver X novos posts" sem interromper a leitura. Paginação *cursor-based* (lotes de 15).
* **🔍 Busca Inteligente:** Busca por nome, curso ou instituição com *debounce* de 300ms e sugestões de conexões em comum.
* **🔔 Notificações:** Painel em tempo real para follows, likes, comments e mentions, com badge de não lidos e ação em massa "Marcar todas como lidas".
* **🎓 Perfil Acadêmico:** Nome, instituição, curso, semestre, até 10 habilidades e upload de avatar (max 2MB) com crop circular.

---

## 🏗️ Arquitetura e Banco de Dados

A estratégia central de performance é o **Fan-out on Write** combinado com **Desnormalização**:

1. Usuário cria um post.
2. Backend busca a lista de seguidores.
3. Insere um *snapshot* do post na coleção `db.feeds` de cada seguidor.
4. Emite evento WebSocket para usuários online.
5. **Leitura do Feed:** Query simples e direta em `db.feeds` ordenada por `createdAt`, sem JOINs.

> **Nota de Otimização:** Para usuários com >10k seguidores, o sistema escala para *Fan-out on Read* + Cache (escopo futuro).

### Collections Principais (MongoDB)
| Collection | Campos Chave | Nota de Design |
| :--- | :--- | :--- |
| `users` | `_id`, `name`, `institution`, `course`, `followersCount*`, `followingCount*`, `avatarUrl` | Contadores desnormalizados para evitar `$lookup`. |
| `posts` | `_id`, `authorId`, `authorName*`, `authorAvatar*`, `content`, `likesCount*`, `commentsCount*`, `createdAt` | Snapshot do autor embutido para reads sem JOIN. |
| `feeds` | `_id`, `userId`, `postId`, `postSnapshot{}`, `createdAt`, `seen` | Fan-out on write: cópia do post no feed de cada seguidor. |
| `follows` | `_id`, `followerId`, `followingId`, `createdAt` | Índice único: `{followerId, followingId}`. |
| `comments` | `_id`, `postId`, `authorId`, `authorName*`, `text`, `createdAt` | Suporte a TTL index opcional para posts expirados. |
| `notifications`| `_id`, `recipientId`, `type`, `actorId`, `actorName*`, `postId`, `read`, `createdAt` | Índice: `{recipientId, read, createdAt}` DESC. |

---

## 📏 Requisitos Não-Funcionais

* **Desempenho:** Latência do Feed < 200ms (garantido por cache e reads simples).
* **Escalabilidade:** Aplicação Python stateless orquestrada em containers Docker. MongoDB preparado para sharding por `userId`.
* **Resiliência:** WebSockets com reconexão automática e fallback HTTP.
* **Segurança:** Rate limiting de 100 req/min por IP. Bloqueio de IP por 15 min após 5 falhas de login. Validação de domínio institucional (`@unifor.br`).

---

## 🗓️ Roadmap do MVP (13 Dias)

| Micro-Sprint | Datas | Foco Principal | Frontend (Vue) | Backend (FastAPI) | MongoDB |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MS1** | 02 a 04/Jun | Fundação & Auth | `AuthForm`, `RegisterForm`, `AppShell` | Rotas Auth (JWT), CRUD Perfil Básico | Collections: `users`, `posts`, `follows` |
| **MS2** | 05 a 08/Jun | Core MVP (Posts) | `PostCard`, `PostComposer`, `ProfilePage` | Endpoints Posts, Upload de Imagem, Likes | Índices estratégicos em `posts` |
| **MS3** | 09 a 12/Jun | Social & Real-time | `FollowButton`, `useWebSocket`, `NotificationBell` | Lógica de Follow, Fan-out Worker, WebSockets | Collection `feeds` com índice `{userId, createdAt}` |
| **MS4** | 13 a 14/Jun | Polimento & Deploy | `SearchBar`, Empty States, Loaders | Endpoint de Busca (Regex), Configuração Prod. | Whitelist de IPs no Atlas |
| **D-Day** | 15/Jun | **Entrega Final** | Apresentação e Monitoramento | Ajustes finais de Rate Limit e Performance | Backups Atlas |

---

## 💻 Como Rodar Localmente

### Pré-requisitos
* Node.js (v18+) e npm/pnpm
* Python 3.10+
* Docker & Docker Compose
* Conta no MongoDB Atlas (ou MongoDB local)

### 1. Clone o repositório
```bash
git clone https://github.com/EdiellyF/StudyGraph

