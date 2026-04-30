import streamlit as st
from PIL import Image
import io
import zipfile

# Sayfa Ayarları
st.set_page_config(page_title="Mailing Yapma Uygulaması", layout="wide")

def generate_html(link_url, page_title):
    """ZIP içine eklenecek, dinamik başlığa sahip HTML kodunu üretir."""
    html_template = f"""<html>
<head>
<title>{page_title}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0" />
<style>
    table {{ border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-spacing: 0; }}
    img {{ display: block; border: 0; width: 100%; max-width: 1080px; }}
</style>
</head>
<body bgcolor="#FFFFFF" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 1080px;" align="center">
        <tr>
            <td align="center">
                <img src="./images/01_ust.jpg" alt="Üst Görsel">
            </td>
        </tr>
        <tr>
            <td align="center">
                <a href="{link_url}" target="_blank">
                    <img src="./images/02_buton.jpg" alt="Tıklanabilir Alan">
                </a>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="./images/03_alt.jpg" alt="Alt Görsel">
            </td>
        </tr>
    </table>
</body>
</html>"""
    return html_template

st.title("🚀 Mailing Yapma Uygulaması")

# ADIM 1: GENEL BİLGİLER
st.header("Adım 1: Genel Bilgiler")
page_title = st.text_input("Sayfa Başlığı (ZIP dosyası adını ve sekme başlığını belirler)", "Mailing_Sablonu")

# ADIM 2: GÖRSEL YÜKLEME
st.header("Adım 2: Görsel Yükleme")
uploaded_file = st.file_uploader("Mailing Görselinizi Yükleyin (JPG/PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    width, height = img.size
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(img, caption=f"Orijinal Görsel ({width}x{height} piksel)", use_container_width=True)
        
    with col2:
        # ADIM 3: GÖRSELİ BÖLME
        st.header("Adım 3: Görseli Bölme (Dilimleme)")
        st.write("Aşağıdaki kaydırıcıyı kullanarak butonun olduğu alanı belirleyin:")
        
        start_y, end_y = st.slider(
            "Buton Başlangıç ve Bitiş Noktası (Piksel):",
            min_value=0,
            max_value=height,
            value=(int(height * 0.6), int(height * 0.75)),
            step=5
        )
        
        top_img = img.crop((0, 0, width, start_y))
        btn_img = img.crop((0, start_y, width, end_y))
        bot_img = img.crop((0, end_y, width, height))
        
        st.write("🎯 **Dilimlenmiş Parçaların Önizlemesi:**")
        st.image(btn_img, caption="Tıklanabilir Buton Alanı (Orta Kısım)", use_container_width=True)
        
        # ADIM 4: LİNK EKLEME
        st.header("Adım 4: Link Ekleme")
        target_link = st.text_input("Butona tıklandığında gidilecek URL:", "https://www.orneklink.com")
        
        # ADIM 5: TEST & ÖNİZLEME
        st.header("Adım 5: Test & Önizleme")
        st.success(f"'{page_title}' başlığı ile HTML yapısı oluşturuldu.")
        
        st.image(top_img, use_container_width=True)
        st.markdown(f"👆 **Üst Görsel** | 👇 **Buton ({target_link})**")
        st.image(btn_img, use_container_width=True)
        st.markdown("👆 **Buton** | 👇 **Alt Görsel**")
        st.image(bot_img, use_container_width=True)

        # ADIM 6: ZIP OLARAK VERME
        st.header("Adım 6: ZIP Olarak İndir")
        
        top_bytes = io.BytesIO()
        btn_bytes = io.BytesIO()
        bot_bytes = io.BytesIO()
        
        top_img.convert('RGB').save(top_bytes, format='JPEG', quality=95)
        btn_img.convert('RGB').save(btn_bytes, format='JPEG', quality=95)
        bot_img.convert('RGB').save(bot_bytes, format='JPEG', quality=95)
        
        html_code = generate_html(target_link, page_title)
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("images/01_ust.jpg", top_bytes.getvalue())
            zip_file.writestr("images/02_buton.jpg", btn_bytes.getvalue())
            zip_file.writestr("images/03_alt.jpg", bot_bytes.getvalue())
            # HTML dosyasının adını her zaman index.html olarak sabitliyoruz
            zip_file.writestr("index.html", html_code)
            
        st.download_button(
            label="📦 Mailing Paketini İndir (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"{page_title}.zip", # ZIP dosyasına sayfa başlığı adını veriyoruz
            mime="application/zip",
            type="primary"
        )