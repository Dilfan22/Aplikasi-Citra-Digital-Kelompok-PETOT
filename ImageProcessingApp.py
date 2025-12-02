# ========== IMPORT LIBRARY ==========
# Mengimport library tkinter sebagai tk untuk membuat GUI (Graphical User Interface)
import tkinter as tk

# Mengimport komponen-komponen spesifik dari tkinter:
# - Menu: untuk membuat menu bar aplikasi
# - filedialog: untuk dialog open/save file
# - messagebox: untuk menampilkan pesan popup
# - simpledialog: untuk input dialog sederhana
# - Scale: untuk membuat slider
# - Button: untuk membuat tombol
# - Label: untuk membuat teks label
# - Toplevel: untuk membuat window baru di atas window utama
from tkinter import Menu, filedialog, messagebox, simpledialog, Scale, Button, Label, Toplevel

# Mengimport library PIL (Python Imaging Library / Pillow) untuk manipulasi gambar:
# - Image: untuk membuka, menyimpan, dan manipulasi gambar
# - ImageTk: untuk konversi gambar PIL ke format Tkinter
# - ImageOps: operasi gambar seperti flip, mirror
# - ImageFilter: filter-filter gambar seperti blur, sharpen
# - ImageEnhance: untuk enhance brightness, contrast, dll
# - ImageDraw: untuk menggambar shape di gambar
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance, ImageDraw

# Mengimport library NumPy untuk operasi array dan matematika numerik
# Gambar akan dikonversi ke array NumPy untuk pemrosesan matematis
import numpy as np

# Mengimport library OpenCV untuk operasi image processing tingkat lanjut
# seperti edge detection, filtering, dll
import cv2

# Mengimport modul ndimage dari SciPy untuk pemrosesan gambar multi-dimensi
# terutama untuk operasi konvolusi dan filtering
from scipy import ndimage

# Mengimport fungsi-fungsi FFT (Fast Fourier Transform) dari SciPy:
# - fft2: 2D Forward Fourier Transform (domain spasial → domain frekuensi)
# - ifft2: 2D Inverse Fourier Transform (domain frekuensi → domain spasial)
# - fftshift: menggeser komponen frekuensi nol ke tengah
# - ifftshift: kebalikan dari fftshift
from scipy.fft import fft2, ifft2, fftshift, ifftshift

# Mengimport library webbrowser untuk membuka URL di browser default
import webbrowser

