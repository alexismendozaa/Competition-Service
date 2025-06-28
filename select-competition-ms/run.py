from app import create_app

if __name__ == "__main__":
    app = create_app()
    # Cambiar el puerto a 3024
    app.run(host="0.0.0.0", port=3024, debug=True)  # Aquí cambiamos el puerto a 3024
