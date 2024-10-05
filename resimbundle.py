import os
import math
import zipfile
from PIL import Image, ImageOps

# Ana klasör yolu
ana_klasor = "/Users/wolfgang/Desktop/adsız klasör/python/etsy/calismalar"

# Tüm PNG klasörlerindeki resim yollarını alacak liste
png_listesi = []
save_folder = ana_klasor
# Ana klasördeki tüm alt klasörleri gezip 'png' klasöründeki dosyaları bulma
for root, dirs, files in os.walk(ana_klasor):
    png_klasoru = os.path.join(root, "png")
    if os.path.exists(png_klasoru) and os.path.isdir(png_klasoru):
        png_dosyalar = [os.path.join(png_klasoru, file) for file in os.listdir(png_klasoru) if file.endswith(('jpg', 'jpeg', 'png'))]
        png_listesi.extend(png_dosyalar)

print("PNG klasöründe bulunan PNG dosyaları:")
for png in png_listesi:
    print(png)

collage_width = 1580
collage_height = 1121
rows = 15
cols = 20
images_per_collage = rows * cols

# Kaydedilecek klasörün var olup olmadığını kontrol et, yoksa oluştur

# Klasördeki tüm resim dosyalarını al
images = png_listesi

# Kaç tane kolaj gerektiğini hesapla
num_collages = math.ceil(len(images) / images_per_collage)

# Ekstra resmi yükle (kolajın altında yer alacak resim)
overlay_image_path = "/Users/wolfgang/Downloads/calismalar/logo.png"  # Değiştirin
overlay_image = Image.open(overlay_image_path)

# Kolajın yüksekliği + overlay resmin yüksekliği
final_collage_height = collage_height + overlay_image.height

# Resimleri parça parça kolajlara yerleştir
for collage_index in range(num_collages):
    # Bu kolajdaki resimlerin başlangıç ve bitiş indekslerini hesapla
    start_index = collage_index * images_per_collage
    end_index = min(start_index + images_per_collage, len(images))
    current_images = images[start_index:end_index]

    # Kaç resim olduğunu bulalım
    num_images_in_this_collage = len(current_images)

    # Eğer resim sayısı 12'den azsa, yerleşim için gerekli satır ve sütunları hesaplayalım
    if num_images_in_this_collage == 0:
        continue  # Eğer hiç resim yoksa, sonraki kolaja geç

    # Resimlerin dizilim sayısını ayarlama
    if num_images_in_this_collage == 1:
        dynamic_cols = 1
        dynamic_rows = 1
    elif num_images_in_this_collage == 2:
        dynamic_cols = 2
        dynamic_rows = 1
    elif num_images_in_this_collage == 3:
        dynamic_cols = 3
        dynamic_rows = 1
    elif num_images_in_this_collage == 4:
        dynamic_cols = 2
        dynamic_rows = 2
    elif num_images_in_this_collage <= 6:
        dynamic_cols = 3
        dynamic_rows = 2
    elif num_images_in_this_collage <= 9:
        dynamic_cols = 3
        dynamic_rows = 3
    else:  # 10 veya daha fazla resim
        dynamic_cols = cols
        dynamic_rows = rows

    # Her bir resim için ayrılacak alanın boyutlarını ayarlayalım
    thumb_width = collage_width // dynamic_cols
    thumb_height = collage_height // dynamic_rows

    # Yeni kolaj için boş bir resim oluştur (sabir boyutlarda, beyaz arka planlı)
    collage_image = Image.new('RGB', (collage_width, collage_height), color=(255, 255, 255))

    # Resimleri yerleştir
    for index, image_path in enumerate(current_images):
        img = Image.open(image_path)

        # Eğer resmin alfa kanalı varsa, şeffaf alanları beyaza doldur
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            alpha = img.convert('RGBA').split()[-1]
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))  # Beyaz arka plan
            background.paste(img, mask=alpha)
            img = background.convert('RGB')  # Şeffaflığı kaldırıp RGB'ye dönüştür

        # Resmi yeniden boyutlandır
        img = ImageOps.contain(img, (thumb_width, thumb_height))

        # Resmin kolaj içindeki yerini hesapla
        row = index // dynamic_cols
        col = index % dynamic_cols
        x = col * thumb_width
        y = row * thumb_height

        # Resmi kolaja yapıştır
        collage_image.paste(img, (x, y))

    # Final görüntü için yeni bir resim oluştur (kolaj + overlay resmi)
    final_image = Image.new('RGB', (collage_width, final_collage_height), color=(255, 255, 255))
    
    # Kolajı üstte, overlay resmi altta yerleştir
    final_image.paste(collage_image, (0, 0))
    final_image.paste(overlay_image, (0, collage_height))  # Overlay resmi kolajın altına yerleştir

    # Kolajı kaydet (kolaj numarasına göre isimlendir) PNG formatında ve beyaz arka planlı
    collage_path = os.path.join(save_folder, f'collage_output_{collage_index + 1}.png')
    final_image.save(collage_path, 'PNG')

print(f"Tüm kolajlar {save_folder} klasörüne PNG formatında kaydedildi.")
