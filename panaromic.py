import cv2
import matplotlib.pyplot as plt
import numpy as np

img1 = cv2.imread('./images/desa-1.jpeg')
img2 = cv2.imread('./images/desa-2.jpeg')

if img1 is None or img2 is None:
    print('gambar kosong')

img1 = cv2.resize(img1, (0,0), fx=0.5, fy=0.5) 
img2 = cv2.resize(img2, (0,0), fx=0.5, fy=0.5)

# ubah ke grayscale buat deteksi fitur
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1_gray, None)
kp2, des2 = sift.detectAndCompute(img2_gray, None)

print("keypoints gambar 1:", len(kp1))
print("keypoints gambar 2:", len(kp2))

# ubah ke rgb buat plottting
img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# visual keypoints mentah
img1_kp = cv2.drawKeypoints(img1_rgb, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img2_kp = cv2.drawKeypoints(img2_rgb, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# matching fitur dengan BFMatcher
bf = cv2.BFMatcher(cv2.NORM_L2)
matches = bf.knnMatch(des1, des2, k=2)

# cari paling match
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)
        
print('jumlah match yg valid:', len(good_matches))

# stittching & homography
MIN_MATCH_COUNT = 10
if len(good_matches) > MIN_MATCH_COUNT:
    # get koordinat paling match
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # get matrix homography
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # logika kanvas
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # get sudut gambarr 1 after wrapping
    corners_img1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
    warped_corners_img1 = cv2.perspectiveTransform(corners_img1, H)
    
    # get sdut gambar 2
    corners_img2 = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)

    # gabungin semua sudht gambar
    all_corners = np.concatenate((warped_corners_img1, corners_img2), axis=0)

    x_min, y_min = np.int32(all_corners.min(axis=0).ravel())
    x_max, y_max = np.int32(all_corners.max(axis=0).ravel())
    
    # translation matriix
    translation_dist = [-x_min, -y_min]
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])
    
    # warping gambar
    panorama = cv2.warpPerspective(img1, H_translation.dot(H), (x_max - x_min, y_max - y_min))
    # tempel gambar 2
    panorama[translation_dist[1]:h2+translation_dist[1], translation_dist[0]:w2+translation_dist[0]] = img2
    
    img_matches = cv2.drawMatches(img1_rgb, kp1, img2_rgb, kp2, good_matches[:100], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    plt.figure(figsize=(20, 10))

    # keypints mentah gambar 1
    plt.subplot(2, 2, 1)
    plt.imshow(img1_kp)
    plt.title("keypoints detection (SIFT) - gambar 1")
    plt.axis('off')

    # keypoints mentah gambar 2
    plt.subplot(2, 2, 2) 
    plt.imshow(img2_kp)
    plt.title("keypoints detection (SIFT) - gambar 2")
    plt.axis('off')

    # feature matching
    plt.subplot(2, 2, 3)
    plt.imshow(img_matches)
    plt.title(f"feature matching: ({len(good_matches)} kecocokan)")
    plt.axis('off')

    # hasil panorama
    plt.subplot(2, 2, 4)
    panorama_rgb = cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB)
    plt.imshow(panorama_rgb)
    plt.title("hasil akhir: penyatuan gambar")
    plt.axis('off')

    plt.tight_layout()
    
    plt.savefig("./results/result.png", dpi=300, bbox_inches='tight')
    plt.show()

else: 
    print(f"gambar kurang matching, hanya {len(good_matches)}/{MIN_MATCH_COUNT} yang valid")
    print('ganti gambar yg lebih mirip')