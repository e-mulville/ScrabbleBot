    #CreateAndSavePFM('m.pfm')
    #img_in = loadPFM('m.pfm')
    #print(img_in[0][0])

    a = LoadAndSavePFM('urbanEM_latlong.pfm', 'test.pfm')
    print(a)
    for i in range(len(img_in)):
        for j in range(len(img_in)):
            distance = np.sqrt(np.power(abs(i-255),2) +np.power(abs(j-255),2))
            if distance > 255:
                img_in[i][j] = [0,0,0]
            else:
                alpha = np.arctan2(j-255,i-255)

                beta = np.arccos(distance/255)

                #vec = [(np.sin(alpha)+1)/2,(np.cos(alpha)+1)/2,np.sin(beta)]
                vec = [np.sin(alpha)*np.cos(beta),np.cos(alpha)*np.cos(beta),np.sin(beta)]

                view = [0,0,-1]
                n = np.array(vec)
                v = np.array(view)

                norm = np.linalg.norm(n)
                if norm != 0:
                    n = n/norm

                r = v - 2*np.dot(v,n)*n

                img_in[i][j] = r


    writePFM("a.pfm", img_in)
