class Sol:
    
    def solve(self):
        self.ans = -float('inf')    
        v =[50,30,45,25]
        w =[5,3,4,2]
        cap = 7
        ans = -float('inf')
        dp = {}
        def dfs(ind,wei):
            if wei>cap:
                return -float('inf')
            if ind == len(v):
                return 0
            if (ind,wei) in dp:
                return dp[(ind,wei)]
            no_take = dfs(ind+1,wei)
            take = dfs(ind+1,wei+w[ind]) + v[ind]
            dp[(ind,wei)] = max(no_take,take)
            return max(no_take,take)
        return dfs(0,0)

s = Sol()
print(s.solve())