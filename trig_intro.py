"""trig_intro.py

簡短教學：計算與繪製 sin, cos, tan

執行：`python3 trig_intro.py`，會在終端印出範例數值並產生一個 PNG 圖檔 `trig_plot.png`。
"""
import math
import numpy as np
import matplotlib.pyplot as plt

def sample_values(angle_degrees):
    theta = math.radians(angle_degrees)
    return {
        'degrees': angle_degrees,
        'radians': theta,
        'sin': math.sin(theta),
        'cos': math.cos(theta),
        'tan': None if math.isclose(math.cos(theta), 0.0, abs_tol=1e-12) else math.tan(theta)
    }

def print_samples(angles):
    print(f"{'deg':>4}  {'rad':>7}    {'sin':>9}    {'cos':>9}    {'tan':>9}")
    print('-'*50)
    for a in angles:
        v = sample_values(a)
        tan_str = f"{v['tan']:.6f}" if v['tan'] is not None else 'inf'
        print(f"{v['degrees']:4.0f}  {v['radians']:7.4f}  {v['sin']:9.6f}  {v['cos']:9.6f}  {tan_str:>9}")

def plot_trig(save_path='trig_plot.png'):
    x = np.linspace(-2*math.pi, 2*math.pi, 1000)
    s = np.sin(x)
    c = np.cos(x)
    # for tan, limit plotting to avoid huge spikes: clip values
    t = np.tan(x)
    t = np.where(np.abs(t) > 10, np.nan, t)

    plt.figure(figsize=(10, 5))
    plt.plot(x, s, label='sin(x)', color='tab:blue')
    plt.plot(x, c, label='cos(x)', color='tab:orange')
    plt.plot(x, t, label='tan(x) (clipped)', color='tab:green')
    plt.axhline(0, color='k', linewidth=0.5)
    plt.axvline(0, color='k', linewidth=0.5)
    plt.legend()
    plt.title('Sine, Cosine and Tangent')
    plt.xlabel('x (radians)')
    plt.ylabel('value')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved to: {save_path}")

def main():
    angles = [0, 30, 45, 60, 90, 120, 180, 270]
    print_samples(angles)
    plot_trig()

if __name__ == '__main__':
    main()
