# DSP_IIR

**DSP** (Digital Signal Process) assignment 3,  coursework.

**GitHub**: [brlink/DSP_IIR: DSP (Digital Signal Process) assignment 3, coursework. (github.com)](https://github.com/brlink/DSP_IIR)

**YouTube Clips**: [[DSP IIR\] Detect Laptop Close-times Using Magnetic Sensor - YouTube](https://youtu.be/IOk0mjxgGTI)

## Lab Main Work

本次实验主要用 IIR 滤波器处理一个实际的 spectrum 输入场景下的噪声，显著地展现出波形变化。

可以用 **Arduino** 或者 **Web Camera** 来捕捉 spectrum。

我们本次实验设想的实际场景：

> 测量具备磁铁感应功能的数码产品（如电脑，平板电脑，etc）开关次数

### 设想

利用磁感应器输入磁力的 impulse response，以 IIR 滤波器滤波后，判断波形是否根据磁力变化而变换。如果显著变换，则可作为标记开关的方法。

### Setup

**Arduino**

![Arduino](https://raw.githubusercontent.com/brlink/FigureBed/master/img/md/Arduino.jpg)

**Magnetic Sensor**

![Sensor](https://raw.githubusercontent.com/brlink/FigureBed/master/img/md/Sensor.jpg)

## Concept Description

**IIR** means `Infinite Impulse Response`,  无限冲击响应

顾名思义，输入的冲击波是无限的，相比于 **FIR** means `Finite Impulse Response`，冲击波响应的时间性质不同，因此我们要改变处理冲击波响应的方式。因为 IIR filters 非常接近于 analogue，所以做 Laplace 变换来得到 coefficient。以此达到过滤无限冲击波的目的。

## Filter Design

**2nd Order IIR Filter**

```python
# a 2nd order IIR filter which takes the coefficients in the constructor
class IIR2Filter:
    #2nd order IIR filter
    def __init__(self,_b0,_b1,_b2,_a0,_a1,_a2,):
        self.a0 = _a0
        self.a1 = _a1
        self.a2 = _a2
        self.b0 = _b0
        self.b1 = _b1
        self.b2 = _b2
        self.buffer1 = 0
        self.buffer2 = 0
    
    def filter(self,x):  #x as input  acc_input=accumulator input
        #IIR PART
        acc_input = float()
        acc_output = float()
        acc_input = x*self.a0 - self.buffer1*self.a1 - self.buffer2*self.a2

        #FIR part 
        #acc_output = acc_input * self.b0 + self.buffer1*self.b1
        acc_output = acc_input * self.b0 + self.buffer1*self.b1+ self.buffer2*self.b2
        self.buffer2 = self.buffer1
        self.buffer1 = acc_input
        
        return acc_output
```

**IIR Filter**

```python
class IIRFilter:
    def __init__(self, sos: np.ndarray):
        self.sos_filters = []
        # get 2nd order filters
        for index in range(sos.shape[0]):
            ba = sos[index]
            filter_tmp = IIR2Filter(ba[0], ba[1], ba[2], ba[3], ba[4], ba[5])
            self.sos_filters.append(filter_tmp)

    def filter(self, x):  # x as input  acc_input=accumulator input
        output = x
        for filter in self.sos_filters:
            output = filter.filter(output)
        return output

```

## Reference

From Professor **Bernd Porr**

[berndporr/py-iir-filter: Realtime IIR filter (sample in, sample out) (github.com)](https://github.com/berndporr/py-iir-filter)

Specially Thanks to **Wayan Van**:

[WayenVan/DsipAssignment3 (github.com)](https://github.com/WayenVan/DsipAssignment3)