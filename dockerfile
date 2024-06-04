# Use a imagem oficial do Ubuntu como base
FROM ubuntu:latest

# Atualize os pacotes 
RUN apt-get update 

# Instale o Python 
RUN apt-get install -y python3

# Copie seus arquivos fonte para o contêiner
COPY . /app

# Defina um diretório de trabalho no contêiner
WORKDIR /app

# Comando padrão para executar o script de inicialização
CMD ["python3", "exclusaoMutua.py"]
