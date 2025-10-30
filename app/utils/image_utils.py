import os
from datetime import datetime, timedelta

def save_image(image, filename):
    """Сохраняет изображение в outputs directory"""
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", filename)
    image.save(filepath, "PNG")
    return filepath

def cleanup_old_files(max_files=1000, max_age_days=7):
    """Очищает старые файлы чтобы не засорять диск"""
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        return
    
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir)]
    files = [f for f in files if os.path.isfile(f)]
    
    # Сортируем по времени модификации
    files.sort(key=os.path.getmtime)
    
    # Удаляем самые старые если превышен лимит
    if len(files) > max_files:
        for file_to_remove in files[:-max_files]:
            os.remove(file_to_remove)
    
    # Удаляем файлы старше max_age_days
    cutoff_time = datetime.now() - timedelta(days=max_age_days)
    for file_path in files:
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_time < cutoff_time:
            os.remove(file_path)