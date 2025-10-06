import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import ImageGrab, Image, ImageTk, ImageDraw
import os
from datetime import datetime
import keyboard
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image as PILImage
import sys

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Manager")
        self.root.geometry("900x700")
        
        # Modern color scheme
        self.colors = {
            'bg': '#1e1e2e',  # Dark background
            'fg': '#cdd6f4',  # Light text
            'accent': '#89b4fa',  # Blue accent
            'button_bg': '#313244',  # Button background
            'button_hover': '#45475a',  # Button hover
            'button_active': '#585b70',  # Button active
            'canvas_bg': '#181825',  # Canvas background
            'success': '#a6e3a1',  # Green
            'warning': '#f9e2af',  # Yellow
            'error': '#f38ba8',  # Red
            'refresh': '#89dceb',  # Cyan
            'rename': '#f5c2e7',  # Pink
            'delete': '#eba0ac',  # Maroon
            'folder': '#fab387'  # Orange
        }
        
        # Apply theme to root
        self.root.configure(bg=self.colors['bg'])
        
        # Screenshot folder
        self.screenshot_folder = r"C:\Screenshot"
        self.create_screenshot_folder()
        
        # Variables
        self.current_preview = None
        self.preview_photo = None
        self.icon = None
        self.button_icons = {}
        
        # Create button icons
        self.create_button_icons()
        
        # Setup GUI
        self.setup_gui()
        
        # Setup menu bar
        self.setup_menu()
        
        # Load existing screenshots
        self.refresh_file_list()
        
        # Register global hotkey for PrintScreen
        self.setup_hotkey()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
    def create_screenshot_folder(self):
        """Create screenshot folder if it doesn't exist"""
        if not os.path.exists(self.screenshot_folder):
            try:
                os.makedirs(self.screenshot_folder)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create folder: {str(e)}")
                
    def create_button_icons(self):
        """Create icons for buttons"""
        # Icon size
        icon_size = 24
        
        # Refresh icon (circular arrow)
        refresh_img = PILImage.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
        # Simple representation - we'll use text-based icons
        
        # Rename icon (pencil/edit)
        rename_img = PILImage.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
        
        # Delete icon (X or trash)
        delete_img = PILImage.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
        
        # Folder icon
        folder_img = PILImage.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
        
        # Convert to PhotoImage
        self.button_icons['refresh'] = ImageTk.PhotoImage(refresh_img)
        self.button_icons['rename'] = ImageTk.PhotoImage(rename_img)
        self.button_icons['delete'] = ImageTk.PhotoImage(delete_img)
        self.button_icons['folder'] = ImageTk.PhotoImage(folder_img)
        
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Screenshot Manager")
        about_window.geometry("450x250")
        about_window.resizable(False, False)
        
        # Center the window
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Main frame
        frame = ttk.Frame(about_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(frame, text="Screenshot Manager", 
                               font=("Consolas", 20, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(frame, text="Version 1.0", 
                                 font=("Consolas", 14))
        version_label.pack(pady=(0, 15))
        
        # Separator
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill='x', pady=(0, 15))
        
        # Developer info
        dev_label = ttk.Label(frame, text="Developer", 
                             font=("Consolas", 12, "bold"))
        dev_label.pack(pady=(0, 8))
        
        info_text = "Designed & Developed by\nBravetux aka B.Vignesh Kumar\nic19939@gmail.com"
        info_label = ttk.Label(frame, text=info_text, 
                              font=("Consolas", 12),
                              justify=tk.CENTER)
        info_label.pack(pady=(0, 15))
        
        # Close button
        close_button = ttk.Button(frame, text="Close", 
                                 command=about_window.destroy)
        close_button.pack(pady=(10, 0))
        
        # Center the window on screen
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (about_window.winfo_width() // 2)
        y = (about_window.winfo_screenheight() // 2) - (about_window.winfo_height() // 2)
        about_window.geometry(f"+{x}+{y}")
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title Label
        title_label = tk.Label(main_frame, text="📸 Screenshot Manager", 
                               font=("Consolas", 18, "bold"),
                               bg=self.colors['bg'], fg=self.colors['accent'])
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Info Label
        info_label = tk.Label(main_frame, 
                              text="Press Ctrl+PrtSc to capture screenshot", 
                              font=("Consolas", 11),
                              bg=self.colors['bg'], fg=self.colors['fg'])
        info_label.grid(row=1, column=0, pady=(0, 10))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Configure button frame to expand
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        # Create custom styled buttons with icons
        btn_style = {
            'font': ('Consolas', 14, 'bold'),
            'width': 15,
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2',
            'activebackground': self.colors['button_active']
        }
        
        # Refresh button with icon
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh", 
                               command=self.refresh_file_list,
                               bg=self.colors['refresh'], fg='#000000',
                               **btn_style)
        refresh_btn.grid(row=0, column=0, padx=3, sticky=(tk.W, tk.E), ipady=8)
        
        # Rename button with icon
        rename_btn = tk.Button(button_frame, text="✏️ Rename", 
                              command=self.rename_file,
                              bg=self.colors['rename'], fg='#000000',
                              **btn_style)
        rename_btn.grid(row=0, column=1, padx=3, sticky=(tk.W, tk.E), ipady=8)
        
        # Delete button with icon
        delete_btn = tk.Button(button_frame, text="🗑️ Delete", 
                              command=self.delete_file,
                              bg=self.colors['delete'], fg='#000000',
                              **btn_style)
        delete_btn.grid(row=0, column=2, padx=3, sticky=(tk.W, tk.E), ipady=8)
        
        # Open Folder button with icon
        folder_btn = tk.Button(button_frame, text="📁 Open Folder", 
                              command=self.open_folder,
                              bg=self.colors['folder'], fg='#000000',
                              **btn_style)
        folder_btn.grid(row=0, column=3, padx=3, sticky=(tk.W, tk.E), ipady=8)
        
        # Create horizontal paned window
        paned_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        paned_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(3, weight=1)
        
        # Configure paned frame - left frame takes only necessary space, right gets the rest
        paned_frame.columnconfigure(0, weight=0)  # Fixed width for list
        paned_frame.columnconfigure(1, weight=1)  # Expandable for preview
        paned_frame.rowconfigure(0, weight=1)
        
        # Left frame - File list (fixed width to fit filenames)
        left_frame = tk.Frame(paned_frame, bg=self.colors['bg'], width=280)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_frame.grid_propagate(False)  # Prevent frame from shrinking
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        
        # File list label
        list_label = tk.Label(left_frame, text="📋 Screenshots", 
                              font=("Consolas", 12, "bold"),
                              bg=self.colors['bg'], fg=self.colors['accent'])
        list_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)
        
        # Listbox frame
        listbox_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(listbox_frame, bg=self.colors['button_bg'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for screenshots
        self.file_listbox = tk.Listbox(listbox_frame, 
                                       yscrollcommand=scrollbar.set,
                                       font=("Consolas", 14),
                                       bg=self.colors['button_bg'],
                                       fg=self.colors['fg'],
                                       selectbackground=self.colors['accent'],
                                       selectforeground='#000000',
                                       bd=0,
                                       highlightthickness=0)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Bind selection event
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        # Right frame - Preview
        right_frame = tk.Frame(paned_frame, bg=self.colors['bg'])
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        # Preview label
        preview_label = tk.Label(right_frame, text="🖼️ Preview", 
                                font=("Consolas", 12, "bold"),
                                bg=self.colors['bg'], fg=self.colors['accent'])
        preview_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)

        # Canvas for image preview
        self.preview_canvas = tk.Canvas(right_frame, bg=self.colors['canvas_bg'], 
                                    highlightthickness=2, 
                                    highlightbackground=self.colors['accent'])
        self.preview_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("✓ Ready - Press Ctrl+PrtSc to capture")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                             relief=tk.FLAT, anchor=tk.W,
                             bg=self.colors['button_bg'], fg=self.colors['fg'],
                             font=('Consolas', 10), padx=10, pady=5)
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def setup_hotkey(self):
        """Setup global hotkey for Ctrl+PrintScreen"""
        def on_printscreen():
            self.take_screenshot()
            
        # Run keyboard listener in separate thread
        def listen_keyboard():
            try:
                keyboard.add_hotkey('ctrl+print screen', on_printscreen)
                keyboard.wait()
            except Exception as e:
                print(f"Keyboard listener error: {str(e)}")
                
        keyboard_thread = threading.Thread(target=listen_keyboard, daemon=True)
        keyboard_thread.start()
        
    def take_screenshot(self):
        """Capture screenshot and save to folder"""
        try:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Generate filename
            timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
            filename = f"ss_{timestamp}.png"
            filepath = os.path.join(self.screenshot_folder, filename)
            
            # Save screenshot
            screenshot.save(filepath, "PNG")
            
            # Update status
            self.status_var.set(f"Screenshot saved: {filename}")
            
            # Refresh file list
            self.refresh_file_list()
            
            # Select the new file
            self.select_file_by_name(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot: {str(e)}")
            self.status_var.set("Error capturing screenshot")
            
    def refresh_file_list(self):
        """Refresh the file list"""
        self.file_listbox.delete(0, tk.END)
        
        try:
            files = [f for f in os.listdir(self.screenshot_folder) 
                    if f.endswith('.png')]
            files.sort(reverse=True)  # Most recent first
            
            for file in files:
                self.file_listbox.insert(tk.END, file)
                
            self.status_var.set(f"Found {len(files)} screenshot(s)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list files: {str(e)}")
            
    def on_file_select(self, event):
        """Handle file selection"""
        selection = self.file_listbox.curselection()
        if selection:
            filename = self.file_listbox.get(selection[0])
            self.show_preview(filename)
            
    def show_preview(self, filename):
        """Show preview of selected screenshot"""
        filepath = os.path.join(self.screenshot_folder, filename)
        
        try:
            # Load image
            image = Image.open(filepath)
            
            # Get canvas size
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # Use default size if canvas not yet rendered
            if canvas_width <= 1:
                canvas_width = 500
            if canvas_height <= 1:
                canvas_height = 500
                
            # Calculate scaling to fit canvas
            img_width, img_height = image.size
            scale = min(canvas_width / img_width, canvas_height / img_height, 1)
            new_width = int(img_width * scale * 0.95)  # 95% to add padding
            new_height = int(img_height * scale * 0.95)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_photo = ImageTk.PhotoImage(image)
            
            # Clear canvas and display image
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(canvas_width // 2, 
                                            canvas_height // 2, 
                                            image=self.preview_photo, 
                                            anchor=tk.CENTER)
            
            self.current_preview = filename
            self.status_var.set(f"Viewing: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preview: {str(e)}")
            
    def select_file_by_name(self, filename):
        """Select a file in the listbox by name"""
        for i in range(self.file_listbox.size()):
            if self.file_listbox.get(i) == filename:
                self.file_listbox.selection_clear(0, tk.END)
                self.file_listbox.selection_set(i)
                self.file_listbox.see(i)
                self.show_preview(filename)
                break
                
    def rename_file(self):
        """Rename selected file"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file to rename")
            return
            
        old_filename = self.file_listbox.get(selection[0])
        old_filepath = os.path.join(self.screenshot_folder, old_filename)
        
        # Get new filename
        new_filename = simpledialog.askstring("Rename File", 
                                             "Enter new filename (without extension):",
                                             initialvalue=old_filename.replace('.png', ''))
        
        if new_filename:
            # Add extension if not provided
            if not new_filename.endswith('.png'):
                new_filename += '.png'
                
            new_filepath = os.path.join(self.screenshot_folder, new_filename)
            
            try:
                # Check if file already exists
                if os.path.exists(new_filepath):
                    messagebox.showerror("Error", "A file with that name already exists")
                    return
                    
                # Rename file
                os.rename(old_filepath, new_filepath)
                
                # Refresh list and select renamed file
                self.refresh_file_list()
                self.select_file_by_name(new_filename)
                
                self.status_var.set(f"Renamed to: {new_filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename file: {str(e)}")
                
    def delete_file(self):
        """Delete selected file"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file to delete")
            return
            
        filename = self.file_listbox.get(selection[0])
        filepath = os.path.join(self.screenshot_folder, filename)
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{filename}'?"):
            try:
                os.remove(filepath)
                self.preview_canvas.delete("all")
                self.refresh_file_list()
                self.status_var.set(f"Deleted: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
                
    def open_folder(self):
        """Open screenshot folder in file explorer"""
        try:
            os.startfile(self.screenshot_folder)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
            
    def create_camera_icon(self):
        """Create a camera icon for system tray"""
        # Create a 64x64 image with camera icon
        img = PILImage.new('RGB', (64, 64), color=(30, 30, 46))  # Dark background
        draw = ImageDraw.Draw(img)
        
        # Camera body (rectangle)
        draw.rectangle([10, 20, 54, 50], fill=(137, 180, 250), outline=(205, 214, 244))
        
        # Camera lens (circle)
        draw.ellipse([24, 28, 40, 44], fill=(24, 24, 37), outline=(205, 214, 244))
        
        # Camera flash (small rectangle on top)
        draw.rectangle([26, 14, 32, 20], fill=(246, 194, 135))
        
        # Viewfinder (small rectangle)
        draw.rectangle([42, 24, 48, 28], fill=(24, 24, 37))
        
        return img
    
    def minimize_to_tray(self):
        """Minimize application to system tray"""
        self.root.withdraw()
        
        # Create camera icon for system tray
        icon_image = self.create_camera_icon()
        
        menu = (
            item('Restore', self.restore_from_tray),
            item('Exit', self.exit_app)
        )
        
        self.icon = pystray.Icon("screenshot_app", icon_image, 
                                "Screenshot Manager", menu)
        
        # Run icon in separate thread
        icon_thread = threading.Thread(target=self.icon.run, daemon=False)
        icon_thread.start()
        
    def restore_from_tray(self, icon=None, item=None):
        """Restore application from system tray"""
        self.root.after(0, self._restore_window)
        
    def _restore_window(self):
        """Helper method to restore window in main thread"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        if self.icon:
            self.icon.stop()
        
    def exit_app(self, icon=None, item=None):
        """Exit the application"""
        if self.icon:
            self.icon.stop()
        self.root.after(0, self._quit_app)
        
    def _quit_app(self):
        """Helper method to quit in main thread"""
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
        
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = ScreenshotApp(root)
    app.run()


if __name__ == "__main__":
    main()
