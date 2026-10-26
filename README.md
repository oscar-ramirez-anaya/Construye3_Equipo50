<div style="text-align: center;">

# Construye 3 | Contexto, memoria y acciones del asistente

### Qué ve, qué recuerda y qué puede tocar el agente de quiebres de anaquel

**Tecnológico de Monterrey** · Maestría en Inteligencia Artificial Aplicada<br>
**IA5004.10 — Sistemas multiagente** · Trimestre sept - dic 2026

**Equipo 50:** Marián Prince Flores (A01185920) · Manuel Alejandro Puga Mora (A01134471) · Oscar Alberto Ramírez Anaya (A01795438)<br>
**Modalidad:** En equipo · **Valor:** 9 % · **Fecha:** 25 de octubre de 2026 · **Modalidad de ejecución:** `luna_api`

**Entregable:** [`Construye3_Equipo50.pdf`](./Construye3_Equipo50.pdf) ·
**Notebook:** [`Construye3_Equipo50.ipynb`](./Construye3_Equipo50.ipynb)

</div>

---

## Resumen

Distribuidora Cuauhtémoc tiene un agente que detecta quiebres de anaquel y deja casos en la bandeja del
gerente de zona. En el módulo 2 el agente aprendió a decidir; en esta etapa se gobierna **qué ve**
(paquete de contexto), **qué recuerda** (memoria con olvido y confidencialidad) y **qué puede tocar**
(contratos de herramienta, repertorio de error y silla vacía). Cada decisión se relaciona con el contrato
de M1 (Construye 1) y la especificación de M2 (Construye 2).

El equipo corrió el notebook tres veces para contrastar resultados: Marián en `sin_api`, y Manuel Alejandro
y Oscar en `luna_api`. Los conteos y los nueve controles coinciden, pero el caso priorizado no: T0046/P060
y T0053/P060 **empatan en costo estimado (2,719)** y el detector no desempata. Al revisar los datos crudos
encontramos además que T0053 se reabasteció el 2026-08-24, así que la explicación de Luna es correcta pero
incompleta. De ahí sale la política propuesta de priorizar el quiebre activo al corte.

## Cobertura de la rúbrica

| Criterio | Valor | Dónde se atiende en el PDF |
|---|---:|---|
| Paquete de contexto: seleccionar, comprimir, aislar y citar | 25 % | Sección 1 y Registros 1 y 3 |
| Política de memoria con olvido y confidencialidad | 25 % | Sección 2 y Registros 1, 2 y 3 |
| Contratos de herramienta con reversibilidad y modos de fallo | 20 % | Sección 3 y Registros 1 y 2 |
| Manejo de error y silla vacía | 20 % | Sección 4 y Registros 2 y 4 |
| Trazabilidad a M1 y M2 | 10 % | Línea de trazabilidad al final de cada sección |
| Contribución y declaración de uso de IA | Requisito | Apéndices A y B |

## Parámetros del equipo

| Parámetro | Valor |
|---|---|
| Mesa de contexto (diseño) | 1,200 tokens: tarea 360 (30 %), evidencia 600 (50 %), respuesta 240 (20 %) |
| Vigencias | ventas 7 días, inventarios 1 día, precios_competencia 14 días |
| Memoria episódica | retención de 90 días; `FUENTES_EXCLUIDAS = {"portal"}` |
| Errores | 3 reintentos (2, 4 y 8 s); tope de 12 pasos por caso |
| Silla vacía | recordatorio a 4 h, elevación a 8 h, borrador como estado seguro |

## Resultados de la corrida entregada

| Registro | Qué demuestra |
|---|---|
| Ejecución 1 | Mesa armada, conteos de vigencia por fuente, 2,528 combinaciones con quiebre, propuesta de Luna validada para T0053/P060, episodio guardado, dato del portal excluido y borrador local |
| Ejecución 2 | Episodio recuperado con fecha, duplicado rechazado antes de crear y conflicto escalado al gerente |
| Caso adversarial | Comentario con inyección y marca de portal detectado (41 y 7); la orden se ignora y nada persiste |
| Errores y silla vacía | Tres reintentos, escalada a operaciones y eventos a t+0, t+4 y t+8 h |

Consumo de Luna: modelo `gpt-5.6-luna`, 1 llamada, 158 tokens de entrada y 142 de salida.
Comprobaciones finales: **9/9 aprobadas**.

## Notebook

- **Visualizar en GitHub:** [`Construye3_Equipo50.ipynb`](./Construye3_Equipo50.ipynb)
- **Visor enriquecido (nbviewer):** https://nbviewer.org/github/oscar-ramirez-anaya/Construye3_Equipo50/blob/main/Construye3_Equipo50.ipynb

El notebook está ejecutado con salidas, con la política del equipo en la celda `MODO`, el comentario
adversarial redactado, la declaración de uso de IA y las conclusiones. Respecto al notebook del curso, el
único cambio de código es que la Ejecución 1 lee la clave desde la variable de entorno `AULA_KEY` si
existe; si no, la pide con la entrada oculta. Las bibliotecas `equipo_lib.py` y `luna_adapter.py` y los
siete CSV son los del paquete común sin modificar.

## Estructura del repositorio

```
.
├── Construye3_Equipo50.pdf       # Entregable para Canvas
├── Construye3_Equipo50.ipynb     # Notebook del equipo, ejecutado en luna_api con salidas
├── equipo_lib.py                 # Biblioteca común (sin cambios)
├── luna_adapter.py               # Adaptador de Aula Gateway (sin cambios)
├── datos/                        # Siete CSV del conjunto común
├── reporte/
│   ├── reporte_tpl.html          # Fuente del PDF
│   ├── logo_tec.png              # Logo de la portada
│   └── generar_pdf.py            # Render con Chrome headless, índice paginado y pie de página
├── README.md
└── .gitignore
```

## Reproducir

**Notebook sin consumo.** Cambia `MODO = "luna_api"` por `MODO = "sin_api"` y ejecuta las celdas en orden
desde la carpeta del repositorio. En `luna_api` se usa la clave individual de Aula Gateway mediante la
entrada oculta; nunca la escribas en una celda. Con `sin_api` el caso priorizado puede ser T0046 o T0053
según la versión de pandas, por el empate de costo descrito arriba.

**PDF.** Requiere Google Chrome y los paquetes `pypdf` y `reportlab`:

```bash
cd reporte
python3 generar_pdf.py
```
