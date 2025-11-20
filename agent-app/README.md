# Agent Chatbot Frontend

Aplicación frontend Flask con interfaz de chatbot que se conecta a la API del agente.

## Características

- 🎨 Interfaz moderna y responsive
- 💬 Chat en tiempo real
- 🔄 Indicador de escritura
- ⚡ Manejo de errores
- 🎯 Configuración de usuario personalizable

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tu configuración
```

3. Ejecutar la aplicación:
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Configuración

Edita el archivo `.env` para configurar:

- `API_URL`: URL del API del agente (default: http://localhost:8000/api/agent)
- `API_TIMEOUT`: Timeout para las peticiones en segundos (default: 30)
- `PORT`: Puerto donde correrá Flask (default: 5000)
- `DEBUG`: Modo debug de Flask (default: True)

## Estructura del Proyecto

```
agent-app/
├── app.py                 # Aplicación Flask principal
├── templates/
│   └── index.html        # Template HTML del chatbot
├── static/
│   ├── css/
│   │   └── style.css     # Estilos del chatbot
│   └── js/
│       └── chat.js       # Lógica del cliente
├── .env.example          # Ejemplo de configuración
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

## API Request/Response

### Request
```json
{
    "question": "hola",
    "user": "igorov"
}
```

### Response
```json
{
    "user": "igorov",
    "question": "hola",
    "response": "Hola, esta es una respuesta dummy",
    "timestamp": "2025-11-20T18:01:53.860066",
    "status": "success"
}
```
