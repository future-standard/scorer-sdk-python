"""
 readAR.cpp

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""
#include <opencv2/opencv.hpp>
#include <aruco/aruco.h>
#include <opencv2/calib3d/calib3d.hpp>

int main(int argc, char* argv[])
{
    if (argc !=4){
        std::cout << "Usage: readAR <intrinsic yml> <jpeg | png> <log file>" << std::endl;
        exit(0);
    }
    // Load image
    cv::Mat inputImage = cv::imread(argv[2]);

    // Load camera parameters
    aruco::CameraParameters params;
    params.readFromXMLFile(argv[1]);
    params.resize(inputImage.size());

    // Recognize marker
    aruco::MarkerDetector detector;
    std::vector<aruco::Marker> markers;
    const float markerSize = 0.04f;
    detector.detect(inputImage, markers, params, markerSize);

    // Output results
    std::string filename = argv[3];
    std::ofstream log_file;
    log_file.open(filename, std::ios::out);

    std::cout << "Total " << markers.size() << " AR marker(s) were detected." << std::endl;
    log_file << "Total " << markers.size() << " AR marker(s) were detected." << std::endl;
    auto outputImage = inputImage.clone();
    for (auto&& marker : markers) {
        std::cout << marker.id << std::endl;
        log_file << marker.id << "=";
        for (int i = 0; i < 4; i++) {
            log_file << "(" << std::fixed << std::setprecision(1) << marker[i].x << ",";
            log_file << std::fixed << std::setprecision(1) << marker[i].y << ") ";
        }
        log_file << "Txyz=";
        for (int i = 0; i < 3; i++) {
            log_file << marker.Tvec.ptr< float >(0)[i] << " ";
        }
        log_file << "Rxyz=";
        for (int i = 0; i < 3; i++) {
            log_file << marker.Rvec.ptr< float >(0)[i] << " ";
        }

        cv::Mat objectPoints(2, 3, CV_32FC1);
        objectPoints.at< float >(0, 0) = 0;
        objectPoints.at< float >(0, 1) = 0;
        objectPoints.at< float >(0, 2) = 0;
        objectPoints.at< float >(1, 0) = 0;
        objectPoints.at< float >(1, 1) = 0;
        objectPoints.at< float >(1, 2) = marker.ssize;

        std::vector< cv::Point2f > imagePoints;
        cv::projectPoints(objectPoints, marker.Rvec, marker.Tvec, params.CameraMatrix, params.Distorsion, imagePoints);

        log_file << "Nvec=(";
        log_file << imagePoints[1].x - imagePoints[0].x << " ";
        log_file << imagePoints[1].y - imagePoints[0].y << ")";
        log_file << std::endl;

    }

    std::cout << std::endl;
    std::cout << "Details were written on" << std::endl;
    std::cout << filename << std::endl;

    return 0;
}
