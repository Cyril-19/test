Learning APP

This is a Streamlit-based Learning Application that allows users to upload images or capture images from the camera, extract text from these images, and then analyze the extracted text using OpenAI's language model to provide answers to questions.
Features:

Image Source Selection: Users can choose to upload an image or capture an image from the camera.

Text Extraction: The application extracts text from the uploaded or captured image.

Answer Generation: After text extraction, the application analyzes the extracted text to generate answers using an OpenAI language model.

Retry Mechanism: If the extracted text is not satisfactory, users can request a retry, which sends the image to OpenAI again for analysis.


This is a Streamlit-based Learning Application that allows users to upload images or capture images from the camera, extract text from these images, and then analyze the extracted text using OpenAI's language model to provide answers to questions.
Features:

Image Source Selection: Users can choose to upload an image or capture an image from the camera.

Text Extraction: The application extracts text from the uploaded or captured image.

Answer Generation: After text extraction, the application analyzes the extracted text to generate answers using an OpenAI language model.

Retry Mechanism: If the extracted text is not satisfactory, users can request a retry, which sends the image to OpenAI again for analysis.

Cost Analysis: The application displays the cost of the analysis performed by OpenAI.


How to Run:

Clone this repository to your local machine.

Install the required dependencies by running:

    pip install -r requirements.txt

Run the Streamlit app by executing:

    streamlit run app.py

Once the application is running, select the desired image source (either upload an image or capture from the camera).

After the image is processed, the extracted text will be displayed along with an option to confirm and continue or retry the analysis.

If the analysis is confirmed, the application will provide the generated answer based on the extracted text.

If the extracted text is unsatisfactory, users can retry the analysis, which will send the image to OpenAI again for re-analysis.

After the analysis, the application will display the generated answer along with the cost of the analysis.

