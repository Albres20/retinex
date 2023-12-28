import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_ksize(sigma):

    return int(((sigma - 0.8)/0.15) + 2.0)

def get_gaussian_blur(img, ksize=0, sigma=5):

    if ksize == 0:
        ksize = get_ksize(sigma)

    sep_k = cv2.getGaussianKernel(ksize, sigma)

    return cv2.filter2D(img, -1, np.outer(sep_k, sep_k))

def ssr(img, sigma):

    return np.log10(img) - np.log10(get_gaussian_blur(img, ksize=0, sigma=sigma) + 1.0)

def msr(img, sigma_scales=[15, 80, 250]):

    msr = np.zeros(img.shape)

    for sigma in sigma_scales:
        msr += ssr(img, sigma)

    msr = msr / len(sigma_scales)

    msr = cv2.normalize(msr, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC3)

    return msr

def color_balance(img, low_per, high_per):

    tot_pix = img.shape[1] * img.shape[0]

    low_count = tot_pix * low_per / 100
    high_count = tot_pix * (100 - high_per) / 100

    ch_list = []
    if len(img.shape) == 2:
        ch_list = [img]
    else:
        ch_list = cv2.split(img)

    cs_img = []

    for i in range(len(ch_list)):
        ch = ch_list[i]

        cum_hist_sum = np.cumsum(cv2.calcHist([ch], [0], None, [256], (0, 256)))

        li, hi = np.searchsorted(cum_hist_sum, (low_count, high_count))
        if (li == hi):
            cs_img.append(ch)
            continue

        lut = np.array([0 if i < li
                        else (255 if i > hi else round((i - li) / (hi - li) * 255))
                        for i in np.arange(0, 256)], dtype = 'uint8')

        cs_ch = cv2.LUT(ch, lut)
        cs_img.append(cs_ch)

    if len(cs_img) == 1:
        return np.squeeze(cs_img)
    elif len(cs_img) > 1:
        return cv2.merge(cs_img)
    return None

def msrcp(img, sigma_scales=[15, 80, 250], low_per=1, high_per=1):
     # Retinex multiescala con preservación del color
     # Int(x,y) = suma(Ic(x,y))/3, c={0...k-1}, k=nº de canales
     # MSR_Int(x,y) = MSR(Int(x,y)), y aplicar balance de color
     # B(x,y) = MAX_VALUE/max(Ic(x,y))
     # A(x,y) = máx(B(x,y), MSR_Int(x,y)/Int(x,y))
     #MSRCP = A*I

    # Imagen de intensidad (Int)
    int_img = (np.sum(img, axis=2) / img.shape[2]) + 1.0

    # Imagen de intensidad de retinex de múltiples escalas (MSR)
    msr_int = msr(int_img, sigma_scales)

    # balance de color de MSR
    msr_cb = color_balance(msr_int, low_per, high_per)

    # B = MÁX/máx(Ic)
    B = 256.0 / (np.max(img, axis=2) + 1.0)

    # BB = stack(B, MSR/Int)
    BB = np.array([B, msr_cb/int_img])

    # A = min(BB)
    A = np.min(BB, axis=0)

    # MSRCP = A*I
    msrcp = np.clip(np.expand_dims(A, 2) * img, 0.0, 255.0)

    return msrcp.astype(np.uint8)

def starConversion(numpyArray):
    # Carga la imagen de entrada *******************************************************************
    #input_image = cv2.imread('Prueba.jpg')
    input_image=np.frombuffer(numpyArray, dtype=np.uint8)

    # Asegúrate de que la imagen se cargó correctamente
    if input_image is None:
        print('Error al cargar la imagen.')
        return 0
    else:
        # Continúa con el procesamiento de la
        # Procesa la imagen utilizando la función msrcp
        resultado = msrcp(input_image, sigma_scales=[15, 80, 250], low_per=1, high_per=1)

        return resultado
