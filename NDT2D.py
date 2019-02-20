# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:41:57 2019

@author: lytov
"""
import numpy as np
import math
from makeOccupancyGrid import makeOccupancyGrid
from getCoordinatesSubgrid import getCoordinatesSubgrid
from checkSingular import checkSingular
from checkConv import checkConv
from normAngle import normAngle


class Ndt2D:
    def __init__(self):
        self.filtered_cloud = np.zeros((2, 1))
        self.target_cloud = np.zeros((2, 1))
        self.epsilon = 1.
#        self.resolution = 0
        self.param = {
                       'L': None,
                       'xmin' : None,
                       'xmax' : None,
                       'ymin' : None,
                       'ymax' : None
                      }
        
    def set_target_cloud(self, target_cloud):
        self.target_cloud = target_cloud
    
    def set_source_cloud(self, filtered_cloud):
        self.filtered_cloud = filtered_cloud   # здесь будет только ссылка на array?
    
    def set_epsilon(self, eps):
        self.epsilon = eps
    
    def set_resolution_grid(self, resolution):
        self.param = {
                  'L': resolution,
                  'xmin' : -25,
                  'xmax' :  25,
                  'ymin' :   0,
                  'ymax' :  50
                 }
        
    def set_step_size(self):
        pass
    
    def set_maximum_iterations(self, max_iter):
        self.max_iter = max_iter
    
    def has_converged(self):
        pass
    
    def get_fitness_score(self):
        pass
    
    def get_final_transformation(self):
        pass
    
    def get_source_cloud(self):
        return self.filtered_cloud
    
    def calc_distribution_parameters(self, cloud):
        sigma = np.cov(cloud)
        mu = np.mean(cloud, axis=1)
        
        return mu, sigma
    
    def transform_filtered_cloud(self):
        theta = self.init_guess[2]
        translate = np.array([self.init_guess[0],self.init_guess[1]])
        
        cos_r = math.cos(theta)
        sin_r = math.sin(theta)
        rotate = np.array([[cos_r, -sin_r], [sin_r, cos_r]])
        self.filtered_cloud = np.dot(rotate, self.filtered_cloud.T)
        for i in range(len(self.filtered_cloud.T)):
            self.filtered_cloud[:,i] = self.filtered_cloud[:,i] + translate
        
    def allocate_cell_structure(self):
        return makeOccupancyGrid(self.target_cloud, self.param)
        
    def align(self, init_guess):
        ### Initialisation  ###
        size_filtered_scan = len(self.filtered_cloud)

        # Предположение о перемещении между target_cloud и filtered_cloud
        x0 = init_guess[0]
        y0 = init_guess[1]
        yaw0 = init_guess[2]

        # Сохранение первоначального предположения для пока не ясно чего в конце !ВНИМАНИЕ!
        original_p = np.array([x0, y0, yaw0])

        # Значение, которое будет итеративно находиться исходя из минимизации функции
        p = np.array([x0, y0, yaw0])

        # Параметры расчета, причем L задается, а остальные не изменяются и записаны исходя из параметров лидара,
        # что не очень хорошо. Еще есть вариант находить мин и макс значения скана.
        cell_size = self.param["L"]
        xmin = self.param["xmin"]
        xmax = self.param["xmax"]
        ymin = self.param["ymin"]
        ymax = self.param["ymax"]

        # ширина и длина облака точек
        x_range = abs(xmin) + abs(xmax)
        y_range = abs(ymin) + abs(ymax)

        # Количество ячеек по X и Y кратное размеру ячейки
        NX = x_range // cell_size
        NY = y_range // cell_size
        
        # generate the grids to fit both scans. Генерирование сетки target_cloud с параметрами распределения.
        sub_grids = self.allocate_cell_structure()
        
        # occGrid1-4 represents the 4 four different grids built over the map with
        # L/2 shift on 3 directions. See the function for details. We are going to
        # use Newton's algorithm to minimize the score function which uses the sum
        # of the four different PDF defined for each cell.

        # !ВНИМАНИЕ! Хрен знает
        lasterror = []
        corr = []

        # !ВНИМАНИЕ! И тут хрен знает как лучше инициализировать
        R, t, NI = None, None, 0

        # Пытаемся за maxIter итераций чет придумать. !ВНИМАНИЕ! Не ясно сколько итераций ставить как максимум
        for i in range(self.max_iter):

            # return if convergence is achieved. Тут, по идее, если ошибка меньше неясного критерия,
            # то вываливаемся из цикла for и в конце расчитываем R, t
            if checkConv(lasterror, corr):
                break

            # Эти параметры просто необходимы для расчета и чтобы лучше воспринимались
            x = p[0]
            y = p[1]
            yaw = p[2]
            cosy = math.cos(yaw)
            siny = math.sin(yaw)
            
            # initialize the gradient and Hessian for this iteration.
            grad = np.zeros(3)
            H = np.zeros([3,3])

            # В общем, ошибка, пока не ясно какая, но по-любому она есть. !ВНИМАНИЕ!
            merr = 0

            # В этом списке сохраняются точки трансформированного нового скана для отрисовки, т.е. после каждой
            # итерации можно отрисовать результат.
            curscan = []
            
            #   loop through all the points in S NEW and find the cell it falls in
            # in the 4 grids.
            for j in range(size_filtered_scan):
                pn = self.filtered_cloud[j]

                for k in range(len(sub_grids)):

                    # здесь будет ссылка на k-ый элемент subGrids
                    ogrid = sub_grids[k]

                    # Инициализируем переменные для одной из стадий расчета !ВНИМАНИЕ! какой?
                    gradS = np.zeros(3)
                    Hps = np.zeros([3,3])
                    
                    # transform the point using the latest estimation !ВНИМАНИЕ! NUMPY?!
                    v = [0, 0]
                    v[0] = x + cosy*pn[0] - siny*pn[1]
                    v[1] = y + siny*pn[0] + cosy*pn[1]

                    # для отрисовки
                    curscan.append([v[0], v[1]])
                    
                    # find in which cell of the grid it falls in. Просто находим координаты ячейки
                    ix, iy = getCoordinatesSubgrid(v[0], v[1], k, self.param)
                    
                    # We need to be inside the grid to have overlap
                    if ix < 0 or ix > NX-1 or iy < 0 or iy > NY-1:
                        continue
                    else:
                        #retrieve mean and covariance and of that cell and find the
                        #gradient of the likelihood function. The likelihood function
                        #is a pdf defined by mean and covariance created by the
                        #occupancy grid. It is used to find the likelihood of a point
                        #projected of being in a particular area of the grid. We need
                        #to derive this function to find the new estimation

                        # !ВНИМАНИЕ! по идее должен получить нужные данные
                        m = ogrid[int(ix)][int(iy)][0]
                        cov = ogrid[int(ix)][int(iy)][1]

                    # Слабое место, может быть мат ожидание равное нулю
                    if m[0] == 0. and m[1] == 0.:
                        continue
                    
                    # if the matrix is singular, we need a backup plan. Return np.array !ВНИМАНИЕ! Интересная штука
                    out, cov_tmp = checkSingular(cov)

                    # по формуле нам нужна обратная матрица
                    inv_cov = np.linalg.inv(cov_tmp)
                    
                    # Gradient of the transformation function
                    dv = [[1, 0, -pn[0]*siny-cosy*pn[1]],
                          [0, 1,  pn[0]*cosy-siny*pn[1]]]
                    
                    # difference with mean. !ВНИМАНИЕ! Сразу numpy.array?!
                    dnm = [v[0]-m[0], v[1]-m[1]]
                    dnmnp = np.array(dnm)
                    
                    # Calculate the Hessian of the likelihood function. Это только вторая производная по dTheta^2
                    vH = [[-pn[0]*cosy+siny*pn[1]],
                          [-pn[0]*siny-siny*pn[1]]]
                    vHnp = np.array(vH)

                    # Здесь и далее просто сокращения записи формулы градиента и матрицы Гессе
                    covdnm = np.dot(dnmnp, inv_cov)   # Скорость и точность решения?
                    exppart = math.exp(-(np.dot(covdnm, dnmnp.T))/2)
                    
                    # Gradient vector
                    dvnp = np.array(dv)
                    gradt = np.dot(np.dot(covdnm, dvnp), exppart)
                    
                    dnmdv_tmp = np.dot(covdnm, dvnp)
                    
                    dnmdv1 = dnmdv_tmp[0]
                    dnmdv2 = dnmdv_tmp[1]
                    dnmdv3 = dnmdv_tmp[2]
                    
                    dvnp_tmp = dvnp.T
                    dnmtdv1 = np.dot(dvnp_tmp[0,:], inv_cov)
                    dnmtdv2 = np.dot(dvnp_tmp[1,:], inv_cov)
                    dnmtdv3 = np.dot(dvnp_tmp[2,:], inv_cov)
                    
                    # Score function as error
                    merr = merr - exppart
                    
                    # Hessian of the function
                    Hp = [[((-dnmdv1)*dnmdv1-np.dot(dnmtdv1,dvnp_tmp[0,:]))*(-exppart),     #DВІ xx
                           ((-dnmdv1)*dnmdv2-np.dot(dnmtdv2,dvnp_tmp[0,:]))*(-exppart),     #DВІ xy
                           ((-dnmdv1)*dnmdv3-np.dot(dnmtdv3,dvnp_tmp[0,:]))*(-exppart)],    #DВІ xTHETA
                          [0,                                                   #DВІ yx
                           ((-dnmdv2)*dnmdv2-np.dot(dnmtdv2,dvnp_tmp[1,:]))*(-exppart),     #DВІ yy
                           ((-dnmdv2)*dnmdv3-np.dot(dnmtdv3,dvnp_tmp[1,:]))*(-exppart)],    #DВІ yTHETA
                          [0,                                                  #DВІ x THETA
                           0,                                                  #DВІ yTHETA
                           (((-dnmdv3)*dnmdv3-np.dot(dnmtdv3,dvnp_tmp[2,:]))-(np.dot(covdnm,vHnp)))*(-exppart)
                            #DВІ THETA THETA. The second derivative is defined only in this point
                            ]]

                    #H is symmetric, let's fill the remaining part
                    Hp[1][0] = Hp[0][1]
                    Hp[2][0] = Hp[0][2]
                    Hp[2][1] = Hp[1][2]
                    Hpnp = np.array(Hp)

                    # Обновление переменных
                    gradS = gradS + gradt
                    Hps = Hps + Hpnp

                # Обновление переменных
                H = H + Hps
                grad = grad + gradS
            
            #   Once we have the Hessian and Gradient of the function we calculate
            # the new translation
            det = np.linalg.det(H)
            if det != 0:
                invh = np.linalg.inv(H)
            else:
                # the Hessian inversion has failed !ВНИМАНИЕ! Что будем тут делать?!
                print("Hessian inversion has failed")
                break

            # по методу Ньютона находим ... блин, что
            dt = - np.dot(invh, grad.T)

            # !ВНИМАНИЕ! тут должен быть np.array
            p = p + dt
            p[2] = normAngle(p[2])
            
            # Maintain last errors to check convergence. !ВНИМАНИЕ! Не понятно как ищется ошибка
            lasterror.append(1/merr)
            corr.append([dt[0], dt[1], dt[2]])

            niterconv = 3  # minimum number of iterations before convergence check
            if len(lasterror) > niterconv:
                del lasterror[0]
                del corr[0]

        print("merr = ", merr)
        # Final result in quaternion. !ВНИМАНИЕ! Почему расчет производится таким образом?
        R = normAngle(p[2] - original_p[2])
        
        t = [p[0]-original_p[0], p[1]-original_p[1]]
        
        NI = i

        return R, t, NI

