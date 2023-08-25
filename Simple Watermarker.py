import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk
import os

class WatermarkApp:
    def __init__(self, root):
        """
        Initializing of the watermarking app, which has three steps:
        1. Uploading Original Image to modify with watermark
        2. Uploading Watermark Image to apply for the Original Image
        3. Previewing and downloading the result
        """
        self.root = root
        self.root.title("Watermark App")
        self.root.minsize(450, 525)
        self.title_font = font.Font(weight='bold')

        self.current_step = 1
        self.placeholder_image = Image.open("img_placeholder.png")
        self.placeholder_image.thumbnail((410, 410))
        self.placeholder_image = ImageTk.PhotoImage(self.placeholder_image)

        self.image_to_modify = self.placeholder_image
        self.image_for_watermark = None
        self.original_image_path = None
        self.result_image = None

        self.create_step1_frame()
        self.create_step2_frame()
        self.create_step3_frame()

        self.show_step1()


    def create_step1_frame(self):
        self.step1_frame = tk.Frame(self.root)
        tk.Label(self.step1_frame, font=self.title_font, text="STEP 1:").pack(anchor='w')
        tk.Label(self.step1_frame, text="- Choose picture to modify").pack(anchor='w')

        # Create the "Upload Original Image" button
        tk.Button(
            self.step1_frame,
            text="Upload Original Image",
            width=41,
            command=self.upload_image_step1
        ).pack(pady=5)

        # Create a Canvas of fixed size 400x400
        self.canvas1 = tk.Canvas(self.step1_frame, width=400, height=400, highlightthickness=0)
        self.canvas1.pack()

        # Create a placeholder image on the canvas
        self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.placeholder_image)

        self.step1_next_button = tk.Button(self.step1_frame, text="Next", command=self.show_step2)
        self.step1_next_button.pack(side=tk.RIGHT)
        self.step1_next_button.config(state="disabled")  # Initially disabled

        self.step1_frame.pack()


    def create_step2_frame(self):
        self.step2_frame = tk.Frame(self.root)
        tk.Label(self.step2_frame, font=self.title_font, text="STEP 2").pack(anchor='w')
        tk.Label(self.step2_frame, text="- Choose picture for watermark").pack(anchor='w')

        # Create the "Upload Watermark Image" button
        tk.Button(
            self.step2_frame,
            text="Upload Watermark Image",
            width=41,
            command=self.upload_image_step2
            ).pack(pady=5)

        # Create a Canvas of fixed size 400x400
        self.canvas2 = tk.Canvas(self.step2_frame, width=400, height=400, highlightthickness=0)
        self.canvas2.pack()

        # Create a placeholder image on the canvas
        self.canvas2.create_image(0, 0, anchor=tk.NW, image=self.placeholder_image)

        self.step2_next_button = tk.Button(self.step2_frame, text="Next", command=self.show_step3)
        self.step2_next_button.pack(side=tk.RIGHT)
        self.step2_next_button.config(state="disabled")  # Initially disabled

        self.step2_back_button = tk.Button(self.step2_frame, text="Back", command=self.show_step1)
        self.step2_back_button.pack(side=tk.LEFT)


    def create_step3_frame(self):
        self.step3_frame = tk.Frame(self.root)
        tk.Label(self.step3_frame, font=self.title_font, text="STEP 3").pack(anchor='w')
        tk.Label(self.step3_frame, text="- Check the result below and confirm").pack(anchor='w')
        tk.Button(
            self.step3_frame,
            text="Download Watermarked Image",
            width=41,
            command=self.download_image
            ).pack(pady=5)

        # Create a Canvas of fixed size 400x400
        self.canvas3 = tk.Canvas(self.step3_frame, width=400, height=400, highlightthickness=0)
        self.canvas3.pack()

        self.step3_back_button = tk.Button(self.step3_frame, text="Back", command=self.show_step2)
        self.step3_back_button.pack(side=tk.LEFT)

        self.step3_exit_button = tk.Button(self.step3_frame, text="Quit", command=self.root.quit)
        self.step3_exit_button.pack(side=tk.RIGHT)


    def upload_image_step1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_to_modify = Image.open(file_path)
            image_to_modify_thumb = self.image_to_modify.copy()
            image_to_modify_thumb.thumbnail((400, 400))

            # Convert the image to a PhotoImage object
            self.step1_image = ImageTk.PhotoImage(image_to_modify_thumb)

            # Clear the canvas and display the uploaded image on the canvas
            self.canvas1.delete("all")
            self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.step1_image)

            self.step1_next_button.config(state="normal")

            # Store the path and original image name
            self.original_image_path = file_path


    def upload_image_step2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_for_watermark = Image.open(file_path)
            image_for_watermark_thumb = self.image_for_watermark.copy()
            image_for_watermark_thumb.thumbnail((400, 400))

            # Convert the image to a PhotoImage object
            self.step2_image = ImageTk.PhotoImage(image_for_watermark_thumb)

            # Clear the canvas and display the uploaded image on the canvas
            self.canvas2.delete("all")
            self.canvas2.create_image(0, 0, anchor=tk.NW, image=self.step2_image)

            self.step2_next_button.config(state="normal")


    def show_step1(self):
        self.step2_frame.pack_forget()
        self.step3_frame.pack_forget()
        self.step1_frame.pack()
        self.current_step = 1
        self.step2_back_button.config(state="disabled")
        self.step3_back_button.config(state="disabled")

    def show_step2(self):
        self.step1_frame.pack_forget()
        self.step3_frame.pack_forget()
        self.step2_frame.pack()
        self.current_step = 2
        self.step1_next_button.config(state="normal")
        self.step2_back_button.config(state="normal")
        self.step3_back_button.config(state="disabled")

    def show_step3(self):
        self.step1_frame.pack_forget()
        self.step2_frame.pack_forget()
        self.step3_frame.pack()
        self.current_step = 3
        self.step2_next_button.config(state="disabled")
        self.step3_back_button.config(state="normal")

        # Generate the watermarked image
        if self.image_to_modify and self.image_for_watermark:
            # Create a copy of the original image to avoid modifying the original
            self.watermarked_image = self.image_to_modify.copy()

            # Calculate the position to paste the watermark
            width, height = self.watermarked_image.size
            watermark_width, watermark_height = self.image_for_watermark.size
            paste_x = (width - watermark_width) // 2
            paste_y = (height - watermark_height) // 2

            # Paste the watermark onto the result image
            self.watermarked_image.paste(self.image_for_watermark, (paste_x, paste_y), self.image_for_watermark)

            watermarked_image_thumb = self.watermarked_image.copy()
            watermarked_image_thumb.thumbnail((400, 400))

            # Convert the result image to PhotoImage for display
            self.step3_image = ImageTk.PhotoImage(watermarked_image_thumb)
            self.result_image = self.watermarked_image

            # Update the image label in Step 3 with the result image
            self.canvas3.delete("all")
            self.canvas3.create_image(0, 0, anchor=tk.NW, image=self.step3_image)


    def download_image(self):
        if self.image_to_modify and self.image_for_watermark:
            # Get the directory and name of the original image
            if self.original_image_path:
                dir_name, file_name = os.path.split(self.original_image_path)
                # Modify the file name to include "_watermarked"
                base_name, ext = os.path.splitext(file_name)
                result_file_name = base_name + "_watermarked" + ext

                # Create the path for the watermarked image
                result_image_path = os.path.join(dir_name, result_file_name)

                # Save the watermarked image with the modified name
                self.result_image.save(result_image_path)

                # Show a message box with the save location
                tk.messagebox.showinfo("Save Successful", f"Image saved to:\n{result_image_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
