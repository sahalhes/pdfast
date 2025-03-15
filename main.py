from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

def create_pdf(c_files, image_files, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    margin = 50
    line_height = 12
    y_position = height - 50
    
    title_font = "Helvetica-Bold"
    title_size = 14
    code_font = "Courier"
    code_size = 10
    
    for c_file in c_files:
        with open(c_file, "r") as f:
            code = f.read()
        
        c.setFont(title_font, title_size)
        c.drawString(margin, y_position, os.path.basename(c_file))
        y_position -= 20
        
        c.setFont(code_font, code_size)
        
        for line in code.split("\n"):
            if y_position < 100:  
                c.showPage()
                c.setFont(code_font, code_size)
                y_position = height - 50
            c.drawString(margin, y_position, line)
            y_position -= line_height
        
        y_position -= 30
        
        if y_position < height/2:
            c.showPage()
            c.setFont(code_font, code_size)
            y_position = height - 50
    
    for image_file in image_files:
        if os.path.exists(image_file):
            if y_position < height/2:
                c.showPage()
                c.setFont(code_font, code_size)
                y_position = height - 50
            
            img = Image.open(image_file)
            img_width, img_height = img.size
            aspect = img_width / float(img_height)
            
            max_width = width - (2 * margin)
            max_height = y_position - margin
            
            if img_width > max_width:
                img_width = max_width
                img_height = img_width / aspect
            
            if img_height > max_height:
                img_height = max_height
                img_width = img_height * aspect
            
            c.drawImage(
                ImageReader(img), 
                margin, 
                y_position - img_height, 
                width=img_width, 
                height=img_height,
                preserveAspectRatio=True
            )
            
            y_position = y_position - img_height - 30
    
    c.save()


#main.py should be on same folder of .c and .png
c_files = ["24.c"]  # put comma to include multiple c files like ["1.c", "2.c"]
image_files = ["24.png"]  # put comma to include multiple image files  ["1.png", "2.png"]
create_pdf(c_files, image_files, "24.pdf")