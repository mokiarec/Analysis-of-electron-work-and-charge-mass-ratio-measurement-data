import numpy as np
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei' 是黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 原始数据
sqrt_Ua = np.array([5, 6, 7, 8, 9, 10, 11, 12])
Ia_T1 = np.array([6, 6, 6, 6, 6, 6, 6, 7])
Ia_T2 = np.array([24, 24, 25, 25, 26, 26, 27, 27])
Ia_T3 = np.array([83, 84, 86, 88, 90, 90, 91, 94])
Ia_T4 = np.array([249, 252, 257, 265, 269, 273, 274, 278])
Ia_T5 = np.array([675, 680, 696, 700, 712, 722, 733, 746])

T = np.array([1800, 1880, 1960, 2040, 2120]) / 1000

# 对数处理
log_Ia_T1 = np.log10(Ia_T1) - 6
log_Ia_T2 = np.log10(Ia_T2) - 6
log_Ia_T3 = np.log10(Ia_T3) - 6
log_Ia_T4 = np.log10(Ia_T4) - 6
log_Ia_T5 = np.log10(Ia_T5) - 6

# 计算数据
log_I = []

def DrowLine1(sqrt_Ua, log_Ia, title):
    # 使用numpy的polyfit进行线性回归，deg=1表示拟合一阶多项式（即直线）
    coefficients = np.polyfit(sqrt_Ua, log_Ia, deg=1)
    slope, intercept = coefficients
    polynomial = np.poly1d(coefficients)

    # 保存拟合出的logI
    log_I.append(intercept)

    # 描处测量点
    plt.scatter(sqrt_Ua, log_Ia, marker='x')
    # 虚线部分（超出数据点范围）
    plt.plot([0, 13], [polynomial(0), polynomial(13)],
             color='black', linestyle='--', linewidth=1)
    # 标出截距
    plt.scatter(0, intercept)
    plt.text(0.2, intercept + 0.1, "logI=" + str(round(intercept, 4)))
    # 曲线的温度
    plt.text(10, log_Ia[6] + 0.15, title, fontsize = 10)

def DrowLine2():
    logI = np.array(log_I)
    y = logI - 2 * np.log10(T)
    print(y)

    # 使用numpy的polyfit进行线性回归，deg=1表示拟合一阶多项式（即直线）
    coefficients = np.polyfit(10 / T, y, deg=1)
    slope, intercept = coefficients
    polynomial = np.poly1d(coefficients)

    # 描绘散点
    plt.scatter(10 / T, y, marker='x', linewidths=3)
    plt.plot([4.5, 5.9], [polynomial(4.5), polynomial(5.9)],
             color='black', linestyle='-', linewidth=1)
    # 标记散点
    for i in range(5):
        plt.text(10 / T[i], y[i] + 0.1, f'({round(10 / T[i], 4)}, {round(y[i], 4)})')

    return slope, intercept

if __name__ == '__main__':

    # 1、绘制sqrt(Ua)~logIa曲线
    plt.figure(num=1)
    fig1, ax1 = plt.subplots(figsize=(6, 8))

    # 署名
    plt.text(2,-2.9, "  57123514 莫可亿\n 2024年12月19日 实验", fontsize=16)

    # 绘制主要曲线
    DrowLine1(sqrt_Ua, log_Ia_T1, "T1 = 1800K")
    DrowLine1(sqrt_Ua, log_Ia_T2, "T2 = 1880K")
    DrowLine1(sqrt_Ua, log_Ia_T3, "T3 = 1960K")
    DrowLine1(sqrt_Ua, log_Ia_T4, "T4 = 2040K")
    DrowLine1(sqrt_Ua, log_Ia_T5, "T5 = 2120K")

    # 在轴上标注公式，使用LaTeX语法
    ax1.set_xlabel(r'$\sqrt{U_a}$', fontsize=15)
    ax1.set_ylabel(r'$\log{I_a}$', fontsize=15)
    ax1.set_title(r'$\log{I_a} - \sqrt{U_a}$ 曲线图')

    plt.xlim((0, 13))
    plt.xticks(np.arange(13))
    plt.ylim((-5.5, -2.5))
    plt.yticks(np.arange(-5.5, -2.5, 0.2))

    plt.savefig('Lab1_1.png', dpi=600)  # 保存图像时设置更高的DPI

    # 2、绘制log(I/T^2)~1/T^2曲线
    plt.figure(num=2)
    fig2, ax2 = plt.subplots(figsize=(6, 6))

    # 署名
    plt.text(5.2,-3.5, "  57123514 莫可亿\n 2024年12月19日 实验", fontsize=12)

    slope, intercept = DrowLine2()

    # 在轴上标注公式，使用LaTeX语法
    ax2.set_xlabel(r'$\frac{1}{T}$', fontsize=20)
    ax2.set_ylabel(r'$log{\frac{I}{T^2}}$', fontsize = 15)
    ax2.set_title(r'$log{\frac{I}{T^2}} - \frac{1}{T}$ 曲线图')
    ax2.text(4.8, -6, f"y = {round(slope, 4)} x + {round(intercept, 4)}")

    plt.savefig('Lab1_2.png', dpi=600)  # 保存图像时设置更高的DPI

    # 展示图像
    plt.show()

    # 处理数据结果
    u = slope * 2.3 * 1.38 / 1.602
    print(f"斜率：{slope}")
    print(f"溢出功：{u}e")
    print(f"误差：{abs(u + 4.45) / 4.45}")