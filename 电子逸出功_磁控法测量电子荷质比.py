import numpy as np
import matplotlib.pyplot as plt
from sympy.printing.pretty.pretty_symbology import line_width

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei' 是黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 原始数据
Ua = {
    '5.0' : {
        'Is' : np.array([1, 163, 184, 186, 190, 191, 192, 194, 195, 196, 197, 199, 200, 201, 202, 203, 204, 205, 207, 209, 211, 214, 216, 219, 225, 230, 238, 260, 296]),
        'Ia' : np.array([150, 150, 143, 140, 130, 124, 122, 112, 106, 102, 99, 92, 86, 79, 78, 73, 68, 66, 58, 52, 46, 38, 33, 29,20, 16, 10, 4, 0])
    },
    '4.5' : {
        'Is' : np.array([1, 155, 170, 176, 178, 180, 181, 182, 184, 185, 186, 187, 188, 189, 191, 193, 194, 197, 200, 204, 209, 215, 216, 217, 220, 224, 235, 240, 253, 267]),
        'Ia' : np.array([148, 148, 145, 139, 134, 129, 123, 119, 113, 106, 103, 100, 95, 89, 82, 74, 69, 59, 49, 38, 28, 18, 17, 15, 13, 9, 5, 4, 2, 1])
    },
    '4.0' : {
        'Is' : np.array([1, 143, 156, 162, 166, 167, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 181, 182, 184, 185, 186, 188, 190, 193, 195, 198, 201, 207, 217, 247]),
        'Ia' : np.array([146, 146, 144, 141, 136, 132, 128, 122, 116, 113, 108, 104, 101, 98, 93, 87, 82, 76, 71, 65, 60, 54, 48, 40, 35, 30, 23, 14, 6, 0])
    },
    '3.5' : {
        'Is' : np.array([1, 138, 143, 149, 152, 154, 157, 159, 160, 161, 163, 165, 166, 167, 169, 170, 172, 173, 174, 175, 176, 177, 179, 182, 186, 190, 194, 200, 206, 229]),
        'Ia' : np.array([142, 142, 141, 139, 136, 133, 128, 121, 118, 115, 108, 102, 96, 92, 86, 82, 76, 72, 68, 63, 60, 59, 51, 41, 32, 24, 18, 10, 6, 1])
    },
    '3.0' : {
        'Is' : np.array([1, 126, 131, 135, 137, 140, 142, 143, 145, 147, 149, 150, 151, 152, 153, 155, 157, 158, 160, 162, 164, 167, 170, 174, 177, 180, 183, 189, 200, 216]),
        'Ia' : np.array([139, 139, 138, 136, 133, 130, 127, 124, 119, 113, 107, 104, 100, 96, 92, 86, 80, 76, 70, 65, 59, 47, 41, 31, 25, 20, 15, 9, 3, 1])
    }
}
U = [5.0, 4.5, 4.0, 3.5, 3.0]
# 生成数据
Ic = []

def Get_Ic(x, y):
    # 计算导数（差分近似）
    dy = np.diff(y) / np.diff(x)

    # 找到导数绝对值最大的点
    max_slope_index = np.argmax(np.abs(dy))
    max_slope_x = (x[:-1] + x[1:])[max_slope_index] / 2  # x坐标是两个点的中点
    max_slope_y = (y[:-1] + y[1:])[max_slope_index] / 2  # y坐标是两个点的中点
    max_slope = dy[max_slope_index]
    intercept = max_slope_y - max_slope * max_slope_x

    # 标记斜率最大的点
    plt.plot(max_slope_x, max_slope_y, 'ro')  # 红色圆点标记

    # 作切线
    coefficients = max_slope, intercept
    polynomial = np.poly1d(coefficients)
    plt.plot([100, max_slope_x+8], [polynomial(100), polynomial(max_slope_x+8)],
             linewidth=0.8, linestyle='--', color='black')
    # 作上界线
    plt.plot([0, 300], np.full_like([0, 300], y[1]),
             linewidth=0.8, linestyle='--', color='black')

    # 计算Ic
    I = (y[1] - intercept)/max_slope
    plt.scatter(I, y[1], linewidths=0.5, s=15, color='black')

    # 作垂线
    plt.axvline(I, linestyle='--', linewidth=0.5)

    return I, max_slope_x, max_slope_y, max_slope

def DrawLine(scatter):
    fig, ax = plt.subplots(figsize=(12, 6))
    # 署名
    plt.text(25,60, "  57123514 莫可亿\n 2024年12月19日 实验", fontsize=20)

    # 绘图
    for key in Ua.keys():
        if scatter:
            plt.scatter(Ua[key]['Is'], Ua[key]['Ia'], linewidths=1, marker='x', color='black')
        plt.plot(Ua[key]['Is'], Ua[key]['Ia'])
    # 加入曲线标签
    plt.text(150, 50, r'$U_{a1}$', fontsize=10)
    plt.text(165, 60, r'$U_{a2}$', fontsize=10)
    plt.text(175, 70, r'$U_{a3}$', fontsize=10)
    plt.text(192, 76, r'$U_{a4}$', fontsize=10)
    plt.text(200, 120, r'$U_{a5}$', fontsize=10)

    plt.xlim((0, 300))
    plt.ylim((0, 160))
    plt.xlabel(r'$I_s$', fontsize=20)
    plt.ylabel(r'$I_a$', fontsize=20)
    plt.title(r'$I_a - I_s$ 曲线图', fontsize=20)

def AnalysisLine():
    DrawLine(False)

    i = 0
    for key in Ua.keys():
        I, max_slope_x, max_slope_y, max_slope = Get_Ic(Ua[key]['Is'], Ua[key]['Ia'])
        # 描点
        plt.scatter(I, 0)
        plt.text(I, 2 + i, f'{round(I, 2)}', fontsize=10)
        i = i + 5
        Ic.append(I)

if __name__ == '__main__':
    DrawLine(True)
    plt.savefig('Lab2_1.png', dpi=600)  # 保存图像时设置更高的DPI
    AnalysisLine()
    plt.savefig('Lab2_2.png', dpi=600)  # 保存图像时设置更高的DPI

    # 计算Ua-Ic^2
    coefficients = np.polyfit(np.array(Ic)**2, np.array(U), deg=1)
    slope, intercept = coefficients
    polynomial = np.poly1d(coefficients)

    # 计算电子荷质比
    e_m = 1.758802      # 标准荷质比
    N = 910             # 线圈匝数
    L = 0.040           # 励磁线圈的长度
    D = 0.049           # 励磁线圈的平均直径
    b = 8.4 / 2 * 10**-3             # 阳极半径
    miu = 4 * 3.1415926 * 10**-7 # 真空磁导率
    K = miu**2 * N**2 /(L**2 + D**2)
    em = 8 * slope / b**2 / K * 10**-5

    # 打印结果
    print(U)
    print(Ic)
    print(K)
    print(f"Ua/Ic^2比值：{slope * 10**-5}")
    print(f"计算得出电子荷质比：{em}")
    print(f"相对误差：{np.abs(em - e_m) / e_m * 100}%")

    plt.show()