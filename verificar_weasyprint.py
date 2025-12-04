"""
Script de verificación de WeasyPrint
Ejecutar: python verificar_weasyprint.py
"""

print("🔍 Verificando instalación de WeasyPrint...")
print("-" * 50)

try:
    import weasyprint
    print("✅ Módulo weasyprint importado correctamente")
    print(f"   Versión: {weasyprint.__version__}")
except ImportError as e:
    print(f"❌ Error al importar weasyprint: {e}")
    exit(1)

try:
    from weasyprint import HTML
    print("✅ Clase HTML importada correctamente")
except ImportError as e:
    print(f"❌ Error al importar HTML: {e}")
    exit(1)

try:
    html = HTML(string='<html><body><h1>Test</h1><p>WeasyPrint funciona!</p></body></html>')
    print("✅ HTML parseado correctamente")
except Exception as e:
    print(f"❌ Error al parsear HTML: {e}")
    exit(1)

try:
    pdf_bytes = html.write_pdf()
    print(f"✅ PDF generado correctamente ({len(pdf_bytes)} bytes)")
except Exception as e:
    print(f"❌ Error al generar PDF: {e}")
    exit(1)

print("-" * 50)
print("🎉 ¡WeasyPrint está completamente funcional!")
print("\n📄 Ahora puedes generar PDFs automáticamente en:")
print("   http://127.0.0.1:8000/dossier/crear/")
