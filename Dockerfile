FROM public.ecr.aws/lambda/python:3.12

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY scrape_wait_times.py ${LAMBDA_TASK_ROOT}
COPY create_image_with_text.py ${LAMBDA_TASK_ROOT}
COPY post_to_facebook.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]

# Copy and load environment variables
COPY .env ${LAMBDA_TASK_ROOT}
RUN pip3 install python-dotenv --target "${LAMBDA_TASK_ROOT}"