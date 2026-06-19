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
    Parameters
    ----------
    recipes : List[str]
        A list of distinct recipe names. Each recipe may depend on zero or more ingredients.
    ingredients : List[List[str]]
        A list of ingredient lists corresponding to `recipes`. ingredients[i] is the list of
        ingredient names required to make recipes[i]. Ingredients are strings and may refer to
        either basic supplies or other recipes.
    supplies : List[str]
        A list of initially available supply names. Supplies are basic ingredients which can be
        used without preparation. The implementation treats this list as a dynamic collection:
        when a new recipe is determined to be makeable it is appended to `supplies` so it can
        be used to enable other recipes.
    Returns
    -------
    List[str]
        A list of recipe names that can be made using the given supplies and by preparing
        other makeable recipes as necessary. The returned list contains each makeable recipe
        exactly once; order reflects the discovery order produced by the BFS/topological traversal.
    Notes
    -----
    - The method builds a mapping from recipe -> its ingredient list and computes an
      indegree (number of recipe-ingredients that are not initially available) for each recipe.
      Recipes with zero indegree are enqueued and processed; when processed and confirmed
      makeable, they are appended to `supplies` and used to decrement the indegree of recipes
      that depend on them.
    - If an ingredient is neither a basic supply nor a recipe, it prevents the recipe from
      being made.
    - Cycles in recipe dependencies will prevent the involved recipes from becoming makeable
      because their indegrees never reach zero.
    Complexity
    ----------
    Let R = len(recipes) and M = total number of ingredient entries across all recipes.
    A typical efficient implementation using hashed lookups (sets/dictionaries) runs in
    O(R + M) time and uses O(R + M) additional space for mappings and indegree counters.
    """
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        d = defaultdict(list)
        cnt = defaultdict(int)
        n = len(recipes)
        for i in range(n):
            d[recipes[i]] = ingredients[i]
        
        for i in range(n):
            d[recipes[i]] = ingredients[i]
            cnt[recipes[i]] = 0   # \U0001f448 Initialize indegree to 0 for all recipes

        # Count indegrees
        for k, v in d.items():
            for ing in v:
                if ing in d and ing not in supplies:  # if ingredient is also a recipe
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
                
        