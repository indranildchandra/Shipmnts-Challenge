import cv2
import numpy as np

def calculate_local_stats(im, map_m, map_s, winx, winy):
    im_sum, im_sum_sq=cv2.integral2(im, cv2.CV_64F)  #diffrent parameters sdepth & sqdepth -- BEWARE
    wxh = int(np.floor(winx/2))
    wyh = int(np.floor(winy/2))
    x_firstth = wxh
    y_firstth = wyh
    y_lastth = im.shape[0] -wyh-1

    winarea = winx * winy
    max_s = 0
    for j in range(y_firstth, y_lastth+1):
        # sum=0
        # sum_sq=0

        sum_top_left = im_sum[j-wyh,0]
        sum_top_right = im_sum[j-wyh, winx]
        sum_bottom_left = im_sum[j-wyh+winy, 0]
        sum_bottom_right = im_sum[j-wyh+winy, winx]

        sum_eq_top_left = im_sum_sq[j - wyh, 0]
        sum_eq_top_right = im_sum_sq[j - wyh, winx]
        sum_eq_bottom_left = im_sum_sq[j - wyh + winy, 0]
        sum_eq_bottom_right = im_sum_sq[j - wyh + winy, winx]

        sum = (sum_bottom_right + sum_top_left) - (sum_top_right + sum_bottom_left)
        sum_sq = (sum_eq_bottom_right + sum_eq_top_left) - (sum_eq_top_right + sum_eq_bottom_left)

        m = sum / winarea
        s= np.sqrt((sum_sq-m*sum)/winarea)
        if(s>max_s):
            max_s =s

        # map_m_data = map_m[j,x_firstth]
        # map_s_data = map_s[j,x_firstth]
        map_m[j, x_firstth] = m
        map_s[j, x_firstth] = s


        for i in range(1, im.shape[1]-winx+1):
            sum_top_left = im_sum[j - wyh, i]
            sum_top_right = im_sum[j - wyh, winx+i]
            sum_bottom_left = im_sum[j - wyh + winy, i]
            sum_bottom_right = im_sum[j - wyh + winy, winx+i]

            sum_eq_top_left = im_sum_sq[j - wyh, i]
            sum_eq_top_right = im_sum_sq[j - wyh, winx+i]
            sum_eq_bottom_left = im_sum_sq[j - wyh + winy, i]
            sum_eq_bottom_right = im_sum_sq[j - wyh + winy, winx+i]

            sum = (sum_bottom_right + sum_top_left) - (sum_top_right + sum_bottom_left)
            sum_sq = (sum_eq_bottom_right + sum_eq_top_left) - (sum_eq_top_right + sum_eq_bottom_left)

            m = sum / winarea
            s = np.sqrt((sum_sq - m * sum) / winarea)
            if (s > max_s):
                max_s = s

            map_m[j, x_firstth + i] = m
            map_s[j, x_firstth + i] = s

    return max_s

def get_binarised_image(im, winx, winy, k, dR):
    wxh=int(np.floor(winx/2))
    wyh=int(np.floor(winy/2))


    x_firstth = wxh
    x_lastth = im.shape[1] - wxh -1
    y_lastth = im.shape[0] - wyh -1
    y_firstth = wyh

    map_m = np.zeros(im.shape,dtype=np.float32)
    map_s = np.zeros(im.shape,dtype=np.float32)
    output = np.zeros(im.shape,dtype=np.uint8)

    max_s = calculate_local_stats(im, map_m, map_s, winx, winy)
    min_I, max_I, _ , _ = cv2.minMaxLoc(im)

    thsurf = np.zeros(im.shape, np.float32)

    for j in range(y_firstth, y_lastth+1):
        # th_surf_data = thsurf[j, wxh]
        for i in range(0,im.shape[1]-winx+1):
            m = map_m[j, wxh +i]
            s = map_s[j, wxh +i]

            th = m + k * (s/max_s-1)* (m-min_I)
            thsurf[j,wxh+i] = th

            if i==0:
                #LEFT BORDER
                for i in range(0, x_firstth+1):
                    thsurf[j,i] = th
                #LEFT UPPER CORNER
                if j==y_firstth:
                    for u in range(0,y_firstth):
                        for i in range(0,x_firstth+1):
                            thsurf[u, i] = th
                #LEFT LOWER CORNER
                if j == y_lastth:
                    for u in range(y_lastth+1, im.shape[0]):
                        for i in range(0, x_firstth + 1):
                            thsurf[u, i] = th
            #UPPER BORDER
            if j==y_firstth:
                for u in range(0,y_firstth):
                    thsurf[u, i +wxh] = th
            #LOWER BORDER
            if j == y_lastth:
                for u in range(y_lastth + 1, im.shape[0]):
                    thsurf[u, i + wxh] = th
        #RIGHT BORDER
        for i in range(x_lastth, im.shape[1]):
            thsurf[j,i]=th
        #RIGHT UPPER CORNER
        if j == y_firstth:
            for u in range(0, y_firstth):
                for i in range(x_lastth, im.shape[1]):
                    thsurf[u, i] = th
        #RIGHT LOWER CORNER
        if j == y_lastth:
            for u in range(y_lastth + 1, im.shape[0]):
                for i in range(x_lastth, im.shape[1]):
                    thsurf[u, i] = th

    print("surface created...")

    for y in range(0,im.shape[0]):
        for x in range(0,im.shape[1]):
            if im[y,x]>= thsurf[y,x]:
                output[y,x]=255
            else:
                output[y,x]=0
	
    return output



##Only for testing

#filepath = "2.png"
#im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
#res = get_binarised_image(im,100,100,0.5,128)
#print(res)
#cv2.imshow('',res)
#cv2.waitKey(10000)
# c,d=cv2.integral2(a, cv2.CV_64F)

# for j in range(1,5):
#     print(j)
# print(a.shape[0])
# print(a[0][0])
# print(d)
# print(c.shape)