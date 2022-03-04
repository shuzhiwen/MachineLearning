#include "opencv2/core/core.hpp"
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <fstream>
#include <iostream>

using namespace std;
using namespace cv;

int main()
{
  VideoCapture capture(0);

  CascadeClassifier School_badge;

  School_badge.load("dst/cascade.xml");

  if (School_badge.empty())
  {
    std::cerr << "load detector failed!!!" << std::endl;
    return -1;
  }

  // 获取训练集的原始尺寸，作为分类器的最小尺寸，这样能得到最佳的检测效果（不是必须的）
  Size original_size = School_badge.getOriginalWindowSize();

  while (1)
  {
    Mat image;
    capture >> image;

    Mat image_gray;
    cvtColor(image, image_gray, COLOR_BGR2GRAY);

    // 降噪
    blur(image_gray, image_gray, Size(7, 7));

    // 用于保存检测到的目标窗口
    std::vector<Rect> badges;

    // 进行多尺度图片检测
    School_badge.detectMultiScale(image_gray, badges, 1.1, 3, 0 | CASCADE_SCALE_IMAGE, original_size);

    // 将检测到的目标窗口逐个绘制到原图上
    for (size_t i = 0; i < badges.size(); i++)
    {
      rectangle(image, badges[i], Scalar(0, 0, 255), 2, 8, 0);
    }

    imshow("detect result", image);
    waitKey(1);
  }
}