# ========== DEFINISI CLASS UTAMA ==========
# Mendefinisikan class ImageProcessingApp sebagai blueprint aplikasi
class ImageProcessingApp:
    # Constructor: method khusus yang otomatis dipanggil saat objek dibuat
    # self: referensi ke instance objek itu sendiri
    # root: parameter window utama Tkinter
    def __init__(self, root):
        # Menyimpan referensi window utama ke atribut instance
        self.root = root
        
        # Mengatur judul window yang muncul di title bar
        self.root.title("Aplikasi Pengolahan Citra Digital - © [Kelompok PETOT] (2025)")
        
        # Mengatur ukuran window awal: lebar 1200px, tinggi 800px
        self.root.geometry("1200x800")
        
        # Membuat atribut untuk menyimpan gambar asli/original
        # Diinisialisasi None karena belum ada gambar yang dimuat
        self.original_image = None
        
        # Membuat atribut untuk menyimpan gambar hasil pemrosesan
        self.processed_image = None
        
        # Membuat atribut untuk menyimpan gambar sementara (untuk preview slider)
        self.temp_image = None  # Untuk preview saat slider bergerak
        
        # Menyimpan path/lokasi file gambar yang dibuka
        # Berguna untuk fitur save
        self.image_path = None
        
        # Memanggil method untuk membuat struktur menu
        self.create_menu()
        
        # Memanggil method untuk membuat area tampilan gambar
        self.create_canvas()
    
    # ========== METHOD MEMBUAT CANVAS ==========
    # Method untuk membuat area canvas (area tampilan gambar)
    def create_canvas(self):
        """Membuat area canvas untuk menampilkan gambar"""
        
        # Membuat Frame (container) untuk menampung canvas
        # Frame ini berada di dalam window utama (self.root)
        self.canvas_frame = tk.Frame(self.root)
        
        # pack(): geometry manager untuk mengatur posisi widget
        # fill=tk.BOTH: Frame akan mengisi ruang horizontal dan vertikal
        # expand=True: Frame akan membesar jika window diperbesar
        # padx=10: padding/jarak horizontal 10 pixel dari tepi
        # pady=10: padding/jarak vertikal 10 pixel dari tepi
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Membuat label teks "Original Image"
        # font: tuple (nama font, ukuran, style)
        self.label_original = tk.Label(self.canvas_frame, text="Original Image", font=("Arial", 12, "bold"))
        
        # grid(): geometry manager untuk mengatur posisi dalam grid
        # row=0, column=0: posisi baris 0, kolom 0
        # padx, pady: jarak/padding dari widget lain
        self.label_original.grid(row=0, column=0, padx=5, pady=5)
        
        # Membuat canvas untuk menampilkan gambar original
        # Canvas: area gambar/drawing dari Tkinter
        # bg="gray": background color abu-abu
        # width=550, height=650: ukuran canvas dalam pixel
        self.canvas_original = tk.Canvas(self.canvas_frame, bg="gray", width=550, height=650)
        
        # Menempatkan canvas original di baris 1, kolom 0 (di bawah label)
        self.canvas_original.grid(row=1, column=0, padx=5, pady=5)
        
        # Membuat label untuk gambar processed (hasil pemrosesan)
        self.label_processed = tk.Label(self.canvas_frame, text="Processed Image", font=("Arial", 12, "bold"))
        
        # Menempatkan label processed di baris 0, kolom 1 (sejajar dengan label original)
        self.label_processed.grid(row=0, column=1, padx=5, pady=5)
        
        # Membuat canvas untuk menampilkan gambar hasil pemrosesan
        # Spesifikasi sama dengan canvas_original
        self.canvas_processed = tk.Canvas(self.canvas_frame, bg="gray", width=550, height=650)
        
        # Menempatkan canvas processed di baris 1, kolom 1 (sebelah kanan canvas_original)
        self.canvas_processed.grid(row=1, column=1, padx=5, pady=5)
    
    # ========== METHOD MEMBUAT MENU ==========
    # Method untuk membuat struktur menu lengkap
    def create_menu(self):
        """Membuat struktur menu lengkap sesuai dokumen"""
        
        # Membuat objek menu bar utama
        menubar = Menu(self.root)
        
        # Mengonfigurasi window utama agar menggunakan menubar ini
        self.root.config(menu=menubar)
        
        # ===== MENU FILE =====
        # Membuat submenu "File"
        # tearoff=0: menu tidak bisa "dirobek" (di-detach) dari window
        menu_file = Menu(menubar, tearoff=0)
        
        # Menambahkan menu "File" ke menu bar
        # add_cascade(): menambahkan menu dropdown
        # label="File": teks yang muncul di menu bar
        # menu=menu_file: submenu yang akan muncul saat di-klik
        menubar.add_cascade(label="File", menu=menu_file)
        
        # Menambahkan item "Open..." ke menu File
        # command=self.open_image: fungsi yang dipanggil saat menu diklik
        menu_file.add_command(label="Open...", command=self.open_image)
        
        # Menambahkan item "Save" yang memanggil self.save_image
        menu_file.add_command(label="Save", command=self.save_image)
        
        # Menambahkan item "Save As" yang memanggil self.save_as_image
        menu_file.add_command(label="Save As", command=self.save_as_image)
        
        # Menambahkan garis pemisah horizontal di menu
        # Untuk memisahkan grup menu yang berbeda
        menu_file.add_separator()
        
        # Menambahkan item "Exit" untuk keluar aplikasi
        menu_file.add_command(label="Exit", command=self.exit_app)
        
        # ===== MENU BASIC OPS =====
        # Membuat menu "Basic Ops" untuk operasi dasar
        menu_basic = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Basic Ops", menu=menu_basic)
        
        # Menu item "Negative" untuk membuat gambar negatif
        menu_basic.add_command(label="Negative", command=self.negative)
        
        # ===== Submenu Arithmetic =====
        # Membuat submenu "Arithmetic" di dalam menu_basic
        menu_arithmetic = Menu(menu_basic, tearoff=0)
        
        # Menambahkan submenu Arithmetic ke menu_basic
        # Submenu akan muncul saat hover/klik "Arithmetic"
        menu_basic.add_cascade(label="Arithmetic", menu=menu_arithmetic)
        
        # Item "Add (+)" untuk operasi penambahan
        menu_arithmetic.add_command(label="Add (+)", command=self.arithmetic_add)
        
        # Item "Subtract (-)" untuk operasi pengurangan
        menu_arithmetic.add_command(label="Subtract (-)", command=self.arithmetic_subtract)
        
        # Item "Multiply (*)" untuk operasi perkalian
        menu_arithmetic.add_command(label="Multiply (*)", command=self.arithmetic_multiply)
        
        # Item "Divide (/)" untuk operasi pembagian
        menu_arithmetic.add_command(label="Divide (/)", command=self.arithmetic_divide)
        
        # ===== Submenu Boolean =====
        # Membuat submenu "Boolean" untuk operasi boolean
        menu_boolean = Menu(menu_basic, tearoff=0)
        menu_basic.add_cascade(label="Boolean", menu=menu_boolean)
        
        # Item operasi NOT (inversi)
        menu_boolean.add_command(label="NOT", command=self.boolean_not)
        
        # Item operasi AND (irisan)
        menu_boolean.add_command(label="AND", command=self.boolean_and)
        
        # Item operasi OR (gabungan)
        menu_boolean.add_command(label="OR", command=self.boolean_or)
        
        # Item operasi XOR (exclusive or)
        menu_boolean.add_command(label="XOR", command=self.boolean_xor)
        
        # ===== Submenu Geometrics =====
        # Membuat submenu "Geometrics" untuk transformasi geometris
        menu_geometrics = Menu(menu_basic, tearoff=0)
        menu_basic.add_cascade(label="Geometrics", menu=menu_geometrics)
        
        # Translation: menggeser gambar secara horizontal/vertikal
        menu_geometrics.add_command(label="Translation", command=self.geometric_translation)
        
        # Rotation: memutar gambar
        menu_geometrics.add_command(label="Rotation", command=self.geometric_rotation)
        
        # Zooming: memperbesar/memperkecil gambar
        menu_geometrics.add_command(label="Zooming", command=self.geometric_zooming)
        
        # Flipping: membalik gambar (horizontal/vertikal)
        menu_geometrics.add_command(label="Flipping", command=self.geometric_flipping)
        
        # Cropping: memotong bagian gambar
        menu_geometrics.add_command(label="Cropping", command=self.geometric_cropping)
        
        # Thresholding: mengubah gambar jadi hitam-putih berdasarkan nilai threshold
        menu_basic.add_command(label="Thresholding", command=self.thresholding)
        
        # Convolution: operasi konvolusi dengan kernel
        menu_basic.add_command(label="Convolution", command=self.convolution)
        
        # Fourier Transform: transformasi ke domain frekuensi
        menu_basic.add_command(label="Fourier Transform", command=self.fourier_transform)
        
        # ===== Submenu Colouring =====
        # Membuat submenu "Colouring" untuk konversi color space
        menu_colouring = Menu(menu_basic, tearoff=0)
        menu_basic.add_cascade(label="Colouring", menu=menu_colouring)
        
        # Binary: konversi ke gambar hitam-putih
        menu_colouring.add_command(label="Binary", command=self.color_binary)
        
        # Grayscale: konversi ke skala abu-abu
        menu_colouring.add_command(label="Grayscale", command=self.color_grayscale)
        
        # RGB: konversi ke color space RGB (Red Green Blue)
        menu_colouring.add_command(label="RGB", command=self.color_rgb)
        
        # HSV: konversi ke color space HSV (Hue Saturation Value)
        menu_colouring.add_command(label="HSV", command=self.color_hsv)
        
        # CMY: konversi ke color space CMY (Cyan Magenta Yellow)
        menu_colouring.add_command(label="CMY", command=self.color_cmy)
        
        # YUV: konversi ke color space YUV (luminance chrominance)
        menu_colouring.add_command(label="YUV", command=self.color_yuv)
        
        # YIQ: konversi ke color space YIQ (digunakan di TV analog)
        menu_colouring.add_command(label="YIQ", command=self.color_yiq)
        
        # Pseudo: konversi ke pseudocolor (colormap)
        menu_colouring.add_command(label="Pseudo", command=self.color_pseudo)
        
        # ===== MENU ENHANCEMENT =====
        # Membuat menu "Enhancement" untuk peningkatan kualitas gambar
        menu_enhancement = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Enhancement", menu=menu_enhancement)
        
        # Brightness: mengatur kecerahan gambar
        menu_enhancement.add_command(label="Brightness", command=self.enhance_brightness)
        
        # Contrast: mengatur kontras gambar
        menu_enhancement.add_command(label="Contrast", command=self.enhance_contrast)
        
        # Histogram Equalization: menyeimbangkan histogram untuk meningkatkan kontras
        menu_enhancement.add_command(label="Hist. Equalization", command=self.histogram_equalization)
        
        # ===== Submenu Smoothing =====
        # Membuat submenu "Smoothing" untuk menghaluskan gambar (mengurangi noise)
        menu_smoothing = Menu(menu_enhancement, tearoff=0)
        menu_enhancement.add_cascade(label="Smoothing", menu=menu_smoothing)
        
        # Sub-submenu Spatial Domain untuk filtering di domain spasial
        menu_smoothing_spatial = Menu(menu_smoothing, tearoff=0)
        menu_smoothing.add_cascade(label="Spatial Domain", menu=menu_smoothing_spatial)
        
        # Lowpass Filtering: melewatkan frekuensi rendah (blur)
        menu_smoothing_spatial.add_command(label="Lowpass Filtering", command=self.smoothing_lowpass)
        
        # Median Filtering: filter median untuk menghilangkan salt-pepper noise
        menu_smoothing_spatial.add_command(label="Median Filtering", command=self.smoothing_median)
        
        # Sub-submenu Frequency Domain untuk filtering di domain frekuensi
        menu_smoothing_freq = Menu(menu_smoothing, tearoff=0)
        menu_smoothing.add_cascade(label="Frequency Domain", menu=menu_smoothing_freq)
        
        # ILPF: Ideal Lowpass Filter (filter frekuensi rendah ideal)
        menu_smoothing_freq.add_command(label="ILPF", command=self.smoothing_ilpf)
        
        # BLPF: Butterworth Lowpass Filter (filter frekuensi rendah Butterworth)
        menu_smoothing_freq.add_command(label="BLPF", command=self.smoothing_blpf)
        
        # ===== Submenu Sharpening =====
        # Membuat submenu "Sharpening" untuk mempertajam gambar (meningkatkan edge)
        menu_sharpening = Menu(menu_enhancement, tearoff=0)
        menu_enhancement.add_cascade(label="Sharpening", menu=menu_sharpening)
        
        # Sub-submenu Spatial Domain untuk sharpening di domain spasial
        menu_sharpening_spatial = Menu(menu_sharpening, tearoff=0)
        menu_sharpening.add_cascade(label="Spatial Domain", menu=menu_sharpening_spatial)
        
        # Highpass Filtering: melewatkan frekuensi tinggi (sharpen)
        menu_sharpening_spatial.add_command(label="Highpass Filtering", command=self.sharpening_highpass)
        
        # Highboost Filtering: amplifikasi frekuensi tinggi
        menu_sharpening_spatial.add_command(label="Highboost Filtering", command=self.sharpening_highboost)
        
        # Sub-submenu Frequency Domain untuk sharpening di domain frekuensi
        menu_sharpening_freq = Menu(menu_sharpening, tearoff=0)
        menu_sharpening.add_cascade(label="Frequency Domain", menu=menu_sharpening_freq)
        
        # IHPF: Ideal Highpass Filter
        menu_sharpening_freq.add_command(label="IHPF", command=self.sharpening_ihpf)
        
        # BHPF: Butterworth Highpass Filter
        menu_sharpening_freq.add_command(label="BHPF", command=self.sharpening_bhpf)
        
        # Geometrics Correction: koreksi geometris
        menu_enhancement.add_command(label="Geometrics Correction", command=self.geometric_correction)
        
        # ===== MENU NOISE =====
        # Membuat menu "Noise" untuk menambahkan berbagai jenis noise ke gambar
        menu_noise = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Noise", menu=menu_noise)
        
        # Gaussian Noise: noise dengan distribusi normal/Gaussian
        menu_noise.add_command(label="Gaussian Noise", command=self.noise_gaussian)
        
        # Rayleigh Noise: noise dengan distribusi Rayleigh
        menu_noise.add_command(label="Rayleigh Noise", command=self.noise_rayleigh)
        
        # Erlang (Gamma) Noise: noise dengan distribusi gamma
        menu_noise.add_command(label="Erlang (Gamma) Noise", command=self.noise_erlang)
        
        # Exponential Noise: noise dengan distribusi eksponensial
        menu_noise.add_command(label="Exponential Noise", command=self.noise_exponential)
        
        # Uniform Noise: noise dengan distribusi uniform (rata)
        menu_noise.add_command(label="Uniform Noise", command=self.noise_uniform)
        
        # Impulse Noise: salt and pepper noise (titik hitam-putih acak)
        menu_noise.add_command(label="Impulse Noise", command=self.noise_impulse)
        
        # ===== MENU EDGE DETECTION =====
        # Membuat menu "Edge Detection" untuk mendeteksi tepi/edge dalam gambar
        menu_edge = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edge Detection", menu=menu_edge)
        
        # ===== Submenu 1st Differential Gradient =====
        # Submenu untuk metode deteksi edge menggunakan turunan pertama
        menu_1st_diff = Menu(menu_edge, tearoff=0)
        menu_edge.add_cascade(label="1st Differential Gradient", menu=menu_1st_diff)
        
        # Sobel: operator Sobel untuk deteksi edge
        menu_1st_diff.add_command(label="Sobel", command=self.edge_sobel)
        
        # Prewitt: operator Prewitt (mirip Sobel, kernel berbeda)
        menu_1st_diff.add_command(label="Prewitt", command=self.edge_prewitt)
        
        # Robert: operator Robert (kernel 2x2)
        menu_1st_diff.add_command(label="Robert", command=self.edge_robert)
        
        # ===== Submenu 2nd Differential Gradient =====
        # Submenu untuk metode deteksi edge menggunakan turunan kedua
        menu_2nd_diff = Menu(menu_edge, tearoff=0)
        menu_edge.add_cascade(label="2nd Differential Gradient", menu=menu_2nd_diff)
        
        # Laplacian: operator Laplacian
        menu_2nd_diff.add_command(label="Laplacian", command=self.edge_laplacian)
        
        # LoG: Laplacian of Gaussian (Gaussian blur + Laplacian)
        menu_2nd_diff.add_command(label="Laplacian of Gaussian (LoG)", command=self.edge_log)
        
        # Canny: algoritma Canny (deteksi edge multi-stage)
        menu_2nd_diff.add_command(label="Canny", command=self.edge_canny)
        
        # Compass: deteksi edge dengan operator Kirsch (8 arah)
        menu_edge.add_command(label="Compass", command=self.edge_compass)
        
        # ===== MENU SEGMENTATION =====
        # Membuat menu "Segmentation" untuk memisahkan objek dari background
        menu_segmentation = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Segmentation", menu=menu_segmentation)
        
        # Region Growing: segmentasi berdasarkan pertumbuhan region dari seed point
        menu_segmentation.add_command(label="Region Growing", command=self.segmentation_region_growing)
        
        # Watershed: segmentasi dengan algoritma watershed (seperti aliran air)
        menu_segmentation.add_command(label="Watershed", command=self.segmentation_watershed)
        
        # ===== MENU ABOUT =====
        # Membuat menu "About" untuk informasi aplikasi dan tim
        menu_about = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=menu_about)
        
        # Info tim developer
        menu_about.add_command(label="Info Tim Developer", command=self.show_info)
        menu_about.add_separator()
        
        # Link ke Github tutorial
        menu_about.add_command(label="Tutorial: Link Github", command=self.open_github)
        
        # Link ke Youtube tutorial
        menu_about.add_command(label="Tutorial: Link Youtube", command=self.open_youtube)
    
    # ========== SLIDER DIALOG ==========
    # Method untuk membuat dialog popup dengan slider
    # Parameters:
    # - title: judul window dialog
    # - label_text: teks instruksi
    # - min_val: nilai minimum slider
    # - max_val: nilai maksimum slider
    # - default_val: nilai default/awal
    # - resolution: langkah perubahan nilai (default=1)
    # - callback: fungsi yang dipanggil saat slider bergerak (default=None)
    def create_slider_dialog(self, title, label_text, min_val, max_val, default_val, resolution=1, callback=None):
        """Membuat dialog dengan slider, OK, dan Reset button"""
        
        # Membuat window baru di atas window utama menggunakan Toplevel
        dialog = Toplevel(self.root)
        
        # Set judul dialog
        dialog.title(title)
        
        # Set ukuran dialog: lebar 400px, tinggi 200px
        dialog.geometry("400x200")
        
        # Membuat dialog non-resizable (tidak bisa diubah ukuran)
        dialog.resizable(False, False)
        
        # Membuat dialog selalu di atas parent window
        # Dialog akan ikut minimize jika parent di-minimize
        dialog.transient(self.root)
        
        # Membuat dialog modal: user harus tutup dialog ini dulu
        # sebelum berinteraksi dengan window lain
        dialog.grab_set()
        
        # Membuat label instruksi dengan font bold
        label = Label(dialog, text=label_text, font=("Arial", 10, "bold"))
        
        # Menampilkan label dengan jarak vertikal 10px
        label.pack(pady=10)
        
        # Membuat variabel Tkinter untuk menyimpan nilai slider
        # DoubleVar: variabel untuk bilangan desimal yang ter-sinkronisasi dengan widget
        value_var = tk.DoubleVar(value=default_val)
        
        # Dictionary untuk menyimpan hasil (nilai dan status konfirmasi)
        # Akan dikembalikan ke pemanggil method
        result = {'value': None, 'confirmed': False}
        
        # Label untuk menampilkan nilai slider saat ini
        # f"...": f-string untuk interpolasi variabel
        value_label = Label(dialog, text=f"Value: {default_val}", font=("Arial", 10))
        value_label.pack(pady=5)
        
        # Inner function (fungsi di dalam fungsi)
        # Dipanggil setiap kali slider bergerak
        def on_slider_change(val):
            # Update label dengan nilai slider baru
            # :.2f: format 2 angka di belakang koma
            value_label.config(text=f"Value: {float(val):.2f}")
            
            # Cek apakah callback function ada (not None)
            if callback:
                # Panggil callback function dengan nilai slider untuk preview real-time
                callback(float(val))
        
        # Membuat widget slider (Scale)
        # from_: nilai minimum (pakai underscore karena "from" adalah keyword Python)
        # to: nilai maksimum
        # orient=tk.HORIZONTAL: slider horizontal (kiri-kanan)
        # resolution: step/langkah perubahan nilai
        # length=300: panjang slider 300 pixel
        # variable=value_var: terikat dengan value_var
        # command: fungsi yang dipanggil saat slider berubah
        slider = Scale(dialog, from_=min_val, to=max_val, orient=tk.HORIZONTAL, 
                      resolution=resolution, length=300, variable=value_var,
                      command=on_slider_change)
        
        # Menampilkan slider
        slider.pack(pady=10)
        
        # Membuat frame untuk menampung tombol OK dan Reset
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        # Inner function untuk tombol OK
        # Dipanggil saat tombol OK diklik
        def on_ok():
            # Simpan nilai slider ke dictionary result
            result['value'] = value_var.get()
            
            # Set status konfirmasi menjadi True
            result['confirmed'] = True
            
            # Tutup dialog
            dialog.destroy()
        
        # Inner function untuk tombol Reset
        # Dipanggil saat tombol Reset diklik
        def on_reset():
            # Set nilai ke None (batalkan)
            result['value'] = None
            
            # Set status konfirmasi menjadi False
            result['confirmed'] = False
            
            # Tutup dialog
            dialog.destroy()
        
        # Membuat tombol OK
        # command=on_ok: fungsi yang dipanggil saat diklik
        # width=10: lebar tombol
        # bg="green": background hijau
        # fg="white": foreground (teks) putih
        btn_ok = Button(btn_frame, text="OK", command=on_ok, width=10, bg="green", fg="white")
        
        # Menampilkan tombol OK di sebelah kiri
        # side=tk.LEFT: posisi di sebelah kiri
        # padx=10: jarak horizontal 10px
        btn_ok.pack(side=tk.LEFT, padx=10)
        
        # Membuat tombol Reset dengan background merah
        btn_reset = Button(btn_frame, text="Reset", command=on_reset, width=10, bg="red", fg="white")
        
        # Menampilkan tombol Reset di sebelah kiri tombol OK
        btn_reset.pack(side=tk.LEFT, padx=10)
        
        # Wait for dialog to close (menunggu hingga dialog ditutup)
        # Eksekusi program akan berhenti di sini sampai dialog ditutup
        dialog.wait_window()
        
        # Mengembalikan dictionary result yang berisi nilai dan status konfirmasi
        return result
    
    # ========== IMPLEMENTASI FUNGSI FILE ==========
    # Method untuk membuka file gambar
    def open_image(self):
        """Membuka file gambar"""
        
        # Menampilkan dialog pemilihan file
        # title: judul dialog
        # filetypes: filter tipe file yang bisa dipilih
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All Files", "*.*")]
        )
        
        # Cek apakah user memilih file (tidak cancel)
        if file_path:
            # Simpan path file
            self.image_path = file_path
            
            # Buka gambar menggunakan PIL dan simpan ke original_image
            self.original_image = Image.open(file_path)
            
            # Copy gambar original ke processed_image
            self.processed_image = self.original_image.copy()
            
            # Tampilkan kedua gambar di canvas
            self.display_images()
    
    # Method untuk menyimpan gambar yang telah diproses
    def save_image(self):
        """Menyimpan gambar yang telah diproses"""
        
        # Cek apakah ada gambar processed
        if self.processed_image:
            # Cek apakah ada path file (sudah pernah dibuka)
            if self.image_path:
                # Simpan gambar ke path yang sama
                self.processed_image.save(self.image_path)
                
                # Tampilkan pesan sukses
                messagebox.showinfo("Success", "Image saved successfully!")
            else:
                # Jika belum ada path, panggil save_as
                self.save_as_image()
        else:
            # Jika tidak ada gambar, tampilkan warning
            messagebox.showwarning("Warning", "No processed image to save!")
    
    # Method untuk menyimpan gambar dengan nama baru
    def save_as_image(self):
        """Menyimpan gambar dengan nama baru"""
        
        # Cek apakah ada gambar processed
        if self.processed_image:
            # Menampilkan dialog save file
            # defaultextension: ekstensi default jika user tidak mengetik ekstensi
            # filetypes: pilihan format file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("All Files", "*.*")]
            )
            
            # Cek apakah user memilih lokasi (tidak cancel)
            if file_path:
                # Simpan gambar ke path yang dipilih
                self.processed_image.save(file_path)
                
                # Tampilkan pesan sukses
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            # Jika tidak ada gambar, tampilkan warning
            messagebox.showwarning("Warning", "No processed image to save!")
    
    # Method untuk keluar dari aplikasi
    def exit_app(self):
        """Keluar dari aplikasi"""
        
        # Tampilkan dialog konfirmasi
        # askokcancel: mengembalikan True jika OK, False jika Cancel
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            # Tutup window dan keluar aplikasi
            self.root.destroy()
    
    # Method untuk menampilkan gambar di canvas
    def display_images(self):
        """Menampilkan gambar di canvas"""
        
        # Cek apakah ada gambar original
        if self.original_image:
            # Resize gambar agar fit di canvas (540x640)
            orig_resized = self.resize_for_canvas(self.original_image, 540, 640)
            
            # Konversi gambar PIL ke format Tkinter PhotoImage
            orig_photo = ImageTk.PhotoImage(orig_resized)
            
            # Tampilkan gambar di canvas original pada koordinat (275, 325) - tengah canvas
            self.canvas_original.create_image(275, 325, image=orig_photo)
            
            # Simpan referensi gambar agar tidak di-garbage collect
            # Tkinter memerlukan referensi gambar tetap hidup
            self.canvas_original.image = orig_photo
        
        # Cek apakah ada gambar processed
        if self.processed_image:
            # Resize gambar processed
            proc_resized = self.resize_for_canvas(self.processed_image, 540, 640)
            
            # Konversi ke PhotoImage
            proc_photo = ImageTk.PhotoImage(proc_resized)
            
            # Tampilkan di canvas processed
            self.canvas_processed.create_image(275, 325, image=proc_photo)
            
            # Simpan referensi
            self.canvas_processed.image = proc_photo
    
    # Method untuk menampilkan gambar temporary (preview)
    def display_temp_image(self):
        """Menampilkan gambar temporary untuk preview"""
        
        # Cek apakah ada temp_image
        if self.temp_image:
            # Resize temp image
            proc_resized = self.resize_for_canvas(self.temp_image, 540, 640)
            
            # Konversi ke PhotoImage
            proc_photo = ImageTk.PhotoImage(proc_resized)
            
            # Tampilkan di canvas processed (menimpa gambar sebelumnya)
            self.canvas_processed.create_image(275, 325, image=proc_photo)
            
            # Simpan referensi
            self.canvas_processed.image = proc_photo
    
    # Method untuk resize gambar agar fit di canvas
    # max_width: lebar maksimum canvas
    # max_height: tinggi maksimum canvas
    def resize_for_canvas(self, image, max_width, max_height):
        """Resize gambar agar fit di canvas"""
        
        # Ambil ukuran gambar original
        img_width, img_height = image.size
        
        # Hitung rasio resize (pilih yang terkecil agar gambar fit)
        # min(): memilih rasio terkecil agar gambar tidak keluar canvas
        ratio = min(max_width/img_width, max_height/img_height)
        
        # Hitung ukuran baru berdasarkan rasio
        # int(): konversi ke integer karena ukuran harus bilangan bulat
        new_size = (int(img_width*ratio), int(img_height*ratio))
        
        # Resize gambar dengan algoritma LANCZOS (kualitas tinggi)
        # Image.Resampling.LANCZOS: algoritma interpolasi berkualitas tinggi
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Method untuk mengecek apakah gambar sudah dimuat
    def check_image_loaded(self):
        """Cek apakah gambar sudah dimuat"""
        
        # Cek apakah original_image masih None (belum ada gambar)
        if self.original_image is None:
            # Tampilkan warning jika belum ada gambar
            messagebox.showwarning("Warning", "Please load an image first!")
            
            # Kembalikan False (gambar belum dimuat)
            return False
        
        # Kembalikan True (gambar sudah dimuat)
        return True
    
    # ========== BASIC OPS FUNCTIONS ==========
    # Method untuk membuat gambar negatif dengan slider
    def negative(self):
        """Negative image dengan slider"""
        
        # Cek apakah gambar sudah dimuat, jika belum return (keluar dari fungsi)
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview negative saat slider bergerak
        # val: nilai slider (0-100)
        def preview_negative(val):
            # Hitung strength (kekuatan efek) dari 0.0 sampai 1.0
            strength = val / 100.0
            
            # Konversi gambar PIL ke numpy array dengan tipe float32
            # convert("RGB"): pastikan gambar dalam format RGB
            # dtype=np.float32: tipe data float untuk operasi matematika
            img_array = np.array(self.original_image.convert("RGB"), dtype=np.float32)
            
            # Hitung inversi (negative): 255 - nilai pixel
            inverted = 255 - img_array
            
            # Interpolasi linear antara gambar original dan inverted
            # result = original + strength * (inverted - original)
            # strength=0: hasil = original
            # strength=1: hasil = inverted
            result = img_array + strength * (inverted - img_array)
            
            # Clip nilai ke range 0-255 dan konversi ke uint8
            # np.clip(): membatasi nilai dalam range tertentu
            # astype(np.uint8): konversi ke tipe data unsigned 8-bit integer
            result = np.clip(result, 0, 255).astype(np.uint8)
            
            # Konversi numpy array kembali ke gambar PIL
            self.temp_image = Image.fromarray(result)
            
            # Tampilkan preview
            self.display_temp_image()
        
        # Tampilkan slider dialog
        # Range 0-100%, default 100%, step 1
        # preview_negative: callback function untuk preview
        result = self.create_slider_dialog("Negative", "Negative: 0-100%", 0, 100, 100, 1, preview_negative)
        
        # Cek apakah user klik OK (confirmed=True) dan ada nilai
        if result['confirmed'] and result['value'] is not None:
            # Hitung strength dari nilai slider
            strength = result['value'] / 100.0
            
            # Konversi gambar ke numpy array
            img_array = np.array(self.original_image.convert("RGB"), dtype=np.float32)
            
            # Hitung inversi
            inverted = 255 - img_array
            
            # Interpolasi linear
            final_result = img_array + strength * (inverted - img_array)
            
            # Clip dan konversi tipe data
            final_result = np.clip(final_result, 0, 255).astype(np.uint8)
            
            # Simpan hasil ke processed_image
            self.processed_image = Image.fromarray(final_result)
        else:
            # Jika user klik Reset atau Cancel, kembalikan ke gambar original
            self.processed_image = self.original_image.copy()
        
        # Tampilkan gambar final
        self.display_images()
    
    # ========== Arithmetic Operations ==========
    # Method untuk operasi penambahan (Add)
    def arithmetic_add(self):
        # Cek gambar sudah dimuat
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_add(val):
            # Konversi gambar ke numpy array float32
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # Operasi penambahan: setiap pixel + val
            # np.clip(): batasi hasil dalam range 0-255
            result = np.clip(img_array + val, 0, 255).astype(np.uint8)
            
            # Simpan ke temp_image dan tampilkan
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider range 0-255, default 50
        result = self.create_slider_dialog("Add", "Add Value: 0-255", 0, 255, 50, 1, preview_add)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            # Lakukan operasi penambahan final
            img_array = np.array(self.original_image, dtype=np.float32)
            final_result = np.clip(img_array + result['value'], 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            # Jika Cancel/Reset, kembalikan ke original
            self.processed_image = self.original_image.copy()
        
        # Tampilkan hasil
        self.display_images()
    
    # Method untuk operasi pengurangan (Subtract)
    def arithmetic_subtract(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_subtract(val):
            # Konversi ke numpy array
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # Operasi pengurangan: setiap pixel - val
            result = np.clip(img_array - val, 0, 255).astype(np.uint8)
            
            # Tampilkan preview
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider range 0-255, default 50
        result = self.create_slider_dialog("Subtract", "Subtract Value: 0-255", 0, 255, 50, 1, preview_subtract)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            final_result = np.clip(img_array - result['value'], 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk operasi perkalian (Multiply)
    def arithmetic_multiply(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_multiply(val):
            # Konversi ke numpy array
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # Operasi perkalian: setiap pixel * val
            result = np.clip(img_array * val, 0, 255).astype(np.uint8)
            
            # Tampilkan preview
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider range 0.1-5.0, default 1.0, step 0.1
        result = self.create_slider_dialog("Multiply", "Multiply Factor: 0.1-5.0", 0.1, 5.0, 1.0, 0.1, preview_multiply)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            final_result = np.clip(img_array * result['value'], 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk operasi pembagian (Divide)
    def arithmetic_divide(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_divide(val):
            # Konversi ke numpy array
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # Operasi pembagian: setiap pixel / val
            result = np.clip(img_array / val, 0, 255).astype(np.uint8)
            
            # Tampilkan preview
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider range 0.1-5.0, default 1.0, step 0.1
        result = self.create_slider_dialog("Divide", "Divide Factor: 0.1-5.0", 0.1, 5.0, 1.0, 0.1, preview_divide)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            final_result = np.clip(img_array / result['value'], 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # ========== Boolean Operations ==========
    # Method untuk operasi Boolean NOT
    def boolean_not(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_not(val):
            # Hitung strength dari slider
            strength = val / 100.0
            
            # Konversi ke grayscale dulu
            # convert("L"): convert ke grayscale (L = Luminance)
            img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            # Inversi (NOT operation)
            inverted = 255 - img_array
            
            # Interpolasi berdasarkan strength
            result = img_array + strength * (inverted - img_array)
            result = np.clip(result, 0, 255).astype(np.uint8)
            
            # Tampilkan preview
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider NOT strength 0-100%, default 100%
        result = self.create_slider_dialog("Boolean NOT", "NOT Strength: 0-100%", 0, 100, 100, 1, preview_not)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            strength = result['value'] / 100.0
            img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
            inverted = 255 - img_array
            final_result = img_array + strength * (inverted - img_array)
            final_result = np.clip(final_result, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk operasi Boolean AND
    def boolean_and(self):
        if not self.check_image_loaded(): return
        
        # Minta user memilih gambar kedua
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Kedua untuk Operasi AND",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All Files", "*.*")]
        )
        
        # Jika user memilih file
        if file_path:
            # Buka gambar kedua
            img2 = Image.open(file_path)
            
            # Resize gambar kedua agar sama dengan gambar original
            img2 = img2.resize(self.original_image.size)
            
            # Konversi kedua gambar ke grayscale
            img1_gray = np.array(self.original_image.convert("L"))
            img2_gray = np.array(img2.convert("L"))
            
            # Operasi bitwise AND
            # np.bitwise_and(): AND setiap bit pixel
            result = np.bitwise_and(img1_gray, img2_gray)
            
            # Simpan hasil
            self.processed_image = Image.fromarray(result)
            self.display_images()
    
    # Method untuk operasi Boolean OR
    def boolean_or(self):
        if not self.check_image_loaded(): return
        
        # Minta user memilih gambar kedua
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Kedua untuk Operasi OR",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All Files", "*.*")]
        )
        
        if file_path:
            # Buka dan resize gambar kedua
            img2 = Image.open(file_path)
            img2 = img2.resize(self.original_image.size)
            
            # Konversi ke grayscale
            img1_gray = np.array(self.original_image.convert("L"))
            img2_gray = np.array(img2.convert("L"))
            
            # Operasi bitwise OR
            result = np.bitwise_or(img1_gray, img2_gray)
            
            self.processed_image = Image.fromarray(result)
            self.display_images()
    
    # Method untuk operasi Boolean XOR
    def boolean_xor(self):
        if not self.check_image_loaded(): return
        
        # Minta user memilih gambar kedua
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Kedua untuk Operasi XOR",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All Files", "*.*")]
        )
        
        if file_path:
            # Buka dan resize gambar kedua
            img2 = Image.open(file_path)
            img2 = img2.resize(self.original_image.size)
            
            # Konversi ke grayscale
            img1_gray = np.array(self.original_image.convert("L"))
            img2_gray = np.array(img2.convert("L"))
            
            # Operasi bitwise XOR (Exclusive OR)
            result = np.bitwise_xor(img1_gray, img2_gray)
            
            self.processed_image = Image.fromarray(result)
            self.display_images()
    
    # ========== Geometric Operations ==========
    # Method untuk translasi (menggeser gambar)
    def geometric_translation(self):
        if not self.check_image_loaded(): return
        
        # Minta input translasi X (horizontal)
        # Range -500 sampai 500, default 0, step 10
        result_x = self.create_slider_dialog("Translation X", "X Translation: -500 to 500", -500, 500, 0, 10)
        
        # Jika user cancel, kembalikan ke original
        if not result_x['confirmed']:
            self.processed_image = self.original_image.copy()
            self.display_images()
            return
        
        # Minta input translasi Y (vertikal)
        result_y = self.create_slider_dialog("Translation Y", "Y Translation: -500 to 500", -500, 500, 0, 10)
        
        # Jika user cancel
        if not result_y['confirmed']:
            self.processed_image = self.original_image.copy()
            self.display_images()
            return
        
        # Ambil nilai translasi
        tx = result_x['value']
        ty = result_y['value']
        
        # Lakukan transformasi affine untuk translasi
        # Image.AFFINE: transformasi affine (linear transformation)
        # (1, 0, -tx, 0, 1, -ty): matrix transformasi
        # [1 0 -tx]   tx = translasi X
        # [0 1 -ty]   ty = translasi Y
        self.processed_image = self.original_image.transform(
            self.original_image.size, Image.AFFINE, (1, 0, -tx, 0, 1, -ty)
        )
        
        self.display_images()
    
    # Method untuk rotasi (memutar gambar)
    def geometric_rotation(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview rotasi
        def preview_rotation(val):
            # Rotasi gambar dengan sudut val
            # expand=True: ukuran canvas menyesuaikan agar gambar tidak terpotong
            rotated = self.original_image.rotate(val, expand=True)
            
            # Simpan ke temp dan tampilkan
            self.temp_image = rotated
            self.display_temp_image()
        
        # Slider rotasi -360 sampai 360 derajat, default 0, step 1
        result = self.create_slider_dialog("Rotation", "Rotation Angle: -360 to 360", -360, 360, 0, 1, preview_rotation)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            # Rotasi gambar final
            self.processed_image = self.original_image.rotate(result['value'], expand=True)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk zooming (memperbesar/memperkecil)
    def geometric_zooming(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview zoom
        def preview_zoom(val):
            # Hitung ukuran baru berdasarkan zoom factor
            new_size = (int(self.original_image.width * val), int(self.original_image.height * val))
            
            # Resize gambar dengan algoritma LANCZOS (kualitas tinggi)
            zoomed = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Simpan dan tampilkan preview
            self.temp_image = zoomed
            self.display_temp_image()
        
        # Slider zoom 0.1x sampai 5.0x, default 1.0x, step 0.1
        result = self.create_slider_dialog("Zooming", "Zoom Factor: 0.1-5.0", 0.1, 5.0, 1.0, 0.1, preview_zoom)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            # Hitung ukuran baru
            new_size = (int(self.original_image.width * result['value']), int(self.original_image.height * result['value']))
            
            # Resize gambar final
            self.processed_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk flipping (membalik gambar)
    def geometric_flipping(self):
        if not self.check_image_loaded(): return
        
        # Buat dialog custom untuk pilihan flip
        dialog = Toplevel(self.root)
        dialog.title("Flipping")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Label instruksi
        Label(dialog, text="Select Flip Direction:", font=("Arial", 10, "bold")).pack(pady=20)
        
        # Dictionary untuk menyimpan pilihan user
        result = {'value': None}
        
        # Inner function untuk tombol Horizontal
        def on_horizontal():
            result['value'] = 'horizontal'
            dialog.destroy()
        
        # Inner function untuk tombol Vertical
        def on_vertical():
            result['value'] = 'vertical'
            dialog.destroy()
        
        # Frame untuk tombol
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        # Tombol Horizontal
        Button(btn_frame, text="Horizontal", command=on_horizontal, width=12, bg="blue", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Tombol Vertical
        Button(btn_frame, text="Vertical", command=on_vertical, width=12, bg="blue", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Tunggu dialog ditutup
        dialog.wait_window()
        
        # Lakukan flipping sesuai pilihan
        if result['value'] == 'horizontal':
            # Flip horizontal (kiri-kanan)
            # Image.FLIP_LEFT_RIGHT: konstanta untuk flip horizontal
            self.processed_image = self.original_image.transpose(Image.FLIP_LEFT_RIGHT)
        elif result['value'] == 'vertical':
            # Flip vertical (atas-bawah)
            # Image.FLIP_TOP_BOTTOM: konstanta untuk flip vertical
            self.processed_image = self.original_image.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            # Jika cancel, kembalikan ke original
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk cropping (memotong gambar)
    def geometric_cropping(self):
        if not self.check_image_loaded(): return
        
        # Minta input koordinat crop menggunakan simpledialog
        # askinteger(): dialog input angka integer
        
        # X1 (left): koordinat kiri
        x1 = simpledialog.askinteger("Crop", "Enter X1 (left):", initialvalue=0)
        if x1 is None: return  # Jika cancel, keluar
        
        # Y1 (top): koordinat atas
        y1 = simpledialog.askinteger("Crop", "Enter Y1 (top):", initialvalue=0)
        if y1 is None: return
        
        # X2 (right): koordinat kanan
        x2 = simpledialog.askinteger("Crop", "Enter X2 (right):", initialvalue=self.original_image.width)
        if x2 is None: return
        
        # Y2 (bottom): koordinat bawah
        y2 = simpledialog.askinteger("Crop", "Enter Y2 (bottom):", initialvalue=self.original_image.height)
        if y2 is None: return
        
        # Crop gambar dengan koordinat (x1, y1, x2, y2)
        # crop(): memotong gambar dalam rectangle
        self.processed_image = self.original_image.crop((x1, y1, x2, y2))
        
        self.display_images()
    
    # Method untuk thresholding (konversi ke binary berdasarkan threshold)
    def thresholding(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview thresholding
        def preview_threshold(val):
            # Konversi ke grayscale
            img_gray = np.array(self.original_image.convert("L"))
            
            # cv2.threshold(): fungsi thresholding OpenCV
            # int(val): nilai threshold
            # 255: nilai maximum (putih)
            # cv2.THRESH_BINARY: tipe thresholding binary
            # Pixel > threshold = 255 (putih), pixel <= threshold = 0 (hitam)
            _, result = cv2.threshold(img_gray, int(val), 255, cv2.THRESH_BINARY)
            
            # Tampilkan preview
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider threshold 0-255, default 127 (tengah), step 1
        result = self.create_slider_dialog("Thresholding", "Threshold Value: 0-255", 0, 255, 127, 1, preview_threshold)
        
        # Jika OK diklik
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"))
            
            # Lakukan thresholding final
            _, final_result = cv2.threshold(img_gray, int(result['value']), 255, cv2.THRESH_BINARY)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk konvolusi dengan kernel
    def convolution(self):
        if not self.check_image_loaded(): return
        
        # Kernel 3x3 sederhana untuk edge detection
        # Kernel ini akan mendeteksi tepi gambar
        kernel = np.array([[-1, -1, -1],
                          [-1,  8, -1],
                          [-1, -1, -1]])
        
        # Konversi gambar ke grayscale dan float32
        img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
        
        # ndimage.convolve(): fungsi konvolusi dari scipy
        # Mengaplikasikan kernel ke seluruh gambar
        result = ndimage.convolve(img_array, kernel)
        
        # Clip hasil dan konversi tipe data
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(result)
        self.display_images()
    
    # Method untuk Fourier Transform
    def fourier_transform(self):
        if not self.check_image_loaded(): return
        
        # Konversi gambar ke grayscale float32
        img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
        
        # fft2(): 2D Fast Fourier Transform
        # Mengubah gambar dari domain spasial ke domain frekuensi
        f = fft2(img_gray)
        
        # fftshift(): menggeser komponen DC (frekuensi 0) ke tengah
        # Agar spectrum lebih mudah divisualisasikan
        fshift = fftshift(f)
        
        # Hitung magnitude spectrum
        # np.abs(): nilai absolut untuk mendapatkan magnitude
        # 20 * np.log(): konversi ke skala logaritmik untuk visualisasi lebih baik
        # +1: untuk menghindari log(0)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        
        # Normalisasi untuk display (0-255)
        magnitude_spectrum = np.clip(magnitude_spectrum, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(magnitude_spectrum)
        self.display_images()
    
    # ========== COLOR OPERATIONS ==========
    # Method untuk konversi ke Binary
    def color_binary(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_binary(val):
            # Konversi ke grayscale
            img_gray = np.array(self.original_image.convert("L"))
            
            # Thresholding untuk binary
            _, result = cv2.threshold(img_gray, int(val), 255, cv2.THRESH_BINARY)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider threshold untuk binary
        result = self.create_slider_dialog("Binary", "Threshold: 0-255", 0, 255, 127, 1, preview_binary)
        
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"))
            _, final_result = cv2.threshold(img_gray, int(result['value']), 255, cv2.THRESH_BINARY)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk konversi ke Grayscale
    def color_grayscale(self):
        if not self.check_image_loaded(): return
        
        # convert("L"): konversi ke grayscale (Luminance)
        # PIL otomatis menghitung weighted average: 0.299R + 0.587G + 0.114B
        self.processed_image = self.original_image.convert("L")
        
        self.display_images()
    
    # Method untuk konversi ke RGB
    def color_rgb(self):
        if not self.check_image_loaded(): return
        
        # convert("RGB"): konversi ke RGB (Red Green Blue)
        # Memastikan gambar dalam format RGB standar
        self.processed_image = self.original_image.convert("RGB")
        
        self.display_images()
    
    # Method untuk konversi ke HSV
    def color_hsv(self):
        if not self.check_image_loaded(): return
        
        # Konversi gambar ke numpy array RGB
        img_rgb = np.array(self.original_image.convert("RGB"))
        
        # cv2.cvtColor(): fungsi konversi color space OpenCV
        # COLOR_RGB2HSV: konversi dari RGB ke HSV (Hue Saturation Value)
        # HSV lebih intuitif untuk manipulasi warna
        img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        
        self.processed_image = Image.fromarray(img_hsv)
        self.display_images()
    
    # Method untuk konversi ke CMY
    def color_cmy(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke RGB dan normalisasi ke range 0-1
        img_rgb = np.array(self.original_image.convert("RGB"), dtype=np.float32) / 255.0
        
        # CMY = 1 - RGB
        # C (Cyan) = 1 - R
        # M (Magenta) = 1 - G
        # Y (Yellow) = 1 - B
        img_cmy = 1.0 - img_rgb
        
        # Konversi kembali ke range 0-255
        img_cmy = (img_cmy * 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(img_cmy)
        self.display_images()
    
    # Method untuk konversi ke YUV
    def color_yuv(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke numpy array RGB
        img_rgb = np.array(self.original_image.convert("RGB"))
        
        # cv2.cvtColor(): konversi RGB ke YUV
        # YUV: Y (luminance), U dan V (chrominance)
        # Digunakan dalam kompresi video (JPEG, MPEG)
        img_yuv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YUV)
        
        self.processed_image = Image.fromarray(img_yuv)
        self.display_images()
    
    # Method untuk konversi ke YIQ
    def color_yiq(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke RGB dan normalisasi
        img_rgb = np.array(self.original_image.convert("RGB"), dtype=np.float32) / 255.0
        
        # Transformation matrix RGB to YIQ
        # YIQ: digunakan di sistem TV analog NTSC
        # Y = luminance, I dan Q = chrominance
        transform_matrix = np.array([[0.299, 0.587, 0.114],
                                    [0.596, -0.275, -0.321],
                                    [0.212, -0.523, 0.311]])
        
        # np.dot(): perkalian matrix
        # Mengaplikasikan transformation matrix ke setiap pixel
        # .T: transpose matrix
        img_yiq = np.dot(img_rgb, transform_matrix.T)
        
        # Clip dan konversi kembali ke 0-255
        img_yiq = np.clip(img_yiq * 255, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(img_yiq)
        self.display_images()
    
    # Method untuk konversi ke Pseudocolor
    def color_pseudo(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale
        img_gray = np.array(self.original_image.convert("L"))
        
        # cv2.applyColorMap(): aplikasikan colormap ke grayscale
        # COLORMAP_JET: colormap jet (biru-cyan-hijau-kuning-merah)
        # Memberi warna pada gambar grayscale untuk visualisasi lebih baik
        img_colored = cv2.applyColorMap(img_gray, cv2.COLORMAP_JET)
        
        # Konversi dari BGR (OpenCV) ke RGB (PIL)
        img_colored = cv2.cvtColor(img_colored, cv2.COLOR_BGR2RGB)
        
        self.processed_image = Image.fromarray(img_colored)
        self.display_images()
    
    # ========== ENHANCEMENT OPERATIONS ==========
    # Method untuk mengatur brightness (kecerahan)
    def enhance_brightness(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview brightness
        def preview_brightness(val):
            # ImageEnhance.Brightness: enhancer untuk brightness
            # val < 1.0: lebih gelap
            # val = 1.0: tidak berubah
            # val > 1.0: lebih terang
            enhancer = ImageEnhance.Brightness(self.original_image)
            result = enhancer.enhance(val)
            
            self.temp_image = result
            self.display_temp_image()
        
        # Slider brightness 0.1-3.0, default 1.0, step 0.1
        result = self.create_slider_dialog("Brightness", "Brightness: 0.1-3.0", 0.1, 3.0, 1.0, 0.1, preview_brightness)
        
        if result['confirmed'] and result['value'] is not None:
            # Enhance brightness final
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.processed_image = enhancer.enhance(result['value'])
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk mengatur contrast (kontras)
    def enhance_contrast(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview contrast
        def preview_contrast(val):
            # ImageEnhance.Contrast: enhancer untuk contrast
            # val < 1.0: kontras lebih rendah
            # val = 1.0: tidak berubah
            # val > 1.0: kontras lebih tinggi
            enhancer = ImageEnhance.Contrast(self.original_image)
            result = enhancer.enhance(val)
            
            self.temp_image = result
            self.display_temp_image()
        
        # Slider contrast 0.1-3.0, default 1.0, step 0.1
        result = self.create_slider_dialog("Contrast", "Contrast: 0.1-3.0", 0.1, 3.0, 1.0, 0.1, preview_contrast)
        
        if result['confirmed'] and result['value'] is not None:
            # Enhance contrast final
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.processed_image = enhancer.enhance(result['value'])
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk histogram equalization
    def histogram_equalization(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale
        img_gray = np.array(self.original_image.convert("L"))
        
        # cv2.equalizeHist(): histogram equalization
        # Menyeimbangkan distribusi intensitas pixel
        # Meningkatkan kontras secara otomatis
        img_eq = cv2.equalizeHist(img_gray)
        
        self.processed_image = Image.fromarray(img_eq)
        self.display_images()
    
    # ========== SMOOTHING OPERATIONS ==========
    # Method untuk Lowpass Filtering (Spatial Domain)
    def smoothing_lowpass(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_lowpass(val):
            # Kernel size untuk filter
            kernel_size = int(val)
            
            # Kernel size harus ganjil
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            # Konversi gambar ke numpy array
            img_array = np.array(self.original_image)
            
            # cv2.blur(): averaging/mean filter
            # (kernel_size, kernel_size): ukuran kernel
            # Filter ini merata-ratakan pixel dengan tetangganya
            result = cv2.blur(img_array, (kernel_size, kernel_size))
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider kernel size 1-31, default 5, step 2
        result = self.create_slider_dialog("Lowpass Filter", "Kernel Size: 1-31", 1, 31, 5, 2, preview_lowpass)
        
        if result['confirmed'] and result['value'] is not None:
            kernel_size = int(result['value'])
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            img_array = np.array(self.original_image)
            final_result = cv2.blur(img_array, (kernel_size, kernel_size))
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk Median Filtering
    def smoothing_median(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_median(val):
            kernel_size = int(val)
            
            # Kernel size harus ganjil
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            img_array = np.array(self.original_image)
            
            # cv2.medianBlur(): median filter
            # Mengganti setiap pixel dengan median dari tetangganya
            # Sangat efektif untuk menghilangkan salt-and-pepper noise
            result = cv2.medianBlur(img_array, kernel_size)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider kernel size 1-31, default 5, step 2
        result = self.create_slider_dialog("Median Filter", "Kernel Size: 1-31", 1, 31, 5, 2, preview_median)
        
        if result['confirmed'] and result['value'] is not None:
            kernel_size = int(result['value'])
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            img_array = np.array(self.original_image)
            final_result = cv2.medianBlur(img_array, kernel_size)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk ILPF (Ideal Lowpass Filter)
    def smoothing_ilpf(self):
        """Ideal Lowpass Filter in Frequency Domain"""
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_ilpf(val):
            # Konversi ke grayscale float32
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            # FFT: transformasi ke domain frekuensi
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            # Ambil ukuran gambar
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2  # Pusat gambar
            
            # Create ILPF mask
            # Mask berbentuk lingkaran dengan radius val
            mask = np.zeros((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    # Hitung jarak dari pusat
                    # Jika jarak <= cutoff frequency (val), pass (1)
                    # Jika jarak > cutoff frequency, reject (0)
                    if np.sqrt((i - crow)**2 + (j - ccol)**2) <= val:
                        mask[i, j] = 1
            
            # Apply filter dengan mengalikan mask
            fshift_filtered = fshift * mask
            
            # IFFT: transformasi kembali ke domain spasial
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)  # Ambil magnitude
            
            # Clip dan konversi tipe data
            result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider cutoff frequency 1-200, default 30, step 1
        result = self.create_slider_dialog("ILPF", "Cutoff Frequency: 1-200", 1, 200, 30, 1, preview_ilpf)
        
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            mask = np.zeros((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    if np.sqrt((i - crow)**2 + (j - ccol)**2) <= result['value']:
                        mask[i, j] = 1
            
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            final_result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk BLPF (Butterworth Lowpass Filter)
    def smoothing_blpf(self):
        """Butterworth Lowpass Filter"""
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_blpf(val):
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            # Create BLPF mask
            # Butterworth filter: transisi lebih smooth dari ILPF
            # Formula: H(u,v) = 1 / (1 + (D(u,v) / D0)^(2n))
            # D(u,v) = jarak dari pusat
            # D0 = cutoff frequency (val)
            # n = order (2 dalam kasus ini)
            mask = np.zeros((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    d = np.sqrt((i - crow)**2 + (j - ccol)**2)  # Jarak dari pusat
                    mask[i, j] = 1 / (1 + (d / val)**(2 * 2))  # order = 2
            
            # Apply filter
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider cutoff frequency 1-200, default 30, step 1
        result = self.create_slider_dialog("BLPF", "Cutoff Frequency: 1-200", 1, 200, 30, 1, preview_blpf)
        
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            mask = np.zeros((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    d = np.sqrt((i - crow)**2 + (j - ccol)**2)
                    mask[i, j] = 1 / (1 + (d / result['value'])**(2 * 2))
            
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            final_result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # ========== SHARPENING OPERATIONS ==========
    # Method untuk Highpass Filtering (Spatial Domain)
    def sharpening_highpass(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_highpass(val):
            # Hitung strength dari slider
            strength = val / 100.0
            
            # Kernel highpass untuk edge enhancement
            # Kernel ini mendeteksi perubahan intensitas (edges)
            kernel = np.array([[-1, -1, -1],
                              [-1,  8, -1],
                              [-1, -1, -1]]) * strength
            
            # Konversi ke grayscale
            img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            # Konvolusi dengan kernel
            result = ndimage.convolve(img_array, kernel)
            result = np.clip(result, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider strength 0-200%, default 100%, step 1
        result = self.create_slider_dialog("Highpass", "Strength: 0-200%", 0, 200, 100, 1, preview_highpass)
        
        if result['confirmed'] and result['value'] is not None:
            strength = result['value'] / 100.0
            kernel = np.array([[-1, -1, -1],
                              [-1,  8, -1],
                              [-1, -1, -1]]) * strength
            
            img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
            final_result = ndimage.convolve(img_array, kernel)
            final_result = np.clip(final_result, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk Highboost Filtering
    def sharpening_highboost(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_highboost(val):
            # A = Amplification factor
            A = val
            
            # Konversi ke grayscale
            img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            # Blur gambar untuk mendapatkan komponen lowpass
            blurred = cv2.GaussianBlur(img_array, (5, 5), 0)
            
            # Highboost = A * original - blurred
            # A > 1: amplifikasi detail
            # Highboost mempertahankan detail original sambil meningkatkan edges
            result = A * img_array - blurred
            result = np.clip(result, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider amplification 1.0-5.0, default 1.5, step 0.1
        result = self.create_slider_dialog("Highboost", "Amplification: 1.0-5.0", 1.0, 5.0, 1.5, 0.1, preview_highboost)
        
        if result['confirmed'] and result['value'] is not None:
            A = result['value']
            img_array = np.array(self.original_image.convert("L"), dtype=np.float32)
            blurred = cv2.GaussianBlur(img_array, (5, 5), 0)
            final_result = A * img_array - blurred
            final_result = np.clip(final_result, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk IHPF (Ideal Highpass Filter)
    def sharpening_ihpf(self):
        """Ideal Highpass Filter"""
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_ihpf(val):
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            # Create IHPF mask (inverse of ILPF)
            # Mask berbentuk lingkaran terbalik
            mask = np.ones((rows, cols), dtype=np.float32)  # Mulai dengan 1 (pass semua)
            for i in range(rows):
                for j in range(cols):
                    # Jika jarak <= cutoff frequency, reject (0)
                    # Jika jarak > cutoff frequency, pass (1)
                    # Kebalikan dari ILPF
                    if np.sqrt((i - crow)**2 + (j - ccol)**2) <= val:
                        mask[i, j] = 0
            
            # Apply filter
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider cutoff frequency 1-200, default 30, step 1
        result = self.create_slider_dialog("IHPF", "Cutoff Frequency: 1-200", 1, 200, 30, 1, preview_ihpf)
        
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            mask = np.ones((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    if np.sqrt((i - crow)**2 + (j - ccol)**2) <= result['value']:
                        mask[i, j] = 0
            
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            final_result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk BHPF (Butterworth Highpass Filter)
    def sharpening_bhpf(self):
        """Butterworth Highpass Filter"""
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_bhpf(val):
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            # Create BHPF mask (inverse of BLPF)
            # Formula: H(u,v) = 1 / (1 + (D0 / D(u,v))^(2n))
            # Kebalikan dari BLPF (cutoff frequency di pembilang, bukan penyebut)
            mask = np.zeros((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    d = np.sqrt((i - crow)**2 + (j - ccol)**2)
                    
                    # Handle pembagian dengan nol di pusat
                    if d == 0:
                        mask[i, j] = 0
                    else:
                        mask[i, j] = 1 / (1 + (val / d)**(2 * 2))
            
            # Apply filter
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider cutoff frequency 1-200, default 30, step 1
        result = self.create_slider_dialog("BHPF", "Cutoff Frequency: 1-200", 1, 200, 30, 1, preview_bhpf)
        
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
            
            f = fft2(img_gray)
            fshift = fftshift(f)
            
            rows, cols = img_gray.shape
            crow, ccol = rows // 2, cols // 2
            
            mask = np.zeros((rows, cols), dtype=np.float32)
            for i in range(rows):
                for j in range(cols):
                    d = np.sqrt((i - crow)**2 + (j - ccol)**2)
                    if d == 0:
                        mask[i, j] = 0
                    else:
                        mask[i, j] = 1 / (1 + (result['value'] / d)**(2 * 2))
            
            fshift_filtered = fshift * mask
            f_ishift = ifftshift(fshift_filtered)
            img_back = ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            final_result = np.clip(img_back, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk Geometric Correction
    def geometric_correction(self):
        if not self.check_image_loaded(): return
        
        # Placeholder untuk fitur geometric correction
        # Fitur ini belum diimplementasikan
        messagebox.showinfo("Info", "Geometric Correction feature - Coming soon!")
    
    # ========== NOISE OPERATIONS ==========
    # Method untuk menambahkan Gaussian Noise
    def noise_gaussian(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_gaussian(val):
            # Konversi gambar ke numpy array float32
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # np.random.normal(): generate noise dengan distribusi Gaussian/Normal
            # mean = 0, std = val (standard deviation)
            # Gaussian noise: noise paling umum di alam
            noise = np.random.normal(0, val, img_array.shape)
            
            # Tambahkan noise ke gambar
            noisy = img_array + noise
            
            # Clip dan konversi tipe data
            result = np.clip(noisy, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider standard deviation 0-50, default 10, step 1
        result = self.create_slider_dialog("Gaussian Noise", "Standard Deviation: 0-50", 0, 50, 10, 1, preview_gaussian)
        
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            noise = np.random.normal(0, result['value'], img_array.shape)
            noisy = img_array + noise
            final_result = np.clip(noisy, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk menambahkan Rayleigh Noise
    def noise_rayleigh(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_rayleigh(val):
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # np.random.rayleigh(): generate noise dengan distribusi Rayleigh
            # scale = val (parameter scale)
            # Rayleigh noise: sering muncul di imaging radar
            noise = np.random.rayleigh(val, img_array.shape)
            
            noisy = img_array + noise
            result = np.clip(noisy, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider scale 0-30, default 10, step 1
        result = self.create_slider_dialog("Rayleigh Noise", "Scale: 0-30", 0, 30, 10, 1, preview_rayleigh)
        
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            noise = np.random.rayleigh(result['value'], img_array.shape)
            noisy = img_array + noise
            final_result = np.clip(noisy, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk menambahkan Erlang (Gamma) Noise
    def noise_erlang(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_erlang(val):
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # np.random.gamma(): generate noise dengan distribusi Gamma
            # shape=2 (untuk Erlang distribution), scale=val
            # Erlang: special case dari Gamma distribution
            noise = np.random.gamma(2, val, img_array.shape)  # shape=2 for Erlang
            
            noisy = img_array + noise
            result = np.clip(noisy, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider scale 0-20, default 5, step 1
        result = self.create_slider_dialog("Erlang Noise", "Scale: 0-20", 0, 20, 5, 1, preview_erlang)
        
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            noise = np.random.gamma(2, result['value'], img_array.shape)
            noisy = img_array + noise
            final_result = np.clip(noisy, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk menambahkan Exponential Noise
    def noise_exponential(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_exponential(val):
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # np.random.exponential(): generate noise dengan distribusi Exponential
            # scale=val (parameter scale = 1/lambda)
            # Exponential noise: digunakan untuk modeling laser imaging
            noise = np.random.exponential(val, img_array.shape)
            
            noisy = img_array + noise
            result = np.clip(noisy, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider scale 0-20, default 5, step 1
        result = self.create_slider_dialog("Exponential Noise", "Scale: 0-20", 0, 20, 5, 1, preview_exponential)
        
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            noise = np.random.exponential(result['value'], img_array.shape)
            noisy = img_array + noise
            final_result = np.clip(noisy, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk menambahkan Uniform Noise
    def noise_uniform(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_uniform(val):
            img_array = np.array(self.original_image, dtype=np.float32)
            
            # np.random.uniform(): generate noise dengan distribusi Uniform
            # low=-val, high=val (range noise)
            # Uniform noise: setiap nilai dalam range memiliki probabilitas sama
            noise = np.random.uniform(-val, val, img_array.shape)
            
            noisy = img_array + noise
            result = np.clip(noisy, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider range 0-50, default 20, step 1
        result = self.create_slider_dialog("Uniform Noise", "Range: 0-50", 0, 50, 20, 1, preview_uniform)
        
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image, dtype=np.float32)
            noise = np.random.uniform(-result['value'], result['value'], img_array.shape)
            noisy = img_array + noise
            final_result = np.clip(noisy, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk menambahkan Impulse Noise (Salt and Pepper)
    def noise_impulse(self):
        """Salt and Pepper Noise"""
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_impulse(val):
            # Copy gambar ke numpy array
            img_array = np.array(self.original_image).copy()
            
            # Hitung probabilitas dari slider (0-50%)
            prob = val / 100.0
            
            # Salt noise (white pixels = 255)
            # np.random.random(): generate angka random 0-1
            # Jika random < prob/2, set pixel jadi putih (salt)
            salt = np.random.random(img_array.shape[:2]) < prob / 2
            img_array[salt] = 255
            
            # Pepper noise (black pixels = 0)
            # Jika random < prob/2, set pixel jadi hitam (pepper)
            pepper = np.random.random(img_array.shape[:2]) < prob / 2
            img_array[pepper] = 0
            
            self.temp_image = Image.fromarray(img_array)
            self.display_temp_image()
        
        # Slider probability 0-50%, default 5%, step 1
        result = self.create_slider_dialog("Impulse Noise", "Probability: 0-50%", 0, 50, 5, 1, preview_impulse)
        
        if result['confirmed'] and result['value'] is not None:
            img_array = np.array(self.original_image).copy()
            prob = result['value'] / 100.0
            
            # Tambahkan salt noise
            salt = np.random.random(img_array.shape[:2]) < prob / 2
            img_array[salt] = 255
            
            # Tambahkan pepper noise
            pepper = np.random.random(img_array.shape[:2]) < prob / 2
            img_array[pepper] = 0
            
            self.processed_image = Image.fromarray(img_array)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # ========== EDGE DETECTION ==========
    # Method untuk Sobel Edge Detection
    def edge_sobel(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale
        img_gray = np.array(self.original_image.convert("L"))
        
        # Sobel operators (deteksi edge dengan turunan pertama)
        # cv2.Sobel(): fungsi Sobel OpenCV
        # CV_64F: tipe data float64 untuk hasil
        # 1, 0: turunan order 1 di X, order 0 di Y (gradient horizontal)
        # ksize=3: ukuran kernel 3x3
        sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
        
        # 0, 1: turunan order 0 di X, order 1 di Y (gradient vertikal)
        sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Magnitude: gabungkan gradient X dan Y
        # Formula: magnitude = sqrt(Gx^2 + Gy^2)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        
        # Clip dan konversi tipe data
        sobel = np.clip(sobel, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(sobel)
        self.display_images()
    
    # Method untuk Prewitt Edge Detection
    def edge_prewitt(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale float32
        img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
        
        # Prewitt kernels (mirip Sobel tapi koefisien berbeda)
        # Kernel X (gradient horizontal)
        kernel_x = np.array([[-1, 0, 1],
                            [-1, 0, 1],
                            [-1, 0, 1]])
        
        # Kernel Y (gradient vertikal)
        kernel_y = np.array([[-1, -1, -1],
                            [0, 0, 0],
                            [1, 1, 1]])
        
        # Konvolusi dengan kernel
        prewitt_x = ndimage.convolve(img_gray, kernel_x)
        prewitt_y = ndimage.convolve(img_gray, kernel_y)
        
        # Hitung magnitude
        prewitt = np.sqrt(prewitt_x**2 + prewitt_y**2)
        prewitt = np.clip(prewitt, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(prewitt)
        self.display_images()
    
    # Method untuk Robert Edge Detection
    def edge_robert(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale float32
        img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
        
        # Roberts kernels (kernel 2x2, lebih sederhana)
        # Kernel X (gradient diagonal)
        kernel_x = np.array([[1, 0],
                            [0, -1]])
        
        # Kernel Y (gradient diagonal lain)
        kernel_y = np.array([[0, 1],
                            [-1, 0]])
        
        # Konvolusi
        robert_x = ndimage.convolve(img_gray, kernel_x)
        robert_y = ndimage.convolve(img_gray, kernel_y)
        
        # Hitung magnitude
        robert = np.sqrt(robert_x**2 + robert_y**2)
        robert = np.clip(robert, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(robert)
        self.display_images()
    
    # Method untuk Laplacian Edge Detection
    def edge_laplacian(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale
        img_gray = np.array(self.original_image.convert("L"))
        
        # cv2.Laplacian(): operator Laplacian (turunan kedua)
        # CV_64F: tipe data float64
        # Laplacian mendeteksi region dengan perubahan intensitas cepat
        laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
        
        # np.absolute(): ambil nilai absolut (edge bisa positif/negatif)
        laplacian = np.absolute(laplacian)
        laplacian = np.clip(laplacian, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(laplacian)
        self.display_images()
    
    # Method untuk LoG (Laplacian of Gaussian) Edge Detection
    def edge_log(self):
        """Laplacian of Gaussian"""
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_log(val):
            kernel_size = int(val)
            
            # Kernel size harus ganjil
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            # Konversi ke grayscale
            img_gray = np.array(self.original_image.convert("L"))
            
            # Step 1: Apply Gaussian blur untuk reduce noise
            # LoG = Laplacian of Gaussian (blur dulu baru Laplacian)
            blurred = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)
            
            # Step 2: Apply Laplacian
            log = cv2.Laplacian(blurred, cv2.CV_64F)
            log = np.absolute(log)
            result = np.clip(log, 0, 255).astype(np.uint8)
            
            self.temp_image = Image.fromarray(result)
            self.display_temp_image()
        
        # Slider kernel size 1-15, default 5, step 2
        result = self.create_slider_dialog("LoG", "Kernel Size: 1-15", 1, 15, 5, 2, preview_log)
        
        if result['confirmed'] and result['value'] is not None:
            kernel_size = int(result['value'])
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            img_gray = np.array(self.original_image.convert("L"))
            blurred = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)
            log = cv2.Laplacian(blurred, cv2.CV_64F)
            log = np.absolute(log)
            final_result = np.clip(log, 0, 255).astype(np.uint8)
            
            self.processed_image = Image.fromarray(final_result)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk Canny Edge Detection
    def edge_canny(self):
        if not self.check_image_loaded(): return
        
        # Inner function untuk preview
        def preview_canny(val):
            # Konversi ke grayscale
            img_gray = np.array(self.original_image.convert("L"))
            
            # cv2.Canny(): algoritma Canny edge detection
            # val: lower threshold
            # val * 2: upper threshold (ratio 1:2 recommended)
            # Canny menggunakan multi-stage algorithm:
            # 1. Gaussian blur
            # 2. Gradient calculation (Sobel)
            # 3. Non-maximum suppression
            # 4. Double thresholding
            # 5. Edge tracking by hysteresis
            edges = cv2.Canny(img_gray, val, val * 2)
            
            self.temp_image = Image.fromarray(edges)
            self.display_temp_image()
        
        # Slider lower threshold 0-255, default 50, step 1
        result = self.create_slider_dialog("Canny", "Lower Threshold: 0-255", 0, 255, 50, 1, preview_canny)
        
        if result['confirmed'] and result['value'] is not None:
            img_gray = np.array(self.original_image.convert("L"))
            edges = cv2.Canny(img_gray, int(result['value']), int(result['value'] * 2))
            self.processed_image = Image.fromarray(edges)
        else:
            self.processed_image = self.original_image.copy()
        
        self.display_images()
    
    # Method untuk Compass Edge Detection (Kirsch)
    def edge_compass(self):
        """Compass Edge Detection (Kirsch)"""
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale float32
        img_gray = np.array(self.original_image.convert("L"), dtype=np.float32)
        
        # Kirsch compass masks (8 directions)
        # 8 kernel untuk mendeteksi edge di 8 arah berbeda
        # N, NE, E, SE, S, SW, W, NW
        kernels = [
            np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),      # N
            np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),     # NE
            np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),     # E
            np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),     # SE
            np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),     # S
            np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),     # SW
            np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),     # W
            np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]])      # NW
        ]
        
        # Apply all kernels and take maximum response
        # Konvolusi gambar dengan semua 8 kernel
        responses = [np.absolute(ndimage.convolve(img_gray, kernel)) for kernel in kernels]
        
        # np.maximum.reduce(): ambil nilai maksimum dari semua response
        # Mengambil edge dengan respon terkuat dari 8 arah
        compass = np.maximum.reduce(responses)
        compass = np.clip(compass, 0, 255).astype(np.uint8)
        
        self.processed_image = Image.fromarray(compass)
        self.display_images()
    
    # ========== SEGMENTATION ==========
    # Method untuk Region Growing Segmentation
    def segmentation_region_growing(self):
        """Region Growing Segmentation dengan seed point selection"""
        if not self.check_image_loaded(): return
        
        # Konversi ke grayscale
        img_gray = np.array(self.original_image.convert("L"))
        
        # Dialog untuk memilih threshold
        # Threshold: beda intensitas maksimal yang masih dianggap satu region
        threshold = simpledialog.askinteger("Region Growing", 
                                           "Enter threshold (0-50):", 
                                           initialvalue=10, minvalue=0, maxvalue=50)
        if threshold is None:
            return
        
        # Info ke user tentang seed point
        messagebox.showinfo("Region Growing", 
                          "Click on the image to select seed point.\nMiddle of the image will be used as default.")
        
        # Gunakan titik tengah sebagai seed point default
        # seed point = titik awal pertumbuhan region
        seed_x, seed_y = img_gray.shape[1] // 2, img_gray.shape[0] // 2
        
        # Implementasi region growing
        h, w = img_gray.shape  # tinggi dan lebar
        segmented = np.zeros((h, w), dtype=np.uint8)  # hasil segmentasi
        visited = np.zeros((h, w), dtype=bool)  # track pixel yang sudah dikunjungi
        
        # Ambil nilai intensitas seed point
        seed_value = int(img_gray[seed_y, seed_x])
        
        # Stack untuk BFS/DFS (Breadth/Depth First Search)
        # Mulai dari seed point
        stack = [(seed_x, seed_y)]
        visited[seed_y, seed_x] = True
        
        # Loop sampai stack kosong
        while stack:
            # Pop pixel dari stack
            x, y = stack.pop()
            
            # Mark pixel ini sebagai bagian dari region (255 = putih)
            segmented[y, x] = 255
            
            # Check 4-connected neighbors (atas, bawah, kiri, kanan)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy  # neighbor coordinates
                
                # Cek apakah neighbor valid dan belum dikunjungi
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    # Cek apakah perbedaan intensitas <= threshold
                    if abs(int(img_gray[ny, nx]) - seed_value) <= threshold:
                        # Tambahkan ke stack untuk diproses
                        stack.append((nx, ny))
                        visited[ny, nx] = True
        
        self.processed_image = Image.fromarray(segmented)
        self.display_images()
    
    # Method untuk Watershed Segmentation
    def segmentation_watershed(self):
        if not self.check_image_loaded(): return
        
        # Konversi ke numpy array RGB
        img_array = np.array(self.original_image.convert("RGB"))
        
        # Konversi ke grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Step 1: Apply threshold dengan Otsu's method
        # THRESH_BINARY_INV: inverse binary (background hitam, foreground putih)
        # THRESH_OTSU: otomatis menentukan threshold optimal
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Step 2: Noise removal dengan morphological opening
        kernel = np.ones((3, 3), np.uint8)
        # Opening = erosion diikuti dilation (remove small noise)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Step 3: Sure background area dengan dilation
        # Dilation memperluas foreground
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Step 4: Finding sure foreground area
        # Distance transform: hitung jarak setiap pixel ke background terdekat
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        
        # Threshold distance transform (70% dari max = sure foreground)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        
        # Step 5: Finding unknown region
        # Unknown = sure background - sure foreground
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Step 6: Marker labelling
        # connectedComponents: label setiap komponen terpisah
        _, markers = cv2.connectedComponents(sure_fg)
        
        # Add 1 ke semua marker agar background bukan 0
        markers = markers + 1
        
        # Mark unknown region dengan 0
        markers[unknown == 255] = 0
        
        # Step 7: Apply watershed algorithm
        # Watershed memperlakukan gambar seperti topographic map
        # Algoritma "mengalirkan air" dari markers
        markers = cv2.watershed(img_array, markers)
        
        # Mark boundaries dengan warna merah
        # markers == -1: boundary yang ditemukan watershed
        img_array[markers == -1] = [255, 0, 0]  # Mark boundaries in red
        
        self.processed_image = Image.fromarray(img_array)
        self.display_images()
    
    # ========== ABOUT MENU ==========
    # Method untuk menampilkan info tim developer
    def show_info(self):
        # String multi-line dengan informasi aplikasi dan tim
        # Triple quotes untuk string multi-line
        info_text = """
Aplikasi Pengolahan Citra Digital
© Kelompok

Anggota Tim:
1. [Ariful Fikri]
2. [Dilfan Irfandi]
3. [Muhammad Fadhil Habibi]

Mata Kuliah: Pengolahan Citra Digital
Dosen Pengampu: [Nama Dosen]
Universitas: [Nama Universitas]

Fitur:
- Basic Operations (Arithmetic, Boolean, Geometric)
- Image Enhancement (Brightness, Contrast, Filtering)
- Noise Addition and Removal
- Edge Detection (Sobel, Prewitt, Canny, etc.)
- Image Segmentation (Region Growing, Watershed)
- Frequency Domain Processing (FFT, Filters)
- Color Space Conversions
"""
        # Tampilkan messagebox info dengan teks di atas
        messagebox.showinfo("Info Tim Developer", info_text)
    
    # Method untuk membuka link Github di browser
    def open_github(self):
        # webbrowser.open(): membuka URL di browser default
        webbrowser.open("https://github.com")
        
        # Tampilkan info bahwa Github tutorial sedang dibuka
        messagebox.showinfo("Tutorial", "Opening Github tutorial...")
    
    # Method untuk membuka link Youtube di browser
    def open_youtube(self):
        # webbrowser.open(): membuka URL di browser default
        webbrowser.open("https://youtube.com")
        
        # Tampilkan info bahwa Youtube tutorial sedang dibuka
        messagebox.showinfo("Tutorial", "Opening Youtube tutorial...")


# ========== MAIN PROGRAM ==========
# Cek apakah script ini dijalankan langsung (bukan di-import)
# __name__ == "__main__": True jika script dijalankan langsung
if __name__ == "__main__":
    # Membuat root window Tkinter
    # Tk(): membuat window utama aplikasi
    root = tk.Tk()
    
    # Membuat instance/objek dari class ImageProcessingApp
    # Passing root window sebagai parameter
    app = ImageProcessingApp(root)
    
    # Memulai event loop Tkinter
    # mainloop(): membuat window tetap terbuka dan menunggu event (klik, input, dll)
    # Program akan terus berjalan sampai window ditutup
    root.mainloop()