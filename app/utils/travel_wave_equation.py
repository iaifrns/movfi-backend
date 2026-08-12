import math

def x_point(i, num_point):
    return i/(num_point-1)

def amplitude(max_ampl, x):
    return max_ampl*(x*x)

def wave_number(wave_length):
    return (2*math.pi) / wave_length

def time(j, fsp):
    return j/fsp

def y_point(k,w,x,a,t):
    return a * math.sin((k*x)+(w*t))

def travel_wave_equation(num_points, max_ampl, wave_length, tail_beat_freq, duration, fsp):
    k = wave_number(wave_length=wave_length)
    w = (2*math.pi) * tail_beat_freq
    frames_num = duration * fsp

    data = []

    print(num_points, max_ampl, wave_length, tail_beat_freq, duration, fsp)
    print('*'*80)

    for i in range(int(num_points)):
        x = x_point(i=i, num_point=num_points)
        a = amplitude(max_ampl=max_ampl, x=x)

        points = {}

        for j in range(int(frames_num)):
            t=time(j, fsp=fsp)

            y = y_point(k=k, a=a, t=t, w=w, x=x)
            key = (j+1)*10

            points[f"{key}x"] = x
            points[f"{key}y"] = y

        data.append(points)

    return data