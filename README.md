# 🏍️ API Taller de Motos

API REST para gestionar un taller de motos, desarrollada con FastAPI y SQLite.

## 📋 Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "Taller moto - pavas"
```

### 2. Crear un entorno virtual (recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Variables de entorno

El archivo `.env` ya está creado con configuraciones por defecto. Si necesitas cambiarlas:

```env
DATABASE_URL=sqlite:///./taller.db
SECRET_KEY=tu_clave_secreta_super_segura_change_me_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_TITLE=API Taller de Motos
API_VERSION=1.0.0
```

**⚠️ En producción, cambia la `SECRET_KEY` por una clave segura y única.**

## 🏃 Ejecución

### Iniciar el servidor

```bash
python -m uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### Documentación interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 Estructura del Proyecto

```
taller-motos-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── config.py               # Configuración (variables de entorno)
│   ├── database.py             # Configuración de la base de datos
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── piloto.py
│   │   ├── motocicleta.py
│   │   └── item.py
│   ├── schemas/                # Esquemas Pydantic (validación)
│   │   ├── usuario.py
│   │   ├── piloto.py
│   │   ├── motocicleta.py
│   │   └── item.py
│   ├── crud/                   # Operaciones de base de datos
│   │   ├── usuario.py
│   │   ├── piloto.py
│   │   ├── motocicleta.py
│   │   └── item.py
│   ├── routers/                # Endpoints de la API
│   │   ├── usuarios.py
│   │   ├── pilotos.py
│   │   ├── motocicletas.py
│   │   └── items.py
│   └── auth/                   # Autenticación JWT
│       └── jwt.py
├── .env                        # Variables de entorno
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Archivos a ignorar en Git
└── taller.db                   # Base de datos SQLite (se crea automáticamente)
```

## 🔐 Autenticación

La API utiliza autenticación con **tokens JWT**. Para acceder a los endpoints:

1. **Registrarse**: `POST /api/usuarios/registro`
   ```json
   {
     "email": "usuario@example.com",
     "rol": "admin",
     "contraseña": "password123"
   }
   ```

2. **Iniciar sesión**: `POST /api/usuarios/login`
   ```json
   {
     "email": "usuario@example.com",
     "contraseña": "password123"
   }
   ```

3. **Usar el token**: Incluir en el header `Authorization: Bearer <token>`

## 📖 Endpoints principales

### Usuarios
- `POST /api/usuarios/registro` - Registrar usuario
- `POST /api/usuarios/login` - Iniciar sesión
- `GET /api/usuarios/me` - Obtener usuario actual
- `GET /api/usuarios/` - Listar todos (solo admin)
- `DELETE /api/usuarios/{id}` - Eliminar usuario (solo admin)

### Pilotos
- `POST /api/pilotos/` - Crear piloto
- `GET /api/pilotos/{id}` - Obtener piloto
- `GET /api/pilotos/` - Listar pilotos
- `PUT /api/pilotos/{id}` - Actualizar piloto
- `DELETE /api/pilotos/{id}` - Eliminar piloto

### Motocicletas
- `POST /api/motocicletas/` - Crear motocicleta
- `GET /api/motocicletas/{id}` - Obtener motocicleta
- `GET /api/motocicletas/` - Listar motocicletas
- `PUT /api/motocicletas/{id}` - Actualizar motocicleta
- `DELETE /api/motocicletas/{id}` - Eliminar motocicleta

### Items (Servicios)
- `POST /api/items/` - Crear item
- `GET /api/items/{id}` - Obtener item
- `GET /api/items/` - Listar items
- `PUT /api/items/{id}` - Actualizar item
- `DELETE /api/items/{id}` - Eliminar item

## 🧪 Probar la API

### Usando Swagger UI (en el navegador)
1. Ir a `http://localhost:8000/docs`
2. Click en "Authorize" e ingresar el token obtenido en el login
3. Probar los endpoints

### Usando Postman o Insomnia
1. Crear una colección
2. Configurar la variable `token` con el valor obtenido en login
3. Usar `Authorization: Bearer {{token}}` en los headers

## 🛠️ Tecnologías utilizadas

- **FastAPI**: Framework web moderno para APIs
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **SQLite**: Base de datos
- **Python-jose**: Tokens JWT
- **Passlib**: Hash de contraseñas
- **Uvicorn**: Servidor ASGI

## 📝 Próximos pasos

- [ ] Implementar el módulo de Servicios (relación entre Motocicletas e Items)
- [ ] Crear tabla de Historial para registrar cambios de estado
- [ ] Implementar estados (Pendiente, En proceso, Terminado)
- [ ] Crear el frontend con React
- [ ] Agregar validaciones adicionales
- [ ] Implementar logging
- [ ] Agregar tests unitarios

## ❓ Ayuda

Si encuentras problemas:

1. Verifica que Python está instalado: `python --version`
2. Asegúrate de estar en el entorno virtual
3. Reinstala las dependencias: `pip install -r requirements.txt --force-reinstall`
4. Revisa el archivo `.env` esté correctamente configurado

## 📄 Licencia

Este proyecto está disponible para uso educativo y comercial.

---

**¡Listo para empezar!** 🚀
