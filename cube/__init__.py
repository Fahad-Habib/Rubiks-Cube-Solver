"""
    Solve a 3x3x3 Rubik's Cube

    @author: Fahad Habib

    "F" (FRONT) Represents White Face of the cube
    "U" (UP) Represents Green Face
    "L" (LEFT) Represents Red Face
    "R" (RIGHT) Represents Orange Face (Opposite of Red Face)
    "D" (DOWN) Represents Blue Face (Opposite of Green Face)
    "B" (BACK) Represents Yellow Face (Opposite of White Face)

    '0' Represents White Color
    '1' Represents Green Color
    '2' Represents Red Color
    '3' Represents Orange Color (Opposite of Red)
    '4' Represents Blue Color (Opposite of Green)
    '5' Represents Yellow Color (Opposite of White)

    "F[0][0]" is the color facing FRONT (White Face) side of the Corner
    made by FRONT, UP and LEFT (FUL) Faces of the cube

    "U[0][0]" is the color facing UP (Green Face) side of the Corner
    made by BACK, UP and LEFT (BUL) Faces of the cube

    "L[0][0]" is the color facing LEFT (Red Face) side of the Corner
    made by BACK, UP and LEFT (BUL) Faces of the cube

    "R[0][0]" is the color facing RIGHT (Opposite Face of Red) side of the Corner
    made by FRONT, UP and RIGHT (FUR) Faces of the cube

    "D[0][0]" is the color facing DOWN (Opposite Face of Green) side of the Corner
    made by FRONT, DOWN and LEFT (FDL) Faces of the cube

    "B[0][0]" is the color facing BACK (Opposite Face of White) side of the Corner
    made by BACK, DOWN and LEFT (BDL) Faces of the cube

    The Program solves the cube in the following steps:
        - First Layer
            Daisy
            White Cross
            White Corners
        - Second Layer
        - Last Layer
            Orient Edges
            Permute Edges
            Permute Corners
            Orient Corners

    Solution of the cube is stored in an array (Cube.rotates)
    The Solution Array contains integers that represents rotations as:
        1: Rotate FRONT (White Face) side Clockwise
        -1: Rotate FRONT (White Face) side Anti Clockwise
        2: Rotate UP (Green Face) side Clockwise
        -2: Rotate UP (Green Face) side Anti Clockwise
        3: Rotate LEFT (Red Face) side Clockwise
        -3: Rotate LEFT (Red Face) side Anti Clockwise
        4: Rotate RIGHT (Opposite Face of Red) side Clockwise
        -4: Rotate RIGHT (Opposite Face of Red) side Anti Clockwise
        5: Rotate DOWN (Opposite Face of Green) side Clockwise
        -5: Rotate DOWN (Opposite Face of Green) side Anti Clockwise
        6: Rotate BACK (Opposite Face of White) side Clockwise
        -6: Rotate BACK (Opposite Face of White) side Anti Clockwise
"""


from random import choice


