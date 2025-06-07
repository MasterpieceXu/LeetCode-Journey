class Solution:
    def convertTemperature(self, celsius: float) -> List[float]:
        kelvin=celsius+273.15
        fahrenheit=1.80*celsius+32.00
        ans=[kelvin,fahrenheit]
        return ans