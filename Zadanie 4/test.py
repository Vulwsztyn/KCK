def gamma(img):
    g = np.mean(img) - 0.3
    return (img ** g)


def contrast(img):
    percmin = 0.3
    percmax = 2.0
    MIN = np.percentile(img, percmin)
    MAX = np.percentile(img, 100 - percmax)
    norm = (img - MIN) / (MAX - MIN)
    norm[norm[:, :] > 1] = 1
    norm[norm[:, :] < 0] = 0
    return norm


def threshold(img):
    thr = np.percentile(img, 4)
    std = np.std(img)
    if (std > 0.15):
        thr += 0.2
    else:
        thr -= 0.1
    if (std < 0.1): thr -= 0.2
    return (img > thr)


def dilation(img):
    return mp.erosion(img)


fig, ax = plt.subplots(18, 2, figsize=(20, 200))

for i in range(0, 18):
    img_origin = data.imread('s' + str(i + 1) + '.jpg', flatten=False)
    img = data.imread('s' + str(i + 1) + '.jpg', flatten=True)
    img = gamma(img)
    img = gamma(img)
    img = contrast(img)
    img = threshold(img)

    ax[i][0].imshow(img, cmap='gray')

    for j in range(0, 7):
        img = dilation(img)

    ax[i][1].imshow(img_origin)

    contours = measure.find_contours(img, 0.7)

    for n, contour in enumerate(contours):
        # np.amax(contour[:,1])-np.amin(contour[:,1]) > 50
        if (1):
            centroid = np.sum(contour, axis=0) / len(contour)
            ax[i][1].plot(contour[:, 1], contour[:, 0], linewidth=2)
            # ax[i].plot(centroid[1], centroid[0], marker='o', markersize=5, color="white")