# Gestión de Podología - Paquete para crear .exe mediante GitHub Actions

Este paquete contiene la aplicación en Python y un flujo de trabajo (GitHub Actions) que **compila automáticamente** un ejecutable `.exe` usando PyInstaller y lo sube como artefacto de release.

## Qué contiene
- `gestion_podologia.py` - aplicación principal
- `requirements.txt` - dependencias
- `.github/workflows/build.yml` - workflow para compilar en GitHub Actions
- `build.bat` - script local para crear el .exe (requiere Python instalado)
- `README.md` - este archivo

## Opción recomendada (sin instalar nada en tu PC)
1. Crea una cuenta en GitHub (si no tienes).
2. Crea un nuevo repositorio público y sube **todo el contenido** de este ZIP.
3. Ve a la pestaña "Actions" y habilita los workflows (si GitHub lo solicita).
4. Cada vez que hagas `git push` al branch `main`, GitHub Actions ejecutará el workflow y generará el `.exe`.
5. Cuando termine, en la sección de "Actions" o en los artefactos del workflow podrás descargar el `.exe`.

> Nota: el workflow está configurado para crear una release con el ejecutable. Si prefieres que el ejecutable sea un artifact simple, puedo ajustar el workflow.

## Alternativa: crear el .exe en tu PC
Si prefieres compilar localmente y tienes Windows:
1. Instala Python 3.10+ (desde python.org).
2. Abre CMD en esta carpeta.
3. Ejecuta: `pip install -r requirements.txt pyinstaller`
4. Ejecuta: `pyinstaller --onefile --windowed gestion_podologia.py`
5. El ejecutable estará en `dist/gestion_podologia.exe`.

