# Caso J: Inteligencia Artificial Generativa (GenAI) - Nivel 9

> **Status**: `PROYECTADO` (Próximamente)

## 🎯 El Desafío
El mercado actual exige integración con IA. No solo usar ChatGPT en la web, sino integrar modelos potentes (LLMs) **dentro** de tu infraestructura segura de AWS, conectada a tus datos.

## 🛠️ Stack Tecnológico
- **Amazon Bedrock**: API unificada para acceder a modelos fundacionales (Claude, Titan, Llama 2).
- **LangChain (Python/JS)**: Framework para orquestar la IA.
- **AWS Lambda**: Para invocar a Bedrock.

## 🚀 ¿Qué construiremos?
Un **"Analista de Portafolio Inteligente"**:
1. Un chat donde el reclutador puede preguntar: "¿Qué experiencia tiene Vladimir en AWS?".
2. El sistema (Lambda) enviará el contexto de tu CV (Caso D) a **Claude 3 (via Bedrock)**.
3. El modelo responderá basado en TU información real, alojada de forma privada.
