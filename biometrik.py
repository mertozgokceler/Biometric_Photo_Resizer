import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk



def select_image():
    """Open a file dialog to select an image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_path:
        global selected_image_path
        selected_image_path = file_path
        image_label.config(text=f"Seçildi: {file_path.split('/')[-1]}")
    else:
        image_label.config(text="Herhangi bir fotoğraf seçilmedi.")

def convert_to_biometric():
    """Convert the selected image to biometric photo dimensions."""
    if not selected_image_path:
        messagebox.showerror("Hata!", "Lütfen önce bir fotoğraf seçin.")
        return

    try:
        # Open the image and resize it to biometric dimensions (50x60 mm, approximately 591x709 px at 300 dpi)
        with Image.open(selected_image_path) as img:
            biometric_size = (591, 709)
            img = img.convert('RGB')
            img_width, img_height = img.size
            target_aspect_ratio = biometric_size[0] / biometric_size[1]
            img_aspect_ratio = img_width / img_height

            if img_aspect_ratio > target_aspect_ratio:
                # Crop width
                new_width = int(img_height * target_aspect_ratio)
                left = (img_width - new_width) // 2
                right = left + new_width
                img = img.crop((left, 0, right, img_height))
            elif img_aspect_ratio < target_aspect_ratio:
                # Crop height
                new_height = int(img_width / target_aspect_ratio)
                top = (img_height - new_height) // 2
                bottom = top + new_height
                img = img.crop((0, top, img_width, bottom))

            mm_to_inch = 1 / 25.4
            #dpi = 300  # 300 DPI for high-quality printing

            # Target size in mm
            target_width_mm = 50
            target_height_mm = 60

            # Convert mm to pixels
            target_width_px = int(target_width_mm / mm_to_inch)
            target_height_px = int(target_height_mm / mm_to_inch)    
            
            img_resized = img.resize(biometric_size, Image.Resampling.LANCZOS)

            # Save the converted image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG Files", "*.jpg"), ("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            if save_path:
                img_resized.save(save_path,dpi=(300, 300),quality=100)
                messagebox.showinfo("Başarılı", f"Fotoğraf başarıyla dönüştürüldü ve şu konuma kaydedildi : {save_path}")
    except Exception as e:
        messagebox.showerror("Hata!", f"An error occurred: {e}")

# Initialize Tkinter window
root = tk.Tk()
root.title("Biometric Fotoğraf Dönüştürücü")
root.geometry("400x200")
root.resizable(False, False)
root.configure(bg="black")

selected_image_path = None

# Add a button to select an image
select_button = tk.Button(root, text="Fotoğraf Seç", command=select_image, bg="white", fg="black",font=("Helvetica", 10, "bold"))
select_button.pack(pady=30)

# Label to show selected image
image_label = tk.Label(root, text="Fotoğraf Seçilmedi", bg="black", fg="white")
image_label.pack(pady=5)

# Add a button to convert to biometric
convert_button = tk.Button(root, text="Dönüştür", command=convert_to_biometric, bg="white", fg="black",font=("Helvetica", 10, "bold"))
convert_button.pack(pady=10)

# Run the application
root.mainloop()
