#!/bin/bash
set -e

PASTA_BASE="$1"
shift
PACOTES=("$@")

ISO_BASE="$PASTA_BASE/base.iso"
ISO_DIR="$PASTA_BASE/iso_extraida"
ISO_FINAL="$PASTA_BASE/ubuntu_custom.iso"

if [ ! -f "$ISO_BASE" ]; then
    echo "Arquivo ISO base não encontrado em $ISO_BASE"
    exit 1
fi

# Esse codigo ira montar e extrair a ISO base
mkdir -p "$ISO_DIR"
bsdtar -xpf "$ISO_BASE" -C "$ISO_DIR"

# Esse codigo vai copiar os pacotes para o diretorio apropriado
mkdir -p "$ISO_DIR/pool/custom"
for p in "${PACOTES[@]}"; do
    cp "$p" "$ISO_DIR/pool/custom/"
done

#Esse codigo vai atualizar a lista de pacotes
sudo chroot "$ISO_DIR" dpkg-scanpackages /pool/custom /dev/null | gzip -9c > "$ISO_DIR/dists/stable/main/binary-amd64/Packages.gz"

#Esse codigo vai recriar a ISO
genisoimage -r -V "Custom Ubuntu" -cache-inodes -J -l \
    -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot \
    -boot-load-size 4 -boot-info-table -o "$ISO_FINAL" "$ISO_DIR"
echo "ISO personalizada criada em $ISO_FINAL"
