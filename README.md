# Stream Review API

This is a REST API project built using Django Rest Framework (DRF) and Python. The API allows users to register, log in, access a list of movies and web series, add and edit reviews, and access movies via various platforms. 
The project includes features such as permissions and authorization, token and JWT authentication, throttling, pagination, filtering, searching, and ordering.

## ✨ Key Features

### User Management & Authentication

🔐 Secure user registration and authentication system  
🎫 Token-based authentication for secure API access  
🔑 JWT (JSON Web Token) implementation  
👥 Role-based access control with custom permissions  

### Content Management

🎬 Extensive movie and web series database  
📺 Platform-specific content filtering (Netflix, Prime Video, etc.)  
⭐ User review system with full CRUD operations  
👨‍💼 Administrative dashboard for content moderation  
🛠️ Full CRUD operations for managing streaming platforms, media content (movies/web shows/podcasts) through a streamlined interface  

### API Capabilities

🔍 Search functionality with multiple parameters  
🎯 Custom throttling for different user types  
📄 Smart pagination for optimal performance  
🔄 Dynamic filtering and ordering options  

### 🔒 Security Features

#### Rate Limiting

- Anonymous: 100 requests/day
- Authenticated: 1000 requests/day

#### Authentication

- JWT with refresh token mechanism
- Token-based authentication
