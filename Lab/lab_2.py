import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

if __name__ == '__main__':

    # a) rep impulsionnelle h[n] pour N=16
    N1 = 16
    n = 16
    t = np.arange((-n/2)+1, (n/2)+1, 1)

    hn1 = 1 / N1 * (np.sin(np.pi * t * 5 / N1) / (np.sin(np.pi * t / N1)))

    hn1[7] = 5.0/N1
    # b) Rép. en freq. pour (N=16)

    hn_1, hn_1_1 = signal.freqz(hn1)

    # c) Fenetre Hamming h_w[n] pour (N=16)

    h_m1 = np.hamming(N1)
    hn1_hm = hn1 * h_m1

    # c) Rép. en freq. fenetrée pour (N=16)

    hn_1f, hn_1_1f = signal.freqz(hn1 * h_m1)

    # affichage des différents graphiques
    plt.figure()
    plt.stem(t,hn1)
    plt.title('a) Rép. impulsionnelle h[n] (N=16)')

    fig, ax1 = plt.subplots()

    ax1.set_title('b) Rép. en fréquence (N=16) freqz')
    ax1.plot(hn_1, 20 * np.log10(abs(hn_1_1)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('rad/éch')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(hn_1_1))
    ax2.plot(hn_1, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()

    fig, ax1 = plt.subplots()

    ax1.set_title('c) Rép. en fréquence fenetrée (N=16) freqz')
    ax1.plot(hn_1f, 20 * np.log10(abs(hn_1_1f)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('rad/éch')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(hn_1_1f))
    ax2.plot(hn_1f, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()

    plt.figure()
    plt.stem(t, hn1_hm)
    plt.title('c) Rép. impulsionnelle fenetrée h_w[n] (N=16)')

    # a) rep impulsionnelle h[n] pour N=32
    N2 = 32
    n = 32
    t = np.arange((-n/2)+1, (n/2)+1, 1)
    hn2 = 1 / N2 * (np.sin(np.pi * t * 9 / N2) / (np.sin(np.pi * t / N2)))
    hn2[15] = 9.0 / N2

    #b) Rép. en freq. pour (N=32)

    hn_2, hn_2_1 = signal.freqz(hn2)

    # c) Fenetre Hamming h_w[n] pour (N=32)

    h_m2 = np.hamming(N2)
    hn2_hm = hn2*h_m2

    # c) Rép. en freq. fenetrée pour (N=32)

    hn_2f, hn_2_1f = signal.freqz(hn2 * h_m2)

    # affichage des différents graphiques
    plt.figure()
    plt.stem(t, hn2, 'b')
    plt.title('a) Rép. impulsionnelle h[n] (N=32)')

    fig, ax1 = plt.subplots()

    ax1.set_title('b) Rép. en fréquence (N=32) freqz')
    ax1.plot(hn_2, 20 * np.log10(abs(hn_2_1)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('rad/éch')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(hn_2_1))
    ax2.plot(hn_2, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()

    fig, ax1 = plt.subplots()

    ax1.set_title('c) Rép. en fréquence fenetrée (N=32) freqz')
    ax1.plot(hn_2f, 20 * np.log10(abs(hn_2_1f)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('rad/éch')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(hn_2_1f))
    ax2.plot(hn_2f, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()

    plt.figure()
    plt.stem(t, hn2_hm)
    plt.title('c) Rép. impulsionnelle fenetrée h_w[n] (N=32)')

    # a) rep impulsionnelle h[n] pour N=64
    N3 = 64
    n = 64
    t = np.arange((-n/2)+1, (n/2)+1, 1)

    hn3 = 1 / N3 * (np.sin(np.pi * t * 17 / N3) / (np.sin(np.pi * t / N3)))

    hn3[31] = 17.0 / N3

    #b) Rép. en freq. pour (N=64)

    hn_3, hn_3_1 = signal.freqz(hn3)

    # c) Fenetre Hamming h_w[n] pour (N=64)

    h_m3 = np.hamming(N3)
    hn3_hm = hn3*h_m3

    # c) Rép. en freq. fenetrée pour (N=64)

    hn_3f, hn_3_1f = signal.freqz(hn3*h_m3)

    # affichage des différents graphiques
    plt.figure()
    plt.stem(t, hn3)
    plt.title('a) Rép. impulsionnelle h[n] (N=64)')

    fig, ax1 = plt.subplots()

    ax1.set_title('b) Rép. en fréquence (N=64) freqz')
    ax1.plot(hn_3, 20 * np.log10(abs(hn_3_1)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('rad/éch')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(hn_3_1))
    ax2.plot(hn_3, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()

    fig, ax1 = plt.subplots()

    ax1.set_title('c) Rép. en fréquence fenetrée (N=64) freqz')
    ax1.plot(hn_3f, 20 * np.log10(abs(hn_3_1f)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('rad/éch')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(hn_3_1f))
    ax2.plot(hn_3f, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()

    plt.figure()
    plt.stem(t, hn3_hm)
    plt.title('c) Rép. impulsionnelle fenetrée h_w[n] (N=64)')

    # d) Filtre RIF fenetre et sans fenetre N=64
    A_1 = 1
    A_2 = 0.25
    f_1 = 200
    f_2 = 3000
    N = 128
    fe = 16000
    x_n = []
    t = np.arange(0.0, 128.0+1, 1)
    n = 129
    t1 = np.arange((-n/2)+1, (n/2)+1, 1)
    for n in t:
        x_n.append(A_1*np.sin((2*np.pi*f_1*n)/fe) + A_2*np.sin((2*np.pi*f_2*n)/fe))

    hn3_d = 1 / N * (np.sin(np.pi * t1 * 33 / N) / (np.sin(np.pi * t1 / N)))

    hn3_d[63] = 33.0 / N
    x_n_f = hn3_d * x_n

    # affichage des différents graphiques
    plt.figure()
    plt.stem(x_n)
    plt.title('d) Signal')

    plt.figure()
    plt.stem(x_n_f)
    plt.title('d) Signal filtré avec rep imp non fenetrée')

    plt.show()
    exit(1)