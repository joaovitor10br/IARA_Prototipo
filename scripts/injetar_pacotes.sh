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

# Monta e extrai a ISO base
mkdir -p "$ISO_DIR"
sudo bsdtar -xpf "$ISO_BASE" -C "$ISO_DIR"

# Copia os pacotes para o diretório apropriado
mkdir -p "$ISO_DIR/pool/custom"
for p in "${PACOTES[@]}"; do
    cp "$p" "$ISO_DIR/pool/custom/"
done

# Atualiza a lista de pacotes (host, não chroot)
dpkg-scanpackages "$ISO_DIR/pool/custom" /dev/null | gzip -9c > "$ISO_DIR/dists/stable/main/binary-amd64/Packages.gz"

# Recria a ISO com xorriso (UEFI + BIOS)
sudo xorriso -as mkisofs \
  -r -V "Ubuntu_Custom" \
  -o "$ISO_FINAL" \
  -J -joliet-long \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
  -c boot.catalog \
  -b boot/grub/i386-pc/eltorito.img \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -e EFI/boot/bootx64.efi \
  -no-emul-boot \
  -isohybrid-gpt-basdat \
  "$ISO_DIR"


echo "ISO personalizada criada em $ISO_FINAL"