class Cube:
    def __init__(self, cube=None):
        if cube is None:
            self.cube = {'F': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                         'U': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                         'L': [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
                         'R': [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
                         'D': [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
                         'B': [[5, 5, 5], [5, 5, 5], [5, 5, 5]]}
        else:
            self.cube = cube
        self.func = {'F': self.F, 'U': self.U, 
                     'L': self.L, 'R': self.R, 
                     'D': self.D, 'B': self.B}
        self.anti_func = {'F': self.F_, 'U': self.U_, 
                          'L': self.L_, 'R': self.R_, 
                          'D': self.D_, 'B': self.B_}
        self.opps = {'F': 'B', 'B': 'F', 'U': 'D', 
                     'D': 'U', 'L': 'R', 'R': 'L'}
        self.values = {'F': 0, 'U': 1, 'L': 2, 
                       'R': 3, 'D': 4, 'B': 5}
        self.itv = {0: 'F', 1: 'U', 2: 'L', 
                    3: 'R', 4: 'D', 5: 'B'}
        self.dire = {'F': self.F, 'F_': self.F_, 
                     'U': self.U, 'U_': self.U_,
                     'L': self.L, 'L_': self.L_, 
                     'R': self.R, 'R_': self.R_, 
                     'D': self.D, 'D_': self.D_, 
                     'B': self.B, 'B_': self.B_}
        self.rotates = []
        self.update_corners()
        self.update_centers()
        self.rotates = []

    def reset(self):
        """
        Reset the Cube
        """
        self.cube = {'F': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                     'U': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                     'L': [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
                     'R': [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
                     'D': [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
                     'B': [[5, 5, 5], [5, 5, 5], [5, 5, 5]]}
        self.rotates = []

    def rotate(self, side):
        self.dire[side]()

    def generate_random_cube(self):
        """
        Generate a random Cube
        """
        rots = "FULRDB"
        funs = [self.func, self.anti_func]
        for i in range(300):
            c = choice(rots)
            f = choice(funs)
            f[c]()
        self.rotates = []
    
    def update_rotates(self):
        """
        Remove Unnecessary (Repetitive) Rotations
        """
        temp = []
        k = 0
        for i, j in enumerate(self.rotates):
            if k > 0:
                k -= 1
                continue
            if i < len(self.rotates) - 3:
                if self.rotates[i] == self.rotates[i+1] == self.rotates[i+2] == self.rotates[i+3]:
                    k = 3
                    continue
                elif self.rotates[i] == self.rotates[i+1] == self.rotates[i+2]:
                    j = -self.rotates[i]
                    k = 2
            temp.append(j)
        self.rotates = temp
        
    def update_corners(self):
        """
        Update Corners of the Cube
        """
        f, u, l, r, d, b = self.cube['F'], self.cube['U'], self.cube['L'], self.cube['R'], self.cube['D'], self.cube['B']
        corners = {'FUL': [f[0][0], u[2][0], l[0][2]], 
                   'FUR': [f[0][2], u[2][2], r[0][0]], 
                   'FDL': [f[2][0], d[0][0], l[2][2]], 
                   'FDR': [f[2][2], d[0][2], r[2][0]], 
                   'BUL': [b[2][0], u[0][0], l[0][0]], 
                   'BUR': [b[2][2], u[0][2], r[0][2]], 
                   'BDL': [b[0][0], d[2][0], l[2][0]], 
                   'BDR': [b[0][2], d[2][2], r[2][2]]}
        self.white_cor = {}
        self.yellow_cor = {}
        for k in corners:
            if 0 in corners[k]:
                self.white_cor[k] = corners[k]
            if 5 in corners[k]:
                self.yellow_cor[k] = corners[k]
        self.corners = corners
    
    def update_centers(self):
        """
        Update Edges of the Cube
        """
        f, u, l, r, d, b = self.cube['F'], self.cube['U'], self.cube['L'], self.cube['R'], self.cube['D'], self.cube['B']
        c = {'FU': [f[0][1], u[2][1]], 
             'FL': [f[1][0], l[1][2]], 
             'FD': [f[2][1], d[0][1]], 
             'FR': [f[1][2], r[1][0]],
             'BU': [b[2][1], u[0][1]], 
             'BL': [b[1][0], l[1][0]],
             'BD': [b[0][1], d[2][1]],
             'BR': [b[1][2], r[1][2]], 
             'UL': [u[1][0], l[0][1]], 
             'UR': [u[1][2], r[0][1]], 
             'DL': [d[1][0], l[2][1]], 
             'DR': [d[1][2], r[2][1]]}
        self.s_centers = {'F': {}, 'B': {}, 'U': {},
                          'D': {}, 'L': {}, 'R': {}}
        self.middle_cen = {'UL': None, 'UR': None, 'DL': None, 'DR': None}
        self.white_cen = {}
        for k in c:
            if 'F' in k:
                self.s_centers['F'][k] = c[k]
            if 'B' in k:
                self.s_centers['B'][k] = c[k]
            if 'U' in k:
                self.s_centers['U'][k] = c[k]
            if 'D' in k:
                self.s_centers['D'][k] = c[k]
            if 'L' in k:
                self.s_centers['L'][k] = c[k]
            if 'R' in k:
                self.s_centers['R'][k] = c[k]
            if 0 in c[k]:
                self.white_cen[k] = c[k]
        for k in self.middle_cen:
            self.middle_cen[k] = c[k]
        self.centers = c
    
    def solve(self):
        self.first_layer()
        self.second_layer()
        self.last_layer()
        self.update_rotates()

    def first_layer(self):
        """
        Solve First Layer of the Cube
        """
        def daisy():
            """
            Make Daisy (White Edges around Yellow Center)
            """
            def check_same(side):
                cen = self.s_centers[side][f'B{side}']
                if cen[0] == 0:
                    self.func['B']()
            
            next = {'L': 'U', 'U': 'R', 'R': 'D', 'D': 'L'}
            prev = {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U'}
            for n in range(4):
                wc = self.white_cen
                for k in wc:
                    key = k
                    value = wc[k]
                    ind = value.index(0)
                    if key[ind] != 'B':
                        break
                count = 0
                for k in wc:
                    if k[wc[k].index(0)] == 'B':
                        count += 1
                if count > n:
                    continue
                if 'B' in key:
                    self.func[key[1]]()
                    for check in range(n):
                        check_same(next[key[1]])
                    self.func[next[key[1]]]()
                elif 'F' in key:
                    for check in range(n):
                        check_same(key[1])
                    self.func[key[1]]()
                    if key[ind] == 'F':
                        for check in range(n):
                            check_same(key[1])
                        self.func[key[1]]()
                    else:
                        for check in range(n):
                            check_same(prev[key[1]])
                        self.anti_func[prev[key[1]]]()
                elif 'U' in key:
                    if key[ind] == 'U':
                        if 'L' in key:
                            for check in range(n):
                                check_same('L')
                            self.anti_func['L']()
                        else:
                            for check in range(n):
                                check_same('R')
                            self.func['R']()
                    else:
                        for check in range(n):
                            check_same('U')
                        if 'L' in key:
                            self.func['U']()
                        else:
                            self.anti_func['U']()
                else:
                    if key[ind] == 'D':
                        if 'L' in key:
                            for check in range(n):
                                check_same('L')
                            self.func['L']()
                        else:
                            for check in range(n):
                                check_same('R')
                            self.anti_func['R']()
                    else:
                        for check in range(n):
                            check_same('D')
                        if 'L' in key:
                            self.anti_func['D']()
                        else:
                            self.func['D']()
        
        def white_cross():
            """
            Make White Cross
            """
            wc = list(self.s_centers['B'].keys())
            for k in wc:
                side = k[1]
                while self.s_centers['B'][k][1] != self.values[side] or self.s_centers['B'][k][0] != 0:
                    self.func['B']()
                self.func[side]()
                self.func[side]()
        
        def white_corners():
            """
            Solve White Corners
            """
            def algo(key):
                side = {'FUR': 'U', 'BUR': 'U',
                        'FUL': 'L', 'BUL': 'L',
                        'FDL': 'D', 'BDL': 'D',
                        'FDR': 'R', 'BDR': 'R'}
                self.anti_func[side[key]]()
                self.anti_func['B']()
                self.func[side[key]]()
                self.func['B']()
            
            def check_pos(pos, val):
                val.remove(0)
                i1, i2 = self.values[pos[1]], self.values[pos[2]]
                if i1 in val and i2 in val:
                    return True
                return False
            
            def correct(p, val):
                v = self.values
                if v[p[0]] == val[0] and v[p[1]] == val[1] and v[p[1]] == val[1]:
                    return True
                return False
            
            while True:
                wc = self.white_cor
                keys = list(wc.keys())
                temp = None
                for k in keys[:]:
                    if correct(k, wc[k][:]):
                        keys.remove(k)
                if len(keys) == 0:
                    return
                k = choice(keys)
                if check_pos(k, wc[k][:]):
                    algo(k)
                else:
                    if 'F' in k:
                        algo(k)
                    self.func['B']()
        daisy()
        white_cross()
        white_corners()
        
    def second_layer(self):
        """
        Solve Second Layer of the Cube
        """
        def algo1(s1, s2):
            self.func[s1]()
            self.func[s2]()
            self.anti_func[s1]()
            self.anti_func[s2]()
                
        def algo2(s1, s2):
            self.anti_func[s1]()
            self.anti_func[s2]()
            self.func[s1]()
            self.func[s2]()
                
        def left(val):
            val = sorted(val)
            key = int(f'{val[0]}{val[1]}')
            l_s = {12: 'L', 13: 'U', 24: 'D', 34: 'R'}
            f_s = {12: 'U', 13: 'R', 24: 'L', 34: 'D'}
            algo2('B', l_s[key])
            algo1('B', f_s[key])
            
        def right(val):
            val = sorted(val)
            key = int(f'{val[0]}{val[1]}')
            r_s = {12: 'U', 13: 'R', 24: 'L', 34: 'D'}
            f_s = {12: 'L', 13: 'U', 24: 'D', 34: 'R'}
            algo1('B', r_s[key])
            algo2('B', f_s[key])
            
        def check_pos(key, val):
            if self.values[key[1]] == val[1]:
                return True
            return False
            
        def correct_pos(key, val):
            i1, i2 = self.values[key[0]], self.values[key[1]]
            if i1 == val[0] and i2 == val[1]:
                return True
            return False
            
        def place(v):
            lefts = [121, 133, 242, 141]
            tc = self.s_centers['B']
            for ke in tc:
                if v == tc[ke]:
                    k = ke
                    break
            if check_pos(k, v[:]):
                v.sort()
                v = int(f'{v[0]}{v[1]}{tc[k][1]}')
                if v in lefts:
                    left(tc[k][:])
                else:
                    right(tc[k][:])
            else:
                self.func['B']()
                place(v)
        while True:
            top_cen = self.s_centers['B']
            nums = [1, 2, 3, 4]
            placeables = []
            for k in top_cen:
                if all(i in nums for i in top_cen[k]):
                    placeables.append(top_cen[k][:])
            if len(placeables) != 0:
                place(placeables[0][:])
            else:
                mc = self.middle_cen
                correctables = []
                for k in mc:
                    if all(i in nums for i in mc[k]):
                        if not correct_pos(k, mc[k]):
                            correctables.append(k)
                if len(correctables) == 0:
                    return
                else:
                    k = correctables[0]
                    left(mc[k][:])
    
    def last_layer(self):
        """
        Solve Last Layer of the Cube
        """
        def orient_edges():
            """
            Orient Edges in the correct orientation
            """
            def algo():
                s = "URB"
                for i in s:
                    self.func[i]()
                s = "RBU"
                for i in s:
                    self.anti_func[i]()
            
            for n in range(4):
                tc = self.s_centers['B']
                corrects = []
                for k in tc:
                    if tc[k][0] == 5:
                        corrects.append(k)
                if len(corrects) == 4:
                    break
                if len(corrects) < 2:
                    algo()
                else:
                    co = 'LR'
                    cs = 'DL'
                    ws1 = 'UL'
                    ws2 = 'RD'
                    s1, s2 = corrects[0][1], corrects[1][1]
                    if self.opps[s1] == s2:
                        if s1 not in co:
                            self.func['B']()
                        algo()
                    else:
                        if s1 not in cs and s2 not in cs:
                            self.func['B']()
                            self.func['B']()
                        elif s1 in ws1 and s2 in ws1:
                            self.func['B']()
                        elif s1 in ws2 and s2 in ws2:
                            self.anti_func['B']()
                        algo()
        
        def permute_edges():
            """
            Solve oriented Edges
            """
            def algo():
                s = "RB"
                for i in s:
                    self.func[i]()
                self.anti_func['R']()
                s = "BRBB"
                for i in s:
                    self.func[i]()
                self.anti_func['R']()
            
            def done():
                t_c = self.s_centers['B']
                k = [1, 2, 3, 4]
                v = []
                for k_ in k:
                    v.append(t_c[f'B{self.itv[k_]}'][1])
                
                if k == v:
                    return True
                return False
            
            def check_opps():
                opps = {'BU': 'BD', 'BD': 'BU',
                        'BL': 'BR', 'BR': 'BL'}
                count = 0
                for k in self.s_centers['B']:
                    v = self.s_centers['B'][k][:]
                    v_o = self.s_centers['B'][opps[k]][:]
                    if v[1] + v_o[1] == 5:
                        count += 1
                        key = k
                        break
                if count > 0:
                    rot = {'BU': 0, 'BR': 1, 'BD': 2, 'BL': 3}
                    for i in range(rot[k]):
                        self.func['B']()
                    return True
                return False
                
            def check_neibs():
                neigbs = {'BU': 'BR', 'BR': 'BD',
                          'BD': 'BL', 'BL': 'BU'}
                neigbs_v = {1: 3, 3: 4, 4: 2, 2: 1}
                count = 0
                for k in self.s_centers['B']:
                    v = self.s_centers['B'][k][:]
                    v_n = self.s_centers['B'][neigbs[k]][:]
                    if neigbs_v[v[1]] == v_n[1]:
                        count += 1
                        key = k
                        break
                if count > 0:
                    rot = {'BU': 3, 'BR': 0, 'BD': 1, 'BL': 2}
                    for i in range(rot[k]):
                        self.func['B']()
                    return True
                return False
            
            while True:
                if check_opps() and not check_neibs():
                    algo()
                elif check_neibs() and not done():
                    algo()
                elif done():
                    break
            
            temp = self.s_centers['B']['BU'][1]
            d = {1: 0, 2: 1, 3: 3, 4: 2}
            for i in range(d[temp]):
                self.func['B']()
        
        def permute_corners():
            """
            Permute Corners
            """
            def algo():
                self.func['B']()
                self.func['R']()
                self.anti_func['B']()
                self.anti_func['L']()
                self.func['B']()
                self.anti_func['R']()
                self.anti_func['B']()
                self.func['L']()
            
            def check_pos(pos):
                l_n = {'BUL': 'BL', 'BUR': 'BU', 
                       'BDR': 'BR', 'BDL': 'BD'}
                r_n = {'BUL': 'BU', 'BUR': 'BR', 
                       'BDR': 'BD', 'BDL': 'BL'}
                lcv = self.centers[l_n[pos]][1]
                rcv = self.centers[r_n[pos]][1]
                
                vals1 = sorted([lcv, rcv])
                val = self.corners[pos][:]
                val.remove(5)
                vals2 = sorted(val)
                if vals1 == vals2:
                    return True
                return False
            
            def correct_one():
                for i in range(4):
                    if check_pos('BUR'):
                        break
                    else:
                        self.func['B']()
                else:
                    algo()
                    correct_one()
            
            correct_one()
            yck = (self.yellow_cor.keys())
            while True:
                n = 0
                for k in yck:
                    if check_pos(k):
                        n += 1
                if n == 4:
                    temp = self.s_centers['B']['BU'][1]
                    d = {1: 0, 2: 1, 3: 3, 4: 2}
                    for i in range(d[temp]):
                        self.func['B']()
                    break
                else:
                    algo()
                    algo()
                    
        def orient_corners():
            """
            Orient permuted Corners in the correct Orientation
            """
            def algo():
                self.anti_func['R']()
                self.anti_func['F']()
                self.func['R']()
                self.func['F']()
                
            def check_pos(pos):
                l_n = {'BUL': 'BL', 'BUR': 'BU', 
                       'BDR': 'BR', 'BDL': 'BD'}
                r_n = {'BUL': 'BU', 'BUR': 'BR', 
                       'BDR': 'BD', 'BDL': 'BL'}
                lcv = self.centers[l_n[pos]][1]
                rcv = self.centers[r_n[pos]][1]
                
                vals1 = sorted([lcv, rcv])
                val = self.corners[pos][:]
                
                val.remove(5)
                vals2 = sorted(val)
                if vals1 == vals2:
                    return True
                return False
            
            def correct(p):
                val = self.corners[p]
                if val[0] == 5:
                    return True
                return False
            
            yck = (self.yellow_cor.keys())
            for s in range(4):
                while not correct('BUR'):
                    algo()
                    algo()
                self.func['B']()
                while not check_pos('BUR'):
                    self.func['B']()
        
        orient_edges()
        permute_edges()
        permute_corners()
        orient_corners()

    def F(self):
        """
        For Rotating Clockwise FRONT (White Face) side of the cube
        """
        self.rotate_clockwise('F')
        r = self.cube['R']
        l = self.cube['L']
        u = self.cube['U']
        d = self.cube['D']
        temp1, temp2 = [], []
        for i in range(3):
            temp1.append(l[2 - i][2])
            temp2.append(r[2 - i][0])
        for i in range(3):
            u[2][i], r[i][0], d[0][i], l[i][2] = temp1[i], u[2][i], temp2[i], d[0][i]
        self.rotates.append(1)
        self.update_corners()
        self.update_centers()

    def F_(self):
        """
        For Rotating Anti Clockwise FRONT (White Face) side of the cube
        """
        self.rotate_anticlockwise('F')
        r = self.cube['R']
        l = self.cube['L']
        u = self.cube['U']
        d = self.cube['D']
        temp1, temp2 = [], []
        for i in range(3):
            temp1.append(d[0][2 - i])
            temp2.append(u[2][2 - i])
        for i in range(3):
            u[2][i], r[i][0], d[0][i], l[i][2] = r[i][0], temp1[i], l[i][2], temp2[i]
        self.rotates.append(-1)
        self.update_corners()
        self.update_centers()

    def U(self):
        """
        For Rotating Clockwise UP (Green Face) side of the cube
        """
        self.rotate_clockwise('U')
        f = self.cube['F']
        r = self.cube['R']
        b = self.cube['B']
        l = self.cube['L']
        f[0], l[0], b[2], r[0] = r[0], f[0], list(reversed(l[0])), list(reversed(b[2]))
        self.rotates.append(2)
        self.update_corners()
        self.update_centers()

    def U_(self):
        """
        For Rotating Anti Clockwise UP (Green Face) side of the cube
        """
        self.rotate_anticlockwise('U')
        f = self.cube['F']
        r = self.cube['R']
        b = self.cube['B']
        l = self.cube['L']
        f[0], l[0], b[2], r[0] = l[0], list(reversed(b[2])), list(reversed(r[0])), f[0]
        self.rotates.append(-2)
        self.update_corners()
        self.update_centers()

    def L(self):
        """
        For Rotating Clockwise LEFT (Red Face) side of the cube
        """
        self.rotate_clockwise('L')
        f = self.cube['F']
        u = self.cube['U']
        b = self.cube['B']
        d = self.cube['D']
        for i in range(3):
            f[i][0], u[i][0], b[i][0], d[i][0] = u[i][0], b[i][0], d[i][0], f[i][0]
        self.rotates.append(3)
        self.update_corners()
        self.update_centers()

    def L_(self):
        """
        For Rotating Anti Clockwise LEFT (Red Face) side of the cube
        """
        self.rotate_anticlockwise('L')
        f = self.cube['F']
        u = self.cube['U']
        b = self.cube['B']
        d = self.cube['D']
        for i in range(3):
            f[i][0], u[i][0], b[i][0], d[i][0] = d[i][0], f[i][0], u[i][0], b[i][0]
        self.rotates.append(-3)
        self.update_corners()
        self.update_centers()

    def R(self):
        """
        For Rotating Clockwise RIGHT (Opposite Face of Red) side of the cube
        """
        self.rotate_clockwise('R')
        f = self.cube['F']
        u = self.cube['U']
        b = self.cube['B']
        d = self.cube['D']
        for i in range(3):
            f[i][2], u[i][2], b[i][2], d[i][2] = d[i][2], f[i][2], u[i][2], b[i][2]
        self.rotates.append(4)
        self.update_corners()
        self.update_centers()

    def R_(self):
        """
        For Rotating Anti Clockwise RIGHT (Opposite Face of Red) side of the cube
        """
        self.rotate_anticlockwise('R')
        f = self.cube['F']
        u = self.cube['U']
        b = self.cube['B']
        d = self.cube['D']
        for i in range(3):
            f[i][2], u[i][2], b[i][2], d[i][2] = u[i][2], b[i][2], d[i][2], f[i][2]
        self.rotates.append(-4)
        self.update_corners()
        self.update_centers()

    def D(self):
        """
        For Rotating Clockwise DOWN (Opposite Face of Green) side of the cube
        """
        self.rotate_clockwise('D')
        f = self.cube['F']
        r = self.cube['R']
        b = self.cube['B']
        l = self.cube['L']
        f[2], l[2], b[0], r[2] = l[2], list(reversed(b[0])), list(reversed(r[2])), f[2]
        self.rotates.append(5)
        self.update_corners()
        self.update_centers()

    def D_(self):
        """
        For Rotating Anti Clockwise DOWN (Opposite Face of Green) side of the cube
        """
        self.rotate_anticlockwise('D')
        f = self.cube['F']
        r = self.cube['R']
        b = self.cube['B']
        l = self.cube['L']
        f[2], l[2], b[0], r[2] = r[2], f[2], list(reversed(l[2])), list(reversed(b[0]))
        self.rotates.append(-5)
        self.update_corners()
        self.update_centers()

    def B(self):
        """
        For Rotating Clockwise BACK (Opposite Face of White) side of the cube
        """
        self.rotate_clockwise('B')
        r = self.cube['R']
        l = self.cube['L']
        u = self.cube['U']
        d = self.cube['D']
        temp1, temp2 = [], []
        for i in range(3):
            temp1.append(d[2][2 - i])
            temp2.append(u[0][2 - i])
        for i in range(3):
            u[0][i], r[i][2], d[2][i], l[i][0] = r[i][2], temp1[i], l[i][0], temp2[i]
        self.rotates.append(6)
        self.update_corners()
        self.update_centers()

    def B_(self):
        """
        For Rotating Anti Clockwise BACK (Opposite Face of White) side of the cube
        """
        self.rotate_anticlockwise('B')
        r = self.cube['R']
        l = self.cube['L']
        u = self.cube['U']
        d = self.cube['D']
        temp1, temp2 = [], []
        for i in range(3):
            temp1.append(l[2 - i][0])
            temp2.append(r[2 - i][2])
        for i in range(3):
            u[0][i], r[i][2], d[2][i], l[i][0] = temp1[i], u[0][i], temp2[i], d[2][i]
        self.rotates.append(-6)
        self.update_corners()
        self.update_centers()

    def rotate_clockwise(self, side):
        s = self.cube[side]
        s[0][0], s[0][1], s[0][2], s[1][0], s[1][2], s[2][0], s[2][1], s[2][2] = s[2][0], s[1][0], s[0][0], s[2][1], s[0][1], s[2][2], s[1][2], s[0][2]

    def rotate_anticlockwise(self, side):
        s = self.cube[side]
        s[0][0], s[0][1], s[0][2], s[1][0], s[1][2], s[2][0], s[2][1], s[2][2] = s[0][2], s[1][2], s[2][2], s[0][1], s[2][1], s[0][0], s[1][0], s[2][0]
