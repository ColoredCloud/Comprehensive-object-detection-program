# Description
#### This is a complete set of applications for object location models based on convolutional neural networks. Users can use a simple crawler to crawl images from a web page. After regularizing and normalizing image data, such as size, the program will allow users to label the image data, and then use DIY test data to train the model. After all the training is complete, the user can test the model with other images

# Usage
#### 1. Scrape image data from the web page
Put the parsed page in file body.txt, and then edit the file "req.py" to indicate the folder scraped images will be saved in. Then run req.py, program will automatically save the image data in the specified folder.

#### 3. Label the regularized and normalized image data
Run TrainSetMaker.py, program will lable the image data, and save it as a tar file in the folder indicated in Settings.py. The correct sequence of operation is: firstly 打开图像, then lable the position of the object, then 保存图像, and finally 删除图像.The program will automatically normalize and standardize the image data.

#### 4. Use DIY test data to train the model
Run Main.py, program will train the model and save the trained model in the file indicated in Settings.py

#### 5. Test the model with other images
Run Test.py, program will load the model ,and then you can test it with other images.

# Contribution

If you would like to contribute to this project, please follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Push your branch to your fork of the repository.
5. Submit a pull request to the original repository.

Please ensure that your contributions follow the existing code style and include appropriate unit tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.