from flaskapp import init_flask_app  # ana flask uygulamamız

app = init_flask_app()  # ana flask uygulamamızı init ediyoruz

if __name__ == "__main__":  # bu dosya çalıştığında uygulamayı ayağa kaldırıyoruz
    app.run()
