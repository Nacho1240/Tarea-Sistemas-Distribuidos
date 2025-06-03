# nixos > cualquier distro de linux
FROM nixos/nix

WORKDIR /app

COPY . .

# esto va a guardar los paquetes en cache cuando se construya la imagen
# asi cuando se ejecute no los tendra que descargar
#RUN nix-shell --pure shell.nix --run "echo END BUILD"

#CMD ["nix-shell", "main.py"]
CMD ["nix-shell", "--pure", "shell.nix"]
