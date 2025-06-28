from app import create_app

if __name__ == "__main__":
    app = create_app()
    # Establecer el puerto directamente en el código
    app.run(host="0.0.0.0", port=3023, debug=True)  # Aquí establecemos el puerto 3023
