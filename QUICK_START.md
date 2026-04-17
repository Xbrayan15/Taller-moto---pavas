# ⚡ Guía Rápida de Instalación

## Pasos para poner el proyecto en funcionamiento

### 1️⃣ Verificar Python

Abre una terminal/cmd y verifica que tengas Python 3.9+:

```bash
python --version
```

Si no lo tienes, descárgalo desde [python.org](https://www.python.org/)

### 2️⃣ Navegar a la carpeta del proyecto

```bash
cd "Taller moto - pavas"
```

### 3️⃣ Crear entorno virtual
 
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5️⃣ Iniciar el servidor

**Opción A - Ejecutar script (Windows):**
```bash
run.bat
```

**Opción B - Ejecutar script (Mac/Linux):**
```bash
bash run.sh
```

**Opción C - Manual:**
```bash
python -m uvicorn app.main:app --reload
```

### 6️⃣ Acceder a la API

- **Documentación interactiva**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API base**: http://localhost:8000

## 🎯 Primeros pasos

1. Ve a http://localhost:8000/docs
2. Expande el endpoint `POST /api/usuarios/registro`
3. Crea un usuario de prueba:
   ```json
   {
     "email": "test@example.com",
     "rol": "admin",
     "contraseña": "password123"
   }
   ```
4. Luego en el endpoint `POST /api/usuarios/login`, obtén el token
5. Haz click en "Authorize" (arriba a la derecha) y pega el token
6. ¡Ahora puedes probar todos los endpoints!

## 🚨 Solución de problemas

### Error: "Python no reconocido"
- Windows: Reinstala Python y marca "Add Python to PATH"
- Mac/Linux: Usa `python3` en lugar de `python`

### Error: "No se encuentra el módulo..."
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: "Puerto 8000 ya en uso"
```bash
python -m uvicorn app.main:app --reload --port 8001
```

## 📁 Archivos útiles

- `run.bat` / `run.sh` - Scripts para iniciar
- `requests.http` - Ejemplos de peticiones (usa extensión REST Client de VS Code)
- `README.md` - Documentación completa
- `.env` - Configuración de la aplicación

¿Necesitas ayuda? Revisa el README.md para más detalles.
