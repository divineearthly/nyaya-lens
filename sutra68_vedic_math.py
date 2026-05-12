class VedicConvolution:
    @staticmethod
    def urdhva_multiply(a, b):
        if a < 10 and b < 10:
            return a * b
        n = max(len(str(a)), len(str(b))) // 2
        a1, a0 = divmod(a, 10**n)
        b1, b0 = divmod(b, 10**n)
        z0 = VedicConvolution.urdhva_multiply(a0, b0)
        z2 = VedicConvolution.urdhva_multiply(a1, b1)
        z1 = VedicConvolution.urdhva_multiply(a0 + a1, b0 + b1) - z0 - z2
        return z2 * 10**(2*n) + z1 * 10**n + z0
    
    @staticmethod
    def nikhilam_multiply(a, b, base=100):
        da = a - base
        db = b - base
        return (a + db) * base + da * db
    
    @staticmethod
    def convolution_1d(signal, kernel):
        result = []
        for i in range(len(signal) - len(kernel) + 1):
            s = 0
            for j in range(len(kernel)):
                s += VedicConvolution.urdhva_multiply(signal[i + j], kernel[j])
            result.append(s)
        return result
    
    @staticmethod
    def benchmark():
        import time
        a, b = 123456789, 987654321
        start = time.time()
        for _ in range(10000):
            _ = a * b
        standard = time.time() - start
        start = time.time()
        for _ in range(10000):
            _ = VedicConvolution.urdhva_multiply(a, b)
        vedic = time.time() - start
        return {"standard_ms": round(standard*1000,2), "vedic_ms": round(vedic*1000,2)}
