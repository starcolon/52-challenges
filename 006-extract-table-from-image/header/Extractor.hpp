#ifndef EXTRACT_HPP
#define EXTRACT_HPP

#include <string>
#include <vector>
#include <tuple>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

struct Line 
{
  tuple<Point2d, Point2d> p; // End points
  inline void drawTo(Mat& im)
  {
    Point2d a,b;
    tie(a, b) = p;
    line(im, a, b, Scalar(255,0,0));
  }
};

/**
 * Generic extractor
 */
template <class A>
class Extract
{
public:
  inline Extract(){};
  virtual inline ~Extract() {};

  virtual vector<A> extract(Mat& im) const = 0;

  inline Mat binarise(Mat& im) const 
  {
    const double maxValue = 255;
    const int blockSize = 7;
    const double C = 0;

    Mat out = Mat::zeros(im.rows, im.cols, CV_8UC1);

    adaptiveThreshold(im, out, maxValue, THRESH_BINARY_INV, ADAPTIVE_THRESH_MEAN_C, blockSize, C);
    return out;
  }

  inline vector<Line> extractLines(Mat& im) const
  {
    vector<Line> v;

    float hrzSize = im.cols / 100;
    float verSize = im.rows / 100;

    auto hrzKernel = getStructuringElement(MORPH_RECT, Size(int(hrzSize), 1));
    auto verKernel = getStructuringElement(MORPH_RECT, Size(1, int(verSize)));

    Mat lineHorz = Mat::zeros(im.rows, im.cols, CV_8UC1);
    Mat lineVert = Mat::zeros(im.rows, im.cols, CV_8UC1);
    Mat lineAll = Mat::zeros(im.rows, im.cols, CV_8UC1);

    erode(im, lineHorz, hrzKernel);
    erode(im, lineVert, verKernel);

    imshow("horz", lineHorz);
    imshow("vert", lineVert);

    // TAOTODO
    return v;
  }
};

#endif