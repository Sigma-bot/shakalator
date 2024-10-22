import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from skimage import io 
from io import BytesIO
import imageio

st.title("Проверка зрения онлайн")
uploaded_files = st.file_uploader(
    "Загрузи картинку, чтобы узнать своё зрение", accept_multiple_files=True, type=['png', 'jpeg', 'jpg']
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image_bytes = uploaded_file.read()
        
        image = imageio.v3.imread(BytesIO(image_bytes))

        if len(image.shape) == 2:  
            continue
        else:
            image = image[:, :, 1]  
        st.write("## Идеальное зрение")
        st.image(image, caption="Идеальное зрениe")

        U, sing_vals, V = np.linalg.svd(image)
        sigma = np.zeros(shape = image.shape)
        np.fill_diagonal(sigma, sing_vals)
        k_top = st.slider("Двигая ползунок право и влево установите его на значении картинки, отражающей как вы видите этот мир", 1, len(sing_vals), 25)
        Unew=U[:,:k_top]
        sigmanew=sigma[:k_top,:k_top]
        Vnew=V[:k_top,:]
        pic=Unew@sigmanew@Vnew
        pic = np.clip(pic, 0, 255).astype(np.uint8)
        st.write("## Ваше зрение")
        st.image(pic, caption="Идеальное зрениe")
        st.write(f'## Ваше зрение - {100 * k_top / len(sing_vals)}% от идеального')
        if k_top==1:
            st.write("# Поздравляю, вы слеп как крот!")
        elif k_top==len(sing_vals):
            st.write("# Поздравляю, вы можете видеть сквозь стены!")
        warning_text = """
        <style>
            .warning-text {
                font-size: 12px; 
                color: gray; 
            }
        </style>

        <p class="warning-text">
            Сумма за обследование будет автоматически списана с вашего счета в соответствии с условиями, которые вы подтвердили ранее. Это действие произойдет без дополнительного уведомления, и средства будут вычтены в полном объеме, что может существенно сказаться на вашем балансе. Обратите внимание, что в случае недостатка средств на счете могут возникнуть дополнительные штрафные санкции, что повлечет за собой непредвиденные финансовые последствия. Пожалуйста, убедитесь, что на вашем счету достаточно средств, чтобы избежать неприятностей и возможных задержек в предоставлении услуг.
        </p>
        """
        st.markdown(warning_text, unsafe_allow_html=True)
