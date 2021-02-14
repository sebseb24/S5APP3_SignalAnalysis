import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

if __name__ == '__main__':
    # a) x_1[n]
    x1 = []
    x_1 = []
    x_1_1 = []
    x_1m = []
    N1 = 22
    N_1 = 20
    N_1_1 = 256

    # boucle pour le signal sin de x1[n] pour n = 22
    t1 = np.arange(0.0, 22.0, 1)
    for n in t1:
        x1.append(np.sin(0.1 * np.pi * n + np.pi / 4))

    # boucle pour le signal sin de x1[n] pour n = 20
    t1_1 = np.arange(0.0, 20.0, 1)
    for n in t1_1:
        x_1.append(np.sin(0.1 * np.pi * n + np.pi / 4))

    # boucle pour le omega (axe x) pour b)
    for m in t1_1:
        x_1m.append(2*np.pi*m/N_1)

# a) et b) tfd module et angle (rad) avec N=22
    x1fft = np.fft.fft(x1, N1)
    x1fft_abs = np.abs(x1fft)
    x1fft_ang = np.angle(x1fft)
    x1fft_rad = np.radians(x1fft_ang)

# a) et b) tfd module et angle (rad) avec N=20
    x1fft_1 = np.fft.fft(x_1, N_1)
    x1fft_1_abs = np.abs(x1fft_1)
    x1fft_1_ang = np.angle(x1fft_1)
    x1fft_1_rad = np.radians(x1fft_1_ang)

#c) fenetre de hanning sur la tfd avec N=22
    h_n = np.hanning(N1)
    x1_hn = x1*h_n
    x1_hn_fft = np.fft.fft(x1_hn, N1)
    x1_hn_fft_abs = np.abs(x1_hn_fft)

# d) fenetre de Hanning sur la tfd avec n=256
    t_1_1 = np.arange(0.0, 256.0, 1)
    for n in t_1_1:
        x_1_1.append(np.sin(0.1 * np.pi * n + np.pi / 4))

    x1fft_1_1 = np.fft.fft(x_1_1, N_1_1)
    x1fft_1_1_abs = np.abs(x1fft_1_1)

    h_n_1 = np.hanning(N_1_1)
    x_1_hn = x_1_1 * h_n_1
    x_1_hn_fft = np.fft.fft(x_1_hn, N_1_1)
    x_1_hn_fft_abs = np.abs(x_1_hn_fft)

#affichage des différentes figures
    plt.figure()
    plt.stem(x1)
    plt.title('a) x_1[n] (N=22)')

    plt.figure()
    plt.stem(x1fft_abs)
    plt.title('a) TFD(x_1[n]) (N=22) amplitude')

    plt.figure()
    plt.stem(x1fft_ang)
    plt.title('a) TFD(x_1[n]) (N=22) angle (rad)')

    plt.figure()
    plt.stem(x_1)
    plt.title('a) x_1[n] (N=20)')

    plt.figure()
    plt.stem(x1fft_1_abs)
    plt.title('a) TFD(x_1[n]) (N=20) amplitude')
    plt.figure()
    plt.stem(x1fft_1_ang)
    plt.title('a) TFD(x_1[n]) (N=20) angle (rad)')

    plt.figure()
    plt.stem(x_1m, x1fft_1_abs)
    plt.title('b) TFD(x_1[n]) freq. norm. amplitude')
    plt.figure()
    plt.stem(x_1m, x1fft_1_ang)
    plt.title('b) TFD(x_1[n]) freq. norm. angle (rad)')

    plt.figure()
    plt.plot(x1fft_abs)
    plt.plot(x1_hn_fft_abs)
    plt.title('c) TFD(x_1[n]) Fenetre Hanning')

    plt.figure()
    plt.plot(x1fft_1_1_abs)
    plt.plot(x_1_hn_fft_abs)
    plt.title('d) TFD(x_1[n]) Fenetre Hanning (N=256)')

    plt.show()

    # a) x_2[n]
    x2 = []
    N2 = 22
    # boucle pour la fonction x2[n] = [1,-1,1,-1...]
    t2 = np.arange(0.0, 22.0, 1)
    for n in t2:
        if n % 2 == 0:
            x2.append(1)
        else:
            x2.append(-1)

    # a) et b) tfd module et angle (rad) avec N=22
    x2fft = np.fft.fft(x2, N2)
    x2fft_abs = np.abs(x2fft)
    x2fft_ang = np.angle(x2fft)
    #x2fft_rad = np.radians(x2fft_ang);

    # affichage des différentes figure
    plt.figure()
    plt.stem(x2)
    plt.title('a) x_2[n]')

    plt.figure()
    plt.stem(x2fft_abs)
    plt.title('a) TFD(x_2[n]) amplitude')

    plt.figure()
    plt.stem(x2fft_ang)
    #plt.stem(x2fft_rad)
    plt.title('a) TFD(x_2[n]) angle (rad)')

    plt.show()

    # a) x_3[n]
    x3 = []
    N3 = 19
    # boucle pour la fonction x2[n] = delta[n-10]
    t3 = np.arange(0.0, 19.0, 1)
    for n in t3:

        if  n-10==0:
            x3.append(1)
        else:
            x3.append(0)

    # a) et b) tfd module et angle (rad) avec N=22
    x3fft = np.fft.fft(x3, N3)
    x3fft_abs = np.abs(x3fft)
    x3fft_ang = np.angle(x3fft)
    #x3fft_rad = np.radians(x3fft_ang);

    # affichage des différentes figure
    plt.figure()
    plt.stem(x3)
    plt.title('a) x_3[n]')

    plt.figure()
    plt.stem(x3fft_abs)
    plt.title('a) TFD(x_3[n]) amplitude')

    plt.figure()
    plt.stem(x3fft_ang)
    #plt.stem(x3fft_rad)
    plt.title('a) TFD(x_3[n]) angle (rad)')

    plt.show()

    exit(1)



