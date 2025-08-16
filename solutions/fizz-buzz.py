class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        R=[]
        for i in range(1,n+1):
            if i%3==0 and i%5==0:
                R.append('FizzBuzz')
            elif i%3==0:
                R.append('Fizz')
            elif i%5==0:
                R.append('Buzz')
            else:
                R.append(f'{i}')
        return R