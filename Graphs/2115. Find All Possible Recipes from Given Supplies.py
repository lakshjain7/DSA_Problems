from collections import defaultdict
from collections import deque
from typing import List
class Solution:
    """
    Determine which recipes can be prepared from given supplies and inter-dependent recipes.
    This method attempts to find all recipes that can be created using the initial supplies
    and other recipes as ingredients. A recipe becomes available to use as a supply once
    all of its ingredients are either in the initial supplies or are recipes that have been
    determined to be makeable. The algorithm is based on indegree counting and a BFS/topological
    sort over the recipe dependency graph.
    """
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        d = defaultdict(list)
        cnt = defaultdict(int)
        n = len(recipes)
        for i in range(n):
            d[recipes[i]] = ingredients[i]
        
        for i in range(n):
            d[recipes[i]] = ingredients[i]
            cnt[recipes[i]] = 0

        # Count indegrees
        for k, v in d.items():
            for ing in v:
                if ing in d and ing not in supplies:
                    cnt[k] += 1
        
        q = deque([])
        for k,v in cnt.items():
            if(v==0):
                q.append(k)
        ans=[]
        while q:
            elem = q.popleft()
            ans_cnt = len(d[elem])
            cnt1 = 0
            for v in d[elem]:
                if(v in supplies):
                    cnt1+=1
            if(cnt1==ans_cnt):
                ans.append(elem)
                supplies.append(elem)
                for k1,v1 in cnt.items():
                    if(v1!=0):
                        if(elem in d[k1]):
                            cnt[k1]-=1
                            if(cnt[k1]==0):
                                q.append(k1)

        return ans
