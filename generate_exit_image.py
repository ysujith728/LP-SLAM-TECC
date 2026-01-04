from PIL import Image, ImageDraw, ImageFont

# Create a blank red background
img = Image.new("RGB", (600, 300), color=(180, 0, 0))
draw = ImageDraw.Draw(img)

# Add EXIT text
draw.text((150, 100), "EXIT", fill="white", size=120)

# Save image
img.save("exit.jpg")

print("✔ exit.jpg created successfully!")
