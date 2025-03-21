from auth import ghlAuthorization
from meetings import pegarSalvarReuniões

# Aplicativo Principal
if __name__ == "__main__":
    # Faz a atenticação com o GHL
    ghlAuthorization()
    pegarSalvarReuniões()