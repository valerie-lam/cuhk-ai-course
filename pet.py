import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(
    page_title="Pet Information", 
    page_icon="😺", 
    layout="wide"
)

st.title("😺 Pet Information")
st.markdown("---")

camera_photo = st.camera_input("Take Photo (Optional)")

with st.form("pet_information_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        pet_name = st.text_input("Pet Name *", placeholder="e.g. Buddy")
        pet_species = st.text_input("Pet Species *", placeholder="e.g. pomeranian")
    
    with col2:
        pet_birthday = st.text_input("Pet's Birthday *", placeholder="e.g. 1st January")
        pet_hobbies = st.text_input("Pet's hobbies *", placeholder="e.g. running")
    
    submitted = st.form_submit_button("Generate Pet Information", type="primary", use_container_width=True)

if submitted:
    if not all([pet_name, pet_species, pet_birthday, pet_hobbies]):
        st.error("Please fill in all required fields (marked with *)")
    else:
        # Create pet information
        card_width, card_height = 400, 250
        card = Image.new('RGB', (card_width, card_height), color='white')
        draw = ImageDraw.Draw(card)
        
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        
        # Draw header
        header_color = 'orange'
        draw.rectangle([(0, 0), (card_width, 70)], fill=header_color)
        draw.text((20, 25), "PET INFORMATION", fill='white', font=title_font)
        draw.text((20, 50), pet_name, fill='white', font=small_font)
        
        # Draw photo
        photo_size = 90
        photo_x, photo_y = 20, 90
        if camera_photo:
            try:
                photo = Image.open(camera_photo)
                width, height = photo.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                photo = photo.crop((left, top, left + size, top + size))
                photo = photo.resize((photo_size, photo_size))
                card.paste(photo, (photo_x, photo_y))
            except:
                draw.rectangle([(photo_x, photo_y), (photo_x + photo_size, photo_y + photo_size)], 
                             outline='#999', width=2)
                draw.text((photo_x + 25, photo_y + 35), "Photo", fill='#999', font=small_font)
        else:
            draw.rectangle([(photo_x, photo_y), (photo_x + photo_size, photo_y + photo_size)], 
                         outline='#999', width=2)
            draw.text((photo_x + 25, photo_y + 35), "Photo", fill='#999', font=small_font)
        
        # Pet information
        info_x = 130
        y_offset = 95
        
        draw.text((info_x, y_offset), f"Name: {pet_name}", fill='black', font=text_font)
        draw.text((info_x, y_offset + 30), f"Species: {pet_species}", fill='black', font=text_font)
        draw.text((info_x, y_offset + 60), f"Birthday: {pet_birthday}", fill='black', font=text_font)
        draw.text((info_x, y_offset + 90), f"Hobbies: {pet_hobbies}", fill='black', font=text_font)

        # Draw border
        draw.rectangle([(0, 0), (card_width-1, card_height-1)], outline='black', width=2)
        
        # Convert to bytes for display
        img_buffer = io.BytesIO()
        card.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Display the card
        st.success("Pet information generated")
        
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(img_buffer, caption="Generated Pet Information", use_container_width=False)
        
        # Download button
        st.download_button(
            label="Download Pet Information",
            data=img_buffer,
            file_name=f"{pet_name}_pet_information.png",
            mime="image/png",
            use_container_width=True
        )