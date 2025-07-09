# 🧪 Mock API Config

Proyecto de mock API para pruebas de integración, usando Flask, PostgreSQL y Swagger.

## 🚀 Descripción

Esta aplicación permite crear, listar y eliminar endpoints mock para simular respuestas de una API, útil en desarrollo y pruebas de frontend o integración.

## 🛠️ Tecnologías

- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
- Docker + Docker Compose
- Flasgger (Swagger UI)
- Alembic
- Pytest

## ⚙️ Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Alejoram2505/Challenge_API.git
cd Challenge_API
```

2. Crea un archivo `.env` o usa las variables del `docker-compose.yml`.

3. Levanta el entorno:

```bash
docker-compose up --build
```

4. Accede a la app:

- UI: [http://localhost:5000](http://localhost:5000)
- Swagger: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)
- pgAdmin: [http://localhost:8080](http://localhost:8080)

## 🧪 Pruebas

Para ejecutar los tests:

```bash
docker exec -it mock_api pytest
```

## 📦 Endpoints

- `GET /configure-mock`: Lista todos los mocks
- `POST /configure-mock`: Crea un nuevo mock
- `DELETE /configure-mock/<id>`: Elimina un mock por ID
- `ANY <mock_path>`: Ejecuta el mock configurado

Documentación completa disponible en Swagger.

## 💡 Funcionalidades

- Modo simple y avanzado desde la UI
- Persistencia de mocks con PostgreSQL
- Generación automática de mocks
- Validaciones básicas
- Interfaz mejorada y responsiva
- Tooltips y placeholders explicativos

## 📂 Estructura

```
mock_api/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── templates/
│
├── static/
├── tests/
├── migrations/
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Notas

- Alembic se encarga de manejar las migraciones.
- `mock_executor.py` maneja la ejecución dinámica de mocks.
- El entorno de tests usa una base de datos separada para aislar los datos.

## 🧑‍💻 Autor

Desarrollado por Diego Ramírez.