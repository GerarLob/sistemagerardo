# Sistema Contable

Sistema de gestión contable desarrollado en Django.

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/GerarLob/sistemagerardo.git
cd sistemagerardo/SistemaContable
```

2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecuta las migraciones:
```bash
python manage.py migrate
```

6. Crea un superusuario (opcional):
```bash
python manage.py createsuperuser
```

7. Ejecuta el servidor de desarrollo:
```bash
python manage.py runserver
```

8. Abre tu navegador y ve a `http://127.0.0.1:8000/`

## Estructura del Proyecto

- `oficont/` - Configuración principal del proyecto Django
- `usuarios/` - Aplicación de gestión de usuarios
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos (CSS, JS, imágenes)

## Funcionalidades

- Sistema de autenticación de usuarios
- Gestión de usuarios
- Interfaz web responsive

## Tecnologías Utilizadas

- Django 4.2.11
- Python 3.x
- SQLite (base de datos)
- HTML/CSS/JavaScript 