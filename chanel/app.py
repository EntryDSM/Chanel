# chanelApplication

from chanel import create_app
from chanel.config.vault import VaultClient

if __name__ == "__main__":
    VaultClient.initialize()
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
